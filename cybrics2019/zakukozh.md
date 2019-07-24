# Zakukozh

The hint says affine chiffre, which means x -> a*x+b and a is coprime to the modulus (here 256, so a simply is odd).
We can brute-force this, about 2**15 ~ 32k choices.

Then sort all files by filetype.
Remove all, that are binary (i.e. don't match a signature).
Then only few remain, actually only one of them has a preview in Nemo.
That is the image with the flag.
