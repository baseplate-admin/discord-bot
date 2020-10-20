import os
while True:
    for files in os.listdir("./LoopQueue"):
        if files.endswith('.mp3'):
            print(files)