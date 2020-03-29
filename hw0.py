import functools
import random
import re

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def show(self):
        print("my location is ("+str(self.x)+","+str(self.y)+")")

def sum(num_string):
    list = num_string.split('.')
    return int(list[0])+int(list[1])





if __name__ == '__main__':

       print(sum("-4.5"))
       print("bye")
