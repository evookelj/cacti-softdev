def fmtTime(hrmin):
    if hrmin[0] == 0:
        return "12:%02d AM" % hrmin[1]
    if hrmin[0] < 12:
        return "%d:%02d AM" % (hrmin[0], hrmin[1])
    return "%d:%02d PM" % (hrmin[0] - 12, hrmin[1])

