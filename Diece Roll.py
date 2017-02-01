__author__ = 'jidziak'
import random


def rzuc_kostka():
    return random.randint (1, 6)


def gra_w_kosci():
    x1, x2 = rzuc_kostka(), rzuc_kostka()
    if x1 == x2:
        return x1, x2, "remis"
    else:
        return x1, x2, x1>x2


def cykl_gier(n):
    wynik = [0,0]
    for i in range(0,n):
        x = gra_w_kosci()
    if x[2] != "remis":
        wynik[1-(x[0]>x[1])*1]+=1
    print(x[0], x[1], wynik)

cykl_gier(5)
