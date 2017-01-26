def fmtTime(hrmin):
    print "at 0: " + str(hrmin[0])
    print "at 1: " + str(hrmin[1])
    if hrmin[0] == 0:
        return "12:%02d AM" % hrmin[1]
    if hrmin[0] < 12:
        return "%d:%02d AM" % (hrmin[0], hrmin[1])
    if hrmin[0] == 12:
        return "12:%02d PM" % hrmin[1]
    return "%d:%02d PM" % (hrmin[0] - 12, hrmin[1])

