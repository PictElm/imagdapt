import imagdapt as iap
from PIL import Image

class Util:
    @staticmethod
    def openImage(fp, mode='r', **kw):
        return Image.open(fp, mode, **kw)

    @staticmethod
    def newImage(mode, size, color=0, **kw):
        return Image.new(mode, size, color, **kw)

    @staticmethod
    def normVec(x, y, s):
        l = (x * x + y * y)**.5 / s
        return x / l, y / l

class Extractor:
    @staticmethod
    def getPixel(image, x, y, transform=None):
        x, y = int(x), int(y)
        w, h = image.size
        if x < 0:
            iap.log('clamp', "x negative")
            x = 0
        elif w - 1 < x:
            iap.log('clamp', "x above w", "(" + str(x) + ")")
            x = w - 1
        if y < 0:
            iap.log('clamp', "y negative")
            y = 0
        elif h - 1 < y:
            iap.log('clamp', "y above h", "(" + str(y) + ")")
            y = h - 1

        pixel = image.getpixel((x, y))
        return pixel if transform is None else transform(pixel)

    @staticmethod
    def extract(grid, additionalPixelTransform=None):
        r = []

        w_, h_ = grid.target
        a, b = grid[0, 0], grid[-1, 0]
        d, c = grid[0, -1], grid[-1, -1]

        px = lambda i: i / w_
        py = lambda j: j / h_

        wa, ha = b.x - a.x, d.y - a.y
        ua = iap.Point.vect(a, b, wa / w_)
        va = iap.Point.vect(a, d, ha / h_)

        wb, hb = c.x - d.x, c.y - b.y
        ub = iap.Point.vect(a, b, wb / w_)
        vb = iap.Point.vect(a, d, hb / h_)

        ux = lambda p: (1 - p) * ua.x + p * ub.x
        uy = lambda p: (1 - p) * ua.y + p * ub.y
        vx = lambda p: (1 - p) * va.x + p * vb.x
        vy = lambda p: (1 - p) * va.y + p * vb.y

        for j in range(h_):
            for i in range(w_):
                r.append(Extractor.getPixel(
                    grid.image,
                    a.x + i*ux(py(j)) + j*vx(py(j)),
                    a.y + i*uy(px(i)) + j*vy(px(i)),
                    additionalPixelTransform
                ))

        result = Util.newImage(grid.image.mode, grid.target)
        result.putdata(r)
        return result

    @staticmethod
    def extractLinear(grid, additionalPixelTransform=None):
        r = []

        w_, h_ = grid.target

        field = []
        w, h = grid.w - 1, grid.h - 1
        w__, h__ = w_ / w, h_ / h
        iap.log('debug', "vector field resolution is", w, "by", h, "bases")
        iap.log('debug', "with each representing", w__, "by", h__)

        for i in range(w):
            field.append([])
            for j in range(h):
                a, b = grid[i, j], grid[i + 1, j]
                d, c = grid[i, j + 1], grid[i + 1, j + 1]

                wa, ha = b.x - a.x, d.y - a.y
                ua = iap.Point.vect(a, b, wa / w__)
                va = iap.Point.vect(a, d, ha / h__)

                wb, hb = c.x - d.x, c.y - b.y
                ub = iap.Point.vect(a, b, wb / w__)
                vb = iap.Point.vect(a, d, hb / h__)

                field[-1].append([a, (ua, va), (ub, vb)])

        for j in range(h_):
            for i in range(w_):
                orig, base1, base2 = field[int(i / w__)][int(j / h__)]
                i_, j_ = i % w__, j % h__
                px, py = i_ / w__, j_ / h__

                ux = (1 - py) * base1[0].x + py * base2[0].x
                uy = (1 - px) * base1[0].y + px * base2[0].y
                vx = (1 - py) * base1[1].x + py * base2[1].x
                vy = (1 - px) * base1[1].y + px * base2[1].y

                r.append(Extractor.getPixel(
                    grid.image,
                    orig.x + i_ * ux + j_ * vx,
                    orig.y + i_ * uy + j_ * vy,
                    additionalPixelTransform
                ))

        result = Util.newImage(grid.image.mode, grid.target)
        result.putdata(r)
        return result

    @staticmethod
    def extractPolynomial(grid, additionalPixelTransform=None):
        r = []

        result = Util.newImage(grid.image.mode, grid.target)
        result.putdata(r)
        return result

    # TODO: change method signature to take a `Grid`
    @staticmethod
    def masked(srcImg, srcA, srcB, srcC, srcD, maskColor=(0,0,0)):
        r = []

        w, h = srcImg.size

        x, y = srcA
        s, t = srcC
        px = lambda i: max(min((x - i) / (x - s), 1), 0)
        py = lambda j: max(min((y - j) / (y - t), 1), 0)

        mx = lambda p: (1 - p) * srcA[0] + p * srcD[0]
        Mx = lambda p: (1 - p) * srcB[0] + p * srcC[0]
        my = lambda p: (1 - p) * srcA[1] + p * srcB[1]
        My = lambda p: (1 - p) * srcD[1] + p * srcC[1]

        isinside = lambda i, j: mx(py(j)) < i and i < Mx(py(j)) and my(px(i)) < j and j < My(px(i))

        for j in range(h):
            for i in range(w):
                r.append(srcImg.getpixel((i, j)) if isinside(i, j) else maskColor)

        img = Util.newImage(srcImg.mode, srcImg.size)
        img.putdata(r)
        return img
