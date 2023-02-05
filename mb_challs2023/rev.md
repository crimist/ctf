# Rando

## Challenge

Author: Desp

This guy keeps taunting me for not being able to guess his flag :( Surely there’s a better way to this, right?

## Walkthrough

We are given a binary which reads stdin, encodes it, and compares it to a hardcoded string to determine if it is the flag.

```c
char check [18];
fgets(check,0x12,stdin);

for (i = 0; (uint)i < 0x11; i = i + 1) {
    bVar2 = check[5] ^ check[0] ^ check[1] ^ check[3];
    memmove(check,check + 1,0x11);
    check[16] = bVar2;
}

iVar3 = strcmp(check,"\x1b8!\x16\n;/\"B\x11#\x16x\x05qlM");
if (iVar3 == 0) {
    puts("How?????");
}
```

After experimenting, I quickly realized it would not be feasible to do by hand and remembered of a tool called Z3, a theorem prover, that I had heard was often helpful for rev challenges.

After spending some time learning Z3 I was able to come up with the following script to decode the message.

```py
from z3 import *

data = "\x1b8!\x16\n;/\"B\x11#\x16x\x05qlM"
s = Solver()

# variables
X = [BitVec('b{}'.format(i), 8) for i in range(17)]

# acsii range
characters = [And(X[i] > 0x20, X[i] < 0x7F) for i in range(17)]
s.add(characters)

# we know start and end
s.add(X[0] == ord('m'))
s.add(X[1] == ord('a'))
s.add(X[2] == ord('p'))
s.add(X[3] == ord('l'))
s.add(X[4] == ord('e'))
s.add(X[5] == ord('{'))
s.add(X[16] == ord('}'))

for i in range(11):
    s.add(X[0] ^ X[1] ^ X[3] ^ X[5] == ord(data[0]))
    data = data[1:] + data[:1]
    X = X[1:] + X[:1]

print(s)

while s.check() == sat:
    m = s.model()
    print(m)

    # pretty print flag
    for _ in range(6):
        data = data[1:] + data[:1]
        X = X[1:] + X[:1]

    print(''.join([chr(m.evaluate(X[i]).as_long()) for i in range(0x11)]))
```

## Solve

`maple{LFSR_wh4t?}`
