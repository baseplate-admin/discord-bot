import os
def function():
    while True:
        for i in os.listdir("./LoopQueue"):
            print(i)

function()