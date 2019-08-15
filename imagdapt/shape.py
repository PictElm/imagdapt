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
        """ returns `"Point({x}, {y})"`
        """
        return f"Point({self.x}, {self.y})"

    def __str__(self):
        """ produce a string representation of the point

            ```
                ({x.3f}, {y.3f})
        """
        return f"({round(self.x, 3)}, {round(self.y, 3)})"

    def get(self):
        """ returns the coordinates as a tuple `(x, y)`
        """
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
    def assertIsPoint(value, orNone=True):
        """ asserts that `value` is a `Point`

            raises a `TypeError` if `value` is not instance of `Point`,
            otherwise returns the point

            if `orNone` is true (by default) and `value` is
            `None`, no error occurs and `None` is returned
        """
        if orNone:
            if value is None or isinstance(value, Point):
                return value
            raise TypeError("Not a Point.")

        if isinstance(value, Point):
            return value
        raise TypeError("Not a Point.")

    @staticmethod
    def asCoordinates(*points):
        """ returns the lists of coordinates of the points

            returns two lists `X` and `Y` respectively containing the
            `.x` and `.y` coordinates of each point (in the order where
            are given)
        """
        X, Y = [], []
        for point in points:
            X.append(point.x)
            Y.append(point.y)
        return X, Y

    @staticmethod
    def between(a, b, ratio=.5):
        """ returns a new `Point` standing between `a` and `b`

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
    """ a `Grid` defines a 2-dimentional array of `Point`s

        the minimal size for a grid is 2x2

        a new `Grid` can be provided with all 4 corners as kwargs:
        'topRight', 'topLeft', 'bottomRight' and 'bottomLeft'; they
        must be instances of `Point` (and cannot be `None`)
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
        """ returns `"Grid({w}, {h})"`
        """
        return f"Grid({self.w}, {self.h})"

    def __str__(self):
        """ produce a string representation of the full grid

            ```
                {w}x{h}: [
                    [ {points[0, 0]}, .. ],
                    [ .. ]
                ]
            ```
        """
        grid = " ],\n\t[ ".join([
            ", ".join([
                str(self[i, j])
            for i in range(self.w)])
        for j in range(self.h)])

        return f"{self.w}x{self.h}: [\n\t[ {grid} ]\n]"

    def __getitem__(self, ij=None):
        """ gets the point at (i, j) with `i, j = ij`

            if `ij` is `None`, returns the entire grid of points

            if `ij` is an integer, returns the corresponding column so
            that both calls produce the same output:
            ```python
                print(grid[i, j])
                print(grid[i][j])
            ```
        """
        if ij is None:
            return self.points
        if isinstance(ij, int):
            return self.points[ij]
        return self.points if ij is None else self.points[ij[0]][ij[1]]

    def __setitem__(self, ij=None, value=None):
        """ sets `value` at (i, j), with `i, j = ij`

            if `ij` is `None` and `value` is a table the same size
            as the gide, updates the entire grid with the given points
        """
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
        """ returns the smallest dimensions of the grid

            min of its width and height
        """
        return min(self.w, self.h)

    def setCorners(self, topLeft, topRight, bottomRight, bottomLeft):
        """ sets the corners of the grid

            all parameters must be instances of `Point` (and cannot be
            `None`)
        """
        self.points[0][0] = Point.assertIsPoint(topLeft, False)
        self.points[-1][0] = Point.assertIsPoint(topRight, False)
        self.points[-1][-1] = Point.assertIsPoint(bottomRight, False)
        self.points[0][-1] = Point.assertIsPoint(bottomLeft, False)

        return self

    def setRows(self, tops=None, rights=None, bottoms=None, lefts=None):
        """ sets the points of one of the border rows

            any given parameter must be a list of instances of `Point`
            and of matching length: the grid's width - 2 for `tops` and
            `bottoms` or grid's height - 2 for `lefts` and `rights`
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

    # TODO: try to use as many already-set points when aligning
    def complete(self, rows=False, fill=False):
        """ completes the grid with aligned points where missing

            if `rows` is true:
                places the missing points for each of the border rows
                (see `Grid.setRows`); the added points are placed using
                the `Point.between` function with the the closest
                defined (i.e. non-`None`) points on the same row: if a
                point has be set on the row, it will likely be used
                instead of the corner to ensure a straight line (I hope
                you get the point...)

            if `fill` is true:
                places the missing inner points (i.e. excluding border
                rows and corners); the added points are placed using
                the `Point.intersect` function with the corresponding
                points from the border rows

            returns `True` if the grid is completed i.e. every element
            is a valid instance of `Point`
        """
        if rows:
            def g(i, j, di, dj):
                """
                (i_, j_) of first non-`None` points starting from
                (i, j) and moving by (di, dj)
                """
                i+= di
                j+= dj
                while self[i, j] is None:
                    i+= di
                    j+= dj
                return i, j

            def p(i, j, di, dj):
                """
                point between the first non-`None` from (i, j)
                moving by (di, dj) and the first non-`None` from
                (i, j) moving by (-di, -dj)
                """
                ija, ijb = g(i, j, di, dj), g(i, j, -di, -dj)
                if di:
                    r = abs(ija[0] - i) / abs(ija[0] - ijb[0])
                else:
                    r = abs(ija[1] - j) / abs(ija[1] - ijb[1])
                return Point.between(self[ija], self[ijb], r)

            for k in range(1, self.w - 1):
                if not self.points[k][0]:
                    self.points[k][0] = p(k, 0, 1, 0)

                if not self.points[k][-1]:
                    self.points[k][-1] = p(k, -1, 1, 0)

            for k in range(1, self.h - 1):
                if not self.points[0][k]:
                    self.points[0][k] = p(0, k, 0, 1)

                if not self.points[-1][k]:
                    self.points[-1][k] = p(-1, k, 0, 1)

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
        """ returns the coordinates of the n-inner closed quadrilateral
        """
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
            *([self.points[l][n] for l in range(n, self.w-n)]
            + [self.points[self.w-n-1][l] for l in range(n+1, self.h-n)]
            + [self.points[l][self.h-n-1] for l in range(self.w-2-n, n-1, -1)]
            + [self.points[n][l] for l in range(self.h-2-n, n-1, -1)])
        )

    def bind(self, image, destSize):
        """ binds an image to the grid and set the expected result size
        """
        self.target = destSize
        if self.complete():
            self.image = image
            return self
        return None

    def extract(self, mode=iap.MODE_LINE, transform=None):
        """ apply the extraction algorithm designed by the chosen mode

            `mode` should be one of the value defined by the `imagdapt`
            module:
                - `MODE_QUAD`
                - `MODE_LINE`
                - `MODE_POLY`

            if a `transform` function is provided, it will be called
            for each pixel and its result will be applied instead of
            the pixel itself
        """
        d = dir(self)
        assert 'image' in d and 'target' in d and self.complete()

        calls = {
            iap.MODE_QUAD: iap.Extractor.extractQuadrilateral,
            iap.MODE_LINE: iap.Extractor.extractLinear,
            iap.MODE_POLY: iap.Extractor.extractPolynomial
        }

        timingResult = {}
        r = iap.time(lambda: calls[mode](self, transform), timingResult)
        iap.log('extract', "operation took", timingResult['time'] / 1e9, "s")
        return r
