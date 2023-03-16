# n = int(input())
def pole (n):
    for i in range (n):
        for j in range (n-1):
            print (" ", end = '')
        print ('* * *')
def triangle (n):
    for i in range (n):
        for j in range (n-i):
            print (" ", end = '')
        for k in range (2*i+1):
            print ('*',end =' ')
        print ()

triangle(5)
# triangle(n)
# pole(n)