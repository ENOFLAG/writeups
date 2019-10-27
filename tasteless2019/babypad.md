# Babypad

Author: plonk

Category: cry

Solves: 51

We heard this kind of enription is super securr, so we'll just give you the flag encripted!

## Challenge

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

int main() {
    char *plaintext = NULL;
    char *one_time_pad = NULL;
    char *ciphertext = NULL;
    size_t flag_length = 0;
    FILE *flag = fopen("flag.txt", "r");
    FILE *urandom = fopen("/dev/urandom", "r");
    assert(flag && urandom);

    /*
     * Get flag length, and allocate memory for the plaintext,
     * one-time pad and ciphertext.
     */
    fseek(flag, 0, SEEK_END);
    flag_length = ftell(flag);
    rewind(flag);

    plaintext = malloc(flag_length + 1);
    one_time_pad = malloc(flag_length + 1);
    ciphertext = malloc(flag_length + 1);
    assert(plaintext && one_time_pad && ciphertext);

    /* Read the plaintext and the one-time-pad */
    fread(plaintext, flag_length, 1, flag);
    fread(one_time_pad, flag_length, 1, urandom);
    plaintext[flag_length] = '\0';
    one_time_pad[flag_length] = '\0';

    /* Make sure that the one-time-pad isn't too short. */
    assert(strlen(plaintext) == strlen(one_time_pad));

    for (int i = 0; i < flag_length; i++) {
        ciphertext[i] = plaintext[i] ^ one_time_pad[i];
    }

    fwrite(ciphertext, flag_length, 1, stdout);
    return 0;
}
```

## Solution

We first started analyzing this rather small challenge. 

This challenge essentially does 4 things:

1. Read the flag

```c
// ...

FILE *urandom = fopen("/dev/urandom", "r");

// ...

fseek(flag, 0, SEEK_END);
flag_length = ftell(flag);
rewind(flag);

plaintext = malloc(flag_length + 1);

// ...

fread(plaintext, flag_length, 1, flag);
plaintext[flag_length] = '\0';
```
2. Generate a One Tme Pad the same exact length of the flag

```c
// ...

FILE *urandom = fopen("/dev/urandom", "r");

// ...

one_time_pad = malloc(flag_length + 1);
fread(one_time_pad, flag_length, 1, urandom);
one_time_pad[flag_length] = '\0';

/* Make sure that the one-time-pad isn't too short. */
assert(strlen(plaintext) == strlen(one_time_pad));
```

3. XOR the flag with the OTP

```c
for (int i = 0; i < flag_length; i++) {
    ciphertext[i] = plaintext[i] ^ one_time_pad[i];
}
```

4. Print the cipher text

```c
fwrite(ciphertext, flag_length, 1, stdout);
```

Now this isn't exactly a big attack surface. 
We assumed that `/dev/urandom` is actually random enough so there is no attacking the randomness.

The important part of this challenge is that the length of the OTP is checked against the length of the plaintext. Because of how `strlen` works in C, the OTP can not include a null byte. If the random OTP does contain a null byte the `strlen` will terminate the string there, the lengths wouldn't match and the assert would stop execution.

```c
assert(strlen(plaintext) == strlen(one_time_pad));
```

Armed with the knowledge that the OTP can't contain a null byte we can look at the XOR. 
Because of that crucial fact we know one thing about the cipher text. 
For each byte in the cipher text the byte can't be the same as the one at the same position in the flag.

The only way to get the original byte of the flag in the cipher text, the OTP would have had to be a null byte because `X ^ 0 = X`.
So to get the flag we now have to request so many cipher texts until we have eliminated all but one byte for each byte in the flag.

## Script

```python
from pwn import *
from IPython import embed
from string import printable

host = "hitme.tasteless.eu"
port = 10401

m = []
for x in range(37): # len(flag) == 37
    m.append({ord(x) for x in printable})

def get():
    io = remote(host, port)
    ret = io.recvall()
    io.close()
    return ret

def do_work(n):
    for x in range(n):
        g = get()
        for k, v in enumerate(g):
            if v in m[k]:
                m[k].remove(v)

while not all(map(lambda x: len(x)==1, m)):
    do_work(100)

print("".join([chr(list(x)[0]) for x in m]))

"""
tctf{p1z_us3:4ll-t3h_by7e5>0n3_tim3}
"""
```