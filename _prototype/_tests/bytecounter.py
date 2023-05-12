bytes = ["ążęźćńół", "abcdefgh", "aą", "ąa", "aa", "ąą"]

for b in bytes:
    print("%s %s" % (b, len(b.encode("utf-8"))))
