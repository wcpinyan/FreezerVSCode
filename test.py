from machine import Pin,PWM
from utime import sleep
print("done")

file=open("max.txt","w")
file.write("75")
sleep(5)
#file.flush()
print(file.read())