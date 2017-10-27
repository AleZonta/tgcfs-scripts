count = 0
with open("/Users/alessandrozonta/PycharmProjects/roadNetwork/data/Rijswijk5.graphml") as fileobject:
    for line in fileobject:
        count += 1
        print count
        