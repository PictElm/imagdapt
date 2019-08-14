""" test with `python -m imagdapt $test_name`
"""

import imagdapt as iap
import sys
import matplotlib.pyplot as plt


# maps pre-calculated locations for the available test pictures
locations = { # size, dest, a, b, c, d, rows
    "1": [
        (2, 2), (800, 200),
        (220, 90), (760, 128), (775, 380), (230, 300),
        None
    ],
    "2": [
        (2, 2), (800, 200),
        (722, 555), (904, 523), (901, 562), (719, 596),
        None
    ],
    "test": [
        (2, 3), (800, 300),
        (580, 446), (1004, 394), (999, 545), (581, 624),
        {
            'tops': None,
            'rights': [ (1015, 433) ],
            'bottoms': None,
            'lefts': [ (592, 503) ]
        }
    ],
    "test-top": [
        (2, 2), (800, 100),
        (580, 446), (1004, 394), (1015, 433), (592, 503),
        None
    ],
    "test-bottom": [
        (2, 2), (800, 200),
        (592, 503), (1015, 433), (999, 545), (581, 624),
        None
    ],
    "test-full": [
        (4, 4), (1200, 798),
        (0, 0), (1200, 0), (1200, 798), (0, 798),
        None
    ]
}
tested = sys.argv[1] if 1 < len(sys.argv) else "test"


size, dest, a, b, c, d, rows = locations[tested]
grd = iap.Grid(
    size[0], size[1],
    topLeft=iap.Point(a),
    topRight=iap.Point(b),
    bottomRight=iap.Point(c),
    bottomLeft=iap.Point(d)
)
if rows:
    p = lambda l: l if l is None else [iap.Point(it) for it in l]
    grd.setRows(
        p(rows['tops']),
        p(rows['rights']),
        p(rows['bottoms']),
        p(rows['lefts'])
    )
grd.complete(rows=True, fill=True)


# transform=blackAndWhite
def blackAndWhite(pixel):
    if 1 < len([v for v in pixel if v < 128]):
        return (0, 0, 0)
    return (255, 255, 255)

src = iap.Util.openImage(f"./imagdapt/test/{tested}/picture.jpg")
ext = grd.bind(src, dest).extract(mode=iap.MODE_LINE)


plt.figure(1)

plt.subplot(121)
plt.imshow(src)
for k in range(len(grd)):
    X, Y = grd.getPlotShape(k)
    plt.plot(X, Y)

plt.subplot(122)
plt.imshow(ext)

plt.show()
