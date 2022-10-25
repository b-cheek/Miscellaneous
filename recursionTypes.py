def tail(n, a):
    if n==1:
        return a
    return tail(n-1, a*n)

def tailRecursion(n):
    return tail(n, 1)

def normalRecursion(n):
    if n==0:
        return 1
    return n*normalRecursion(n-1)

num = 5
print(tailRecursion(num))
print(normalRecursion(num))
