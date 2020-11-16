with open("bits","r") as f:
    lines = f.readlines()
    for line in lines:
        a = line.rstrip()[:8]
        b = line.rstrip()[8:]
        print(chr(int(a,2))+chr(int(b,2)), end="")
    print("")
