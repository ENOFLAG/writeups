# Fault Box

We have an online service, where we can
1. get the encrypted flag
2. get an encrypted fake-flag
3. get an faulty encryption of the fake-flag
4. encrypt an arbitrary message
all with RSA, e = 65537 but *unknown n*.

After executing 2 of the first 3 options, the key is reset.
Only the 4th we can perform arbitrarily (within 5 minutes).

## Getting n

* Input some small messages *a_i* (e.g. '0' and '1', i.e. 0x30 and 0x31) get cipher *b_i*
* We have *a_i ^ e = b_i + k_i * n*
* Compute gcd of the *a_i ^ e - b_i* (that's why *a_i* should be small)
Most likely the gcd will be *n*.
To increase the chance, you can add a third message.

## Factor n

The faulty encryption is like the improved RSA encryption via Chinese Remainder Theorem (CRT), but at one step, some small number is added.
As a result, *p* divides *fake - faulty_fake*, so *p = gcd(n, fake - faulty_fake)*

Unfortunately, this need 2 calls, and when we ask for the encrypted flag, the key is reset.

## Save a Function Call

It turns out, we don't have to call the second function.
We only use the function calls 4,4,3,4,...,4,1.
When generating the key, the server computes
* `base_p = random`
* `p = next_prime(base_p)`
* `x = p - base_p`
and likewise `q,y`.
The fake flag is `y`, which is ~ln(n) ~ 1000-1500.
We just try out all values (before we ask for the encrypted flag), and then check for each guess, whether the above method works.
If it fails, just try again, the chances are good (Trying y = 0,...,500 took 3 or 4 attempts).

## Alternative Approach

The seed for random is `time.time()`, which is seconds since Epoch.
By default, it is a float, but might be int.
With the primes and the offsets, we could guess the initial seed, then we can compute the new key after the reset.
