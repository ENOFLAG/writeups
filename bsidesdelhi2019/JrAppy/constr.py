import collections
from constraint import *

problem = Problem()

for i in range(20):
    if i not in [9, 13, 18]:
        problem.addVariable(chr(97 + i), [x for x in range(97, 123)])
    else:
        problem.addVariable(chr(97 + i), [x for x in range(65, 91)])

caa = [210, 221, 213, 215, 203, 211, 189, 220, 215, 190]
# ord(str1[i]) + ord(str1[(i + 1)]) != caa[int(i / 2)]

problem.addConstraint(lambda a, b: a + b == caa[0], ("a", "b"))
problem.addConstraint(lambda c, d: c + d == caa[1], ("c", "d"))
problem.addConstraint(lambda e, f: e + f == caa[2], ("e", "f"))
problem.addConstraint(lambda g, h: g + h == caa[3], ("g", "h"))
problem.addConstraint(lambda i, j: i + j == caa[4], ("i", "j"))
problem.addConstraint(lambda k, l: k + l == caa[5], ("k", "l"))
problem.addConstraint(lambda m, n: m + n == caa[6], ("m", "n"))
problem.addConstraint(lambda o, p: o + p == caa[7], ("o", "p"))
problem.addConstraint(lambda q, r: q + r == caa[8], ("q", "r"))
problem.addConstraint(lambda s, t: s + t == caa[9], ("s", "t"))

ca = [196, 225, 210, 200, 214, 219, 215, 215, 203, 190]

problem.addConstraint(lambda a, k: a + k == ca[0], ("a", "k"))
problem.addConstraint(lambda b, l: b + l == ca[1], ("b", "l"))
problem.addConstraint(lambda c, m: c + m == ca[2], ("c", "m"))
problem.addConstraint(lambda d, n: d + n == ca[3], ("d", "n"))
problem.addConstraint(lambda e, o: e + o == ca[4], ("e", "o"))
problem.addConstraint(lambda f, p: f + p == ca[5], ("f", "p"))
problem.addConstraint(lambda g, q: g + q == ca[6], ("g", "q"))
problem.addConstraint(lambda h, r: h + r == ca[7], ("h", "r"))
problem.addConstraint(lambda i, s: i + s == ca[8], ("i", "s"))
problem.addConstraint(lambda j, t: j + t == ca[9], ("j", "t"))

# if ord(str1[i]) ^ ord(str1[(i + 10)]) != cx[i]:
cx = [2, 29, 8, 40, 4, 3, 23, 23, 43, 62]

problem.addConstraint(lambda a, k: a ^ k == cx[0], ("a", "k"))
problem.addConstraint(lambda b, l: b ^ l == cx[1], ("b", "l"))
problem.addConstraint(lambda c, m: c ^ m == cx[2], ("c", "m"))
problem.addConstraint(lambda d, n: d ^ n == cx[3], ("d", "n"))
problem.addConstraint(lambda e, o: e ^ o == cx[4], ("e", "o"))
problem.addConstraint(lambda f, p: f ^ p == cx[5], ("f", "p"))
problem.addConstraint(lambda g, q: g ^ q == cx[6], ("g", "q"))
problem.addConstraint(lambda h, r: h ^ r == cx[7], ("h", "r"))
problem.addConstraint(lambda i, s: i ^ s == cx[8], ("i", "s"))
problem.addConstraint(lambda j, t: j ^ t == cx[9], ("j", "t"))

# if ord(str1[7]) ^ ord(str1[8]) != 1:
problem.addConstraint(lambda h, i: h ^ i == 1, ("h", "i"))


aa = problem.getSolutions()


for a in aa:
    od = collections.OrderedDict(sorted(a.items()))

    for i in [99, 111, 109, 112, 105, 108, 101, 114, 115, 88, 97, 114, 101, 88, 109, 111, 114, 101, 88, 102]:
        print(chr(i), end="")

    print("")


ca = [
    196,
    225,
    210,
    200,
    214,
    219,
    215,
    215,
    203,
    190]
cx = [
    2,
    29,
    8,
    40,
    4,
    3,
    23,
    23,
    43,
    62]
caa = [
    210,
    221,
    213,
    215,
    203,
    211,
    189,
    220,
    215,
    190]
