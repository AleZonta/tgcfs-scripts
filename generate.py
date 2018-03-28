from random import *

repetitions = 20

versions = 9
random_numbers = []

for i in range(repetitions * versions):
    random_numbers.append(randint(1, 10000))

for i in range(repetitions):
    print("tgcfs-nn-Five-Neurons-Five-I " + str(i) + " 3 8.0 25 1 5 5 " + str(random_numbers[i + repetitions * 0]))
for i in range(repetitions):
    print("tgcfs-nn-Five-Neurons-Eight-I " + str(i) + " 3 8.0 25 1 5 8 " + str(random_numbers[i + repetitions * 1]))
for i in range(repetitions):
    print("tgcfs-nn-Five-Neurons-Ten-I " + str(i) + " 3 8.0 25 1 5 10 " + str(random_numbers[i + repetitions * 2]))
for i in range(repetitions):
    print("tgcfs-nn-Five-Neurons-Five-G " + str(i) + " 4 21.0 25 1 5 5 " + str(random_numbers[i + repetitions * 3]))
for i in range(repetitions):
    print("tgcfs-nn-Five-Neurons-Eight-G " + str(i) + " 4 21.0 25 1 5 8 " + str(random_numbers[i + repetitions * 4]))
for i in range(repetitions):
    print("tgcfs-nn-Five-Neurons-Ten-G " + str(i) + " 4 21.0 25 1 5 5 " + str(random_numbers[i + repetitions * 5]))
for i in range(repetitions):
    print("tgcfs-nn-Five-Neurons-Five-ETH " + str(i) + " 5 3.0 25 1 5 10 " + str(random_numbers[i + repetitions * 6]))
for i in range(repetitions):
    print("tgcfs-nn-Five-Neurons-Eight-ETH " + str(i) + " 5 3.0 25 1 5 8 " + str(random_numbers[i + repetitions * 7]))
for i in range(repetitions):
    print("tgcfs-nn-Five-Neurons-Ten-ETH " + str(i) + " 5 3.0 25 1 5 10 " + str(random_numbers[i + repetitions * 8]))
