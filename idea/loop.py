import os
DIR = os.path.abspath(os.path.realpath("./idea/LoopQueue"))
first_file = os.listdir(DIR)[-1]

print(first_file.strip(".txt"))