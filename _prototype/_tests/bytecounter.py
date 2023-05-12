bytes = ["ążęźćńół", "abcdefgh", "aą", "ąa", "aa", "ąą","塾の手紙","の","紙","補習班","習","班"]

for b in bytes:
    print("%s %s" % (b, len(b.encode("utf-8"))))
