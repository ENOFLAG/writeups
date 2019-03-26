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

Apart from this, the program takes

## Decompiled trees
