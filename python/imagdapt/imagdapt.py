from PIL import Image

DEBUG = __debug__

def debug(b):
    global DEBUG
    DEBUG = b

def open(fp, mode='r'):
    return Image.open(fp, mode)

def normVec(x, y, s):
    l = (x * x + y * y)**.5 / s
    return x / l, y / l

def extract(srcImg, srcA, srcB, srcC, srcD, destSize=None):
    r = []

    w_, h_ = destSize

    x, y = srcA
    s, t = srcC
    px = lambda i: i / w_
    py = lambda j: j / h_

    wa, ha = srcB[0] - x, srcD[1] - y
    sax, say = wa / w_, ha / h_
    uax, uay = normVec(srcB[0] - x, srcB[1] - y, sax)
    vax, vay = normVec(srcD[0] - x, srcD[1] - y, say)

    wb, hb = s - srcD[0], t - srcB[1]
    sbx, sby = wb / w_, hb / h_
    ubx, uby = normVec(srcB[0] - x, srcB[1] - y, sbx)
    vbx, vby = normVec(srcD[0] - x, srcD[1] - y, sby)

    ux = lambda p: (1 - p) * uax + p * ubx
    uy = lambda p: (1 - p) * uay + p * uby
    vx = lambda p: (1 - p) * vax + p * vbx
    vy = lambda p: (1 - p) * vay + p * vby

    if DEBUG:
        print("shape is from", wa, "x", ha, "to", wb, "x", hb)
        print("use base 1 (", uax, uay, ";", vax, vay, ")")
        print("and base 2 (", ubx, uby, ";", vbx, vby, ")")

    for j in range(h_):
        for i in range(w_):
            X = x + i*ux(py(j)) + j*vx(py(j))
            Y = y + i*uy(px(i)) + j*vy(px(i))
            r.append(srcImg.getpixel((X, Y)))

    img = Image.new(srcImg.mode, destSize)
    img.putdata(r)
    return img

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

    img = Image.new(srcImg.mode, srcImg.size)
    img.putdata(r)
    return img
