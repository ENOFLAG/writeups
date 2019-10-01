import collections
from constraint import *

problem = Problem()

for i in range(21):
    if i not in [2, 7, 20]:
        problem.addVariable(chr(97 + i), [x for x in range(97, 123)])
    else:
        problem.addVariable(chr(97 + i), [x for x in range(65, 91)])

problem.addConstraint(lambda a: a == 117, ("a"))
problem.addConstraint(lambda b: b == 110, ("b"))

problem.addConstraint(lambda c: c == 88, ("c"))
problem.addConstraint(lambda h: h == 88, ("h"))
problem.addConstraint(lambda u: u == 88, ("u"))

problem.addConstraint(lambda d: d == 116, ("d"))
problem.addConstraint(lambda e: e == 104, ("e"))
problem.addConstraint(lambda f: f == 97, ("f"))
problem.addConstraint(lambda g: g == 110, ("g"))

zz = [29, 22, 19, 7, 5, -17, 9, 15, 0, -2, -10, 5, 26, 27]

problem.addConstraint(lambda a, c: a - c == zz[0], ("a", "c"))
problem.addConstraint(lambda b, c: b - c == zz[1], ("b", "c"))

problem.addConstraint(lambda d, f: d - f == zz[2], ("d", "f"))
problem.addConstraint(lambda e, f: e - f == zz[3], ("e", "f"))

problem.addConstraint(lambda g, i: g - i == zz[4], ("g", "i"))
problem.addConstraint(lambda h, i: h - i == zz[5], ("h", "i"))

problem.addConstraint(lambda j, l: j - l == zz[6], ("j", "l"))
problem.addConstraint(lambda k, l: k - l == zz[7], ("k", "l"))

problem.addConstraint(lambda m, o: m - o == zz[8], ("m", "o"))
problem.addConstraint(lambda n, o: n - o == zz[9], ("n", "o"))

problem.addConstraint(lambda p, r: p - r == zz[10], ("p", "r"))
problem.addConstraint(lambda q, r: q - r == zz[11], ("q", "r"))

problem.addConstraint(lambda s, u: s - u == zz[12], ("s", "u"))
problem.addConstraint(lambda t, u: t - u == zz[13], ("t", "u"))


aa = problem.getSolutions()
abc = open("lmao", "w")
for a in aa:
    for i in collections.OrderedDict(sorted(a.items())).values():
        print(chr(i), end="")
        abc.write(chr(i))
    print("")
    abc.write("\n")

print(len(aa))

ca = [196, 225, 210, 200, 214, 219, 215, 215, 203, 190]
cx = [2, 29, 8, 40, 4, 3, 23, 23, 43, 62]
caa = [210, 221, 213, 215, 203, 211, 189, 220, 215, 190]
