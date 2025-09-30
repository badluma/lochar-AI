import time

loading_animation = ["–", "/", "|", "\\"]

while True:
    for i in loading_animation:
       print(i + "\r", end="")
       time.sleep(0.1)