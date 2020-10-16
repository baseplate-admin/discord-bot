import os
def check_loop():
    loopqueuenumer = 0
    for i in range(0,len(os.listdir(os.path.realpath("./LoopQueue")))):
        print("hello")
        loopqueuenumer += 1
        
check_loop()