# Sanitize

Decompiling with Ghidra *(domenukk: "I would never")* a CTF Challenge.

![Ghidra](ghidra.png)

## Intro

Sanitize was a reversing challenge at the 2019 0ctf with 282 points and 29 solves. 

## Reversing

The first thing we noticed was that the whole binary was scattered with a function that merely increments an int at the given memory location.

![Increment Function](increment.png)

It's literally everywhere, however always with a different memory location.
We figured out, at some point, that it's some sort of instrumentation, indicating which branches were taken - and how often.

Apart from this, the binary didn't print any output at the start -- apart from "Invalid" -- so the first thing was to analyze what kind of input the binary wanted.

The general sequence of events was:
1. Input a string of length < than 32
2. Input a number n
3. Input n numbers
4. Get some kind of output

![Sequence of Events](ServiceInteraction.png)

For this sequence to work the binary required a file called flag, and it used the numbers as indexes from where to read.

The output was a dump of the memory that was incremented during the flow of the program.

## Decompiled trees

We tried to reason what the program did to our input, because it wasn't particularly obvious.
The binary first created an empty tree, to which it appended our input character by character. After that it appended the n characters of the flag at the indexes we specified.

So we tried to figure out how the tree exactly behaved and how it responded input. Weirdly enough new nodes were always appended at the root of the tree, and it had some kind of self balancing. When balancing the nodes with higher values should go to the 2nd branch -- but it wasn't particularly obvious from the counters, or from the debugger we used on the decompiled code.

To better wrap our head around how chars could be deducted from the counters, we added a bit of functionality to the decompiled C Code which printed the tree after every added character.

There were some counters which were in the *"sorting"* algorithm of the tree that seemed particularly interesting, however we failed to deduct a straightforward relationship between the counter and the characters we were interested in.


## From counter-dump to Hash function 

Firstly YES, these counters aren't a good hash function in itself, since they weren't particularly collision resistant, since the binary only ever compared two values to decide its path on where to go next. That meant using the same "base tree" (the first 32 Characters inputted) the character sequence "aaab" and "aaac" were probably indistinguishable in most of the cases.

However if the right base tree was used "aaab" would end up with slightly different counter values based upon the *"sorting"*.
That meant using the same unknown char sequence on *enough* base trees, they would differ in some of them.

Thinking we would need to create a rainbow table 
