# Count on me

The server asks for a seed and then returns the encrypted flag 100 times.

The service then generated blocks of 32 Bits, expands them to 16 Bytes and encrypts these with AES-128 with unknown key in ECB mode, i.e. same input leads to same cipher.
This bitstream then is XORed with: "Encrypted Flag: " + FLAG

Observations:
* "Encrypted Flag: " has 16 Byte, i.e. one full block.
* The encrypted string has 48 Byte, so 3 blocks.
* We have control over the seed.

We know, which random bytes were encrypted and we know the plaintext of the first block, we know to which 16 bytes, these were encrypted.
So for some blocks, we know the cipher.
Now we have to find a seed, such that some random bits from the first block also appears as a second block (possibly in one of the other other 99 iterations).
The same we do for the third blocks.
We can do this in an offline search.
Similar to the birthday paradox, the chances are good, actually both seeds are ~77k.
