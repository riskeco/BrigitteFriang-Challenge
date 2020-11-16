def condition(n):
    if (n*n*n)%8387!=573:
        return False
    if (n*n*n)%9613!=98:
        return False
    if (n*n*n)%7927!=2726:
        return False
    return True

i = 0
while not condition(i):
    i+=1
print(i)
