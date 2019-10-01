# JrAppy

This was a reversing challenge from the bsidesdelhi 2019 CTF.

The only challenge provided us with one file only: [chall.py](chall.py), python bytecode.

I used [pycdc](https://github.com/zrax/pycdc) to decompile, and got [recover.py](recover.py).

In the check() function, we can see that the input string has to pass several constraints, in order to be valid.
I modeled these constraints using [python-constraint](https://labix.org/python-constraint), 
and got the first part of the flag: compilersXareXmoreXf (see [constr.py](constr.py)),
though "Correct! get the other part of the flag." alreay hinted that there is a second part.

The dump() function actually generates the second part of the challenge, a Java class file.
I have not spent a whole lot of time reversing it.
The idea was the same, though this time the constraint got a little bit more complicated.

Luckily, I could [guess](constr2.py) parts of the second part (i.e. starting with "un"), and so there were only ~3000 possibilites left.
I printed out all of them and quickly found the [solution](flag_part2.png).

All in all a sighlty tedious challenge, although I had fun solving it nevertheless.