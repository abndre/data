# main.py
from math import sqrt

def baskara(a,b,c):
    delta = (b**2) - 4*a*c
    
    if delta < 0:
        return False
    
    x1 = (-1*b + sqrt(delta))/(2*a)
    x2 = (-1*b - sqrt(delta))/(2*a)

    return [x1,x2]

def main(a,b,c):
    result = baskara(a,b,c)

    if not result:
        print("SEM RAIZES")
        return

    print("RAIZ 1: {}".format(result[0]))
    print("RAIZ 2: {}".format(result[1]))

if __name__ == "__main__":
    main(1,12,-13)
