def do_something_with(line):
    with open("/Users/alessandrozonta/PycharmProjects/roadNetwork/data/TheHagueSmall.graphml", "a") as myfile:
        myfile.write(line)


count = 0
with open("/Users/alessandrozonta/PycharmProjects/roadNetwork/data/TheHague.graphml") as fileobject:
    for line in fileobject:
        count += 1
        print count
        if not "<data key=\"d9\">" in line and not "<data key=\"d10\">" in line and not "<data key=\"d8\">" in line and not "<data key=\"d12\">" in line and not "<data key=\"d13\">" in line and not "<data key=\"d14\">" in line and not "<data key=\"d15\">" in line and not "<data key=\"d16\">" in line and not "<data key=\"d17\">" in line and not "<data key=\"d18\">" in line and not "<data key=\"d19\">" in line and not "<data key=\"d20\">" in line and not "<data key=\"d21\">" in line and not "<data key=\"d22\">" in line:
            do_something_with(line)
