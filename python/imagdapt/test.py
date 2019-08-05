DEBUG = True
PAUSE = False
TESTS = "2" # None for all tests
SAVES = True
SHOWS = False
STAGES = (False, True) # (masked, extract)


import imagdapt as iap
iap.debug(DEBUG)

locations = { # maps pre-calculated locations for the available test pictures
    "1": [ (220, 90), (760, 128), (775, 380), (230, 300) ],
    "2": [ (722, 555), (904, 523), (901, 562), (719, 596) ]
}

if __name__ == '__main__' and (SAVES or SHOWS):
    for n in TESTS or locations:
        print("Test number", n)

        if DEBUG: print(" --- open ---------------------------------------")
        a, b, c, d = locations[n]
        img = iap.open("./test/"+n+"/picture.jpg")

        if STAGES[0]:
            if DEBUG: print(" --- mask ---------------------------------------")
            msk = iap.masked(img, a, b, c, d, maskColor=(0, 255, 0))
            if SAVES: msk.save("./test/"+n+"/masked.jpg")
            if SHOWS: msk.show

        if STAGES[1]:
            if DEBUG: print(" --- extract ------------------------------------")
            ext = iap.extract(img, a, b, c, d, destSize=(800, 200))
            if SAVES: ext.save("./test/"+n+"/extracted.jpg")
            if SHOWS: ext.show()

        (input if PAUSE else print)("...")
