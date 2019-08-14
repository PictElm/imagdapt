import imagdapt as iap

class Point:
    """ a `Point` holds 2 coordinates `x` and `y`
    """
    def __init__(self, x=0, y=0):
        if isinstance(x, (tuple, list)):
            x, y = x
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"

    def get(self):
        return self.x, self.y

    @staticmethod
    def vect(a, b, mag=None):
        """ return the vector from `a` to `b`

            returns a `Point` object holding the coordinates of the
            vector from `a` to `b`
        """
        x, y = b.x - a.x, b.y - a.y
        if mag is None:
            return Point(x, y)
        l = mag / (x * x + y * y)**.5
        return Point(x * l, y * l)

    @staticmethod
    def assertIsPoint(value):
        """ asserts that `value` is a `Point`

            raises a `TypeError` if `value` is not instance of `Point`,
            otherwise returns it
        """
        if not isinstance(value, Point):
            raise TypeError("Not a Point.")
        return value

    @staticmethod
    def asCoordinates(*points):
        """ returns the lists of coordinates of the points

            returns two lists `X` and `Y` respectively containing the
            `.x` and `.y` coordinates of each points (in the order they
            are given)
        """
        X, Y = [], []
        for point in points:
            X.append(point.x)
            Y.append(point.y)
        return X, Y

    @staticmethod
    def between(a, b, ratio=.5):
        """ returns a new `Point` between `a` and `b`

            let `c` be the new point; the ratio of the distance from
            `a` to `c` and from `a` to `b` is equal to `ratio`
        """
        return Point(
            (1 - ratio) * a.x + ratio * b.x,
            (1 - ratio) * a.y + ratio * b.y
        )

    @staticmethod
    def intersect(a, b, c, d):
        """ returns a new `Point` at the intersection of the lines

            the returned point is on line 1 (defined by `a` and`b`)
            and on line 2 (by `c` and `d`)
        """
        r, s = Point.vect(a, b), Point.vect(c, d)
        z = r.x * s.y - r.y * s.x
        tmp1, tmp2 = Point.vect(a, c), Point(s.x / z, s.y / z)
        t = tmp1.x * tmp2.y - tmp1.y * tmp2.x
        return Point(a.x + t * (b.x - a.x), a.y + t * (b.y - a.y))

class Grid:
    """ a `Grid`  defines a 2-dimentional array of `Point`s

        the minimal size for a grid is 2x2

        a new `Grid` can be provided with all 4 corners as k-args:
        'topRight', 'topLeft', 'bottomRight' and 'bottomLeft'; they
        must be instances of `Point`
    """
    def __init__(self, w=2, h=None, **corners):
        self.w = w
        self.h = h or w

        if self.w < 2 or self.h < 2:
            raise IndexError(f"Invalid grid size of {w}x{h}: "
                + "the minimal size for a grid is 2x2.")

        self.points = [[None for k in range(self.h)] for k in range(self.w)]
        if corners:
            self.setCorners(
                corners['topLeft'],
                corners['topRight'],
                corners['bottomRight'],
                corners['bottomLeft']
            )

    def __repr__(self):
        return f"Grid({self.w}, {self.h})"

    def __str__(self):
        return f"({self.w}x{self.h})"

    def __getitem__(self, ij=None):
        if isinstance(ij, int):
            return self.points[ij]
        return self.points if ij is None else self.points[ij[0]][ij[1]]

    def __setitem__(self, ij=None, value=[]):
        if ij is None:
            if len(value) != self.w or len(value[0]) != self.h:
                raise IndexError(
                    f"The {len(value)}x{len(value[0])} array "
                    + "does not match this {self.w}x{self.h} Grid object."
                )
            for i in range(self.w):
                for j in range(self.h):
                    self.points[i][j] = Point.assertIsPoint(value[i][j])
        else:
            self.points[ij[0]][ij[1]] = Point.assertIsPoint(value)

    def __len__(self):
        return min(self.w, self.h)

    def setCorners(self, topLeft, topRight, bottomRight, bottomLeft):
        """ sets the corners of the grid

            all parameters must be instances of `Point`
        """
        self.points[0][0] = Point.assertIsPoint(topLeft)
        self.points[-1][0] = Point.assertIsPoint(topRight)
        self.points[-1][-1] = Point.assertIsPoint(bottomRight)
        self.points[0][-1] = Point.assertIsPoint(bottomLeft)

        return self

    def setRows(self, tops=None, rights=None, bottoms=None, lefts=None):
        """ sets the points of one of the border rows

            any given parameter must be a list of instances of `Point`
            and of matching length: the grid's width -2 for `tops` and
            `bottoms` or grid's height for `lefts` and `rights`
        """
        if tops is not None:
            for k in range(1, self.w - 1):
                self.points[k][0] = Point.assertIsPoint(tops[k - 1])

        if rights is not None:
            for k in range(1, self.h - 1):
                self.points[-1][k] = Point.assertIsPoint(rights[k - 1])

        if bottoms is not None:
            for k in range(1, self.w - 1):
                self.points[k][-1] = Point.assertIsPoint(bottoms[k - 1])

        if lefts is not None:
            for k in range(1, self.h - 1):
                self.points[0][k] = Point.assertIsPoint(lefts[k - 1])

        return self

    def complete(self, rows=False, fill=False):
        """ completes the grid with aligned points where missing

            if `rows` is true:
                places the missing points for each of the border rows
                (see `Grid.setRows`); the added points are placed using
                the `Point.between` function with the corner points
                and the ratio of the index and the width or height

            if `fill` is true:
                places the missing inner points (i.e. excluding border
                rows and corners); the added points are placed using
                the `Point.intersect` function with the corresponding
                points from each of the border rows

            returns `True` if the grid is completed i.e. every element
            is a valid instance of `Point`
        """
        if rows:
            def p(ia, ja, ib, jb, r):
                pa, pb = self.points[ia][ja], self.points[ib][jb]
                return Point.between(pa, pb, r)

            for k in range(1, self.w - 1):
                if not self.points[k][0]:
                    self.points[k][0] = p(0, 0, -1, 0, k / (self.w-1))

            for k in range(1, self.h - 1):
                if not self.points[-1][k]:
                    self.points[-1][k] = p(-1, 0, -1, -1, k / (self.h-1))

            for k in range(1, self.w - 1):
                if not self.points[k][-1]:
                    self.points[k][-1] = p(0, -1, -1, -1, k / (self.w-1))

            for k in range(1, self.h - 1):
                if not self.points[0][k]:
                    self.points[0][k] = p(0, 0, 0, -1, k / (self.h-1))

        if fill:
            def q(i, j):
                ai, bi = self.points[i][0], self.points[i][-1]
                aj, bj = self.points[0][j], self.points[-1][j]
                return Point.intersect(ai, bi, aj, bj)

            for i in range(1, self.w - 1):
                for j in range(1, self.h - 1):
                    if not self.points[i][j]:
                        self.points[i][j] = q(i, j)

        return (rows and fill or
                all([all(isinstance(p, Point) for p in l)]
                    for l in self.points))

    def getPlotQuad(self, n=0):
        return Point.asCoordinates(
            self.points[n][n],
            self.points[self.w - n - 1][n],
            self.points[self.w - n - 1][self.h - n - 1],
            self.points[n][self.h - n - 1],
            self.points[n][n]
        )

    def getPlotShape(self, n=0):
        """ returns the coordinates of the n-inner closed shape
        """
        return Point.asCoordinates(
            *([self.points[l][n] for l in range(n, self.w - n)]
            + [self.points[self.w - n - 1][l] for l in range(n + 1, self.h - n)]
            + [self.points[l][self.h - n - 1] for l in range(self.w - 2 - n, n - 1, -1)]
            + [self.points[n][l] for l in range(self.h - 2 - n, n - 1, -1)])
        )

    def bind(self, image, destSize):
        """ binds an image to the grid to uses extract on
        """
        self.target = destSize
        if self.complete():
            self.image = image
            return self
        return None

    def extract(self, mode=iap.MODE_LINE, transform=None):
        """ TODO
        """
        d = dir(self)
        assert 'image' in d and 'target' in d and self.complete()

        call = {
            iap.MODE_QUAD: iap.Extractor.extract,
            iap.MODE_LINE: iap.Extractor.extractLinear,
            iap.MODE_POLY: iap.Extractor.extractPolynomial
        }

        d = {}
        r = iap.time(lambda: call[mode](self, transform), d)
        iap.log('extract', "operation took", d['time'], "ns")
        return r
