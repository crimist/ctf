# Vault

## Challenge

We we're given the file `vault.dat` with an unknown encryption scheme and challenged to decode it - if it was possible...

## Walkthrough

Inspecting the vault showed that there was a binary system with only 2 possible uint8 combos.

```bash
$ hexdump -C vault.dat
00028a90  20 20 09 09 20 09 09 20  20 09 09 20 20 09 09 20  |  .. ..  ..  .. |
00028aa0  20 20 09 09 20 09 09 09  20 20 09 09 20 09 09 20  |  .. ...  .. .. |
00028ab0  20 20 09 09 20 09 09 20  20 20 09 09 20 09 20 09  |  .. ..   .. . .|
00028ac0  20 20 09 09 20 09 09 20  20 09 09 20 20 09 20 20  |  .. ..  ..  .  |
00028ad0  20 20 09 09 20 09 09 20  20 20 09 09 20 20 09 20  |  .. ..   ..  . |
...
```

Decoding `0x20` as 1 and `0x09` as 0 resulted in ASCII hex characters and decoding these gave us our flag.

Credits to [@rctcwyvrn](https://github.com/rctcwyvrn) for her script. We worked on this chall together.

```py
from Crypto.Util.number import long_to_bytes

f = open("vault.dat")
contents = f.read()

test = b""
with open("layer.out", "wb") as f:
    for b_start in range(0, len(contents), 16):
        b = ["1" if x == "\x20" else "0" for x in contents[b_start:b_start+16]]
        sliced = b[4:8] + b[12:16]
        b = long_to_bytes(int("".join(sliced), 2))
        print(test)
        test += b
        f.write(b)
```

## Solve

`Encryption key 1: 1a54a7c80123f8f23711f9572f0e9798`
