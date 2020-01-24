# RuCTFe 2019 -- Profile

## Description

A small webservice to store messages and the possibility to retrieve them if you know the correct signature.
Actually, there are two different algorithms for the signature.
You can:
* Enter user and message and get
** the user's public key
** the message hash
** the message's signature
* get all users
* for a user get all message hashes
* enter user, message hash and signature to get message (flag)

## Exploit -- Empty Signature

Method "stop" always accepts the empty signature.

    def verify(self, msg, pub, sign):
        sign = split_signature(sign, 32)
        return all(x == n_hash(y, sha256, 2**self._w - 1 - z) for x,y,z in zip(pub, sign, split_message(msg, 8, 18)))

Fix: Just decline empty signature.

## Exploit -- Forge Trivial Signature

Theoretically, we use RLWE (Ring Learning with Error -- Learning with error over a polynomial ring).
But it is wrongly implemented, and has terrible parameters.

    def verify(self, msg, pub, sign):
        msg = np.array(list(msg))
        pub, a = map(np.array, pub)
        c, z1, z2 = map(np.array, sign)
        return all(c == ((a*z1 + z2 - pub*c) + msg) % self.q)

We can just use
* c = 0
* z1 = 0
* z2 = q - msg

Fix: Decline `c = 0`

## Exploit -- Retrieve Private Key

The message-hash `msg` has 16 Bytes (split into 18 parts of 8 Bit, 0-padded), the private key 18 Int64.
Entry `priv[i]` is hashed `msg[i]` times.

* The last two entries aren't hashed.
* If our message hash contains 0-Byte, that entry is not hashed.

Code is:

    def sign(self, msg, priv):
        signature = [n_hash(x, sha256, y) for x, y in zip(priv, split_message(msg, 8, 18))] 
        return join_signature(signature)

For index `i` create random words, until you find one with `msg[i] = 0`.
Can be done offline.
Then send all of these words, get them signed.
We can put together the private key and can sign arbitrary messages.

***This exploit is hardly distinguishable from normal traffic.***
