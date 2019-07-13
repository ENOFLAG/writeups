# python-foo

python-foo was a tiny cli key-value store written in python, backed by a mongodb. It offered the commands `encrypt`, `decrypt`, `store` and `retrieve`.

After a successful store, you received a random id, which you could supply in retrieve.

The service's crypto module's source code was not deployed, however throwing its .pyc file into your python decompiler of choice yielded only slightly obfuscated source code.

## Vulnerability 1: Backdoor

The crypt module was imported with `from crypto import *`, so all global names from that file were imported. Among the many useless statements, there was
```python
int = iaa
```

and

```python
def iaa(*args, **kwargs):
    if args:
        if args[0] == caisheoquaMeeth6wo5waa4Eefaigh(iaa, b'SECRET', 'TOP'):
            print('so boring!')
        return -42
    else:
        return o_int(*args, **kwargs)

def caisheoquaMeeth6wo5waa4Eefaigh(a: int, b: bytes, c: str) -> str:
    a = 1
    b = bytes([(i + a * i // 10 + 7 ^ o_int(a * 3.1415)) % 10 + 48 for i in range(2, 30)])
    c = b.decode()
    return c
```

So in troll.py, `int` returned -42 if the argument was `0985432976321076540985432987`. This caused the `debug` function to leak `RECORDS`, which contained all encrypted values, which you could decrypt with the `decrypt` function.
```
def debug(op: int):
    print('operation: ', op)
    print('Global variables:')
    print('\n'.join(
        f'{k}: {v}'
        for k, v in globals().items()
        # make sure that we do not leak the key
        if k.isupper() and k != 'KEY'))
```
Removing the debug function fixes this issue.



## Vulnerability 2: Badlock
Since the storage was backed by a simple file, and socat spawned a python process for every connection (what could **possibly** go wrong on 512MB memory vulnboxes), python-foo had to use custom synchronization to protect the file from concurrent access.

The `store_record` and `load_records` had a `@fasteners.interprocess_locked('lock-file')` decorator, which seemingly protects against concurrent access. However, `store_record` called `load_records` multiple times, and the lock was release after the first call to `load_records` finished.

The load results were compared, and if they were not equal, `debug` was called:
```
    RECORDS = load_or_initialize_records()

    records_2 = load_or_initialize_records()
    records_3 = load_or_initialize_records()
    records_4 = load_or_initialize_records()

    # these aliens are very rude, sometimes. better safe than sorry
    try:
        assert RECORDS == records_2 == records_3 == records_4, 'there are aliens'
    except AssertionError:
        debug(2)  # write operation
```
To exploit this you had to ensure the race condition occurs, so you threw concurrent `store_record` commands at it until you got the debug output.

Removing the debug function fixes this issue.

