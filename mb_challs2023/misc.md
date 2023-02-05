# The Return of 110

## Challenge

Author: Arctic

Hey you. You’re finally awake. You were trying to cross into second year, right? Walked right into that ambush, same as us, and that cpen student over there. Damn you Gregor. CPSC 110 was imperative until you came along. Programming was nice and easy.

Part 1 will put you in a jail with no restrictions to let you get used to the basics. Connect with nc 1337.maplebacon.org 4000.

Part 2 will put you in a jail with quite a few restrictions that you’ll have to work around. Connect with nc 1337.maplebacon.org 4001.

## Walkthrough

### Part 1

Part 1 has no restrictions, as such a simple payload suffices.

```racket
(system "get-flag")
```

### Part 2

Part 2 is the proper challenge. The restrictions are as follows:

The following substrings are disallowed:

* `system`
* `process`
* `read-eval-print-loop`
* `shell-execute`

The following substrings are allowed:

* `string`
* `quote`

You are allowed 1 term that is not in the allowed list, however it cannot be a disallowed term. A disallowed term will immediately invalidate your query. We are given a hint that [quasiquoting](https://cadence.moe/blog/2022-10-17-explaining-lisp-quoting-without-getting-tangled) is of use.

After much painful investigation I realized that I could use the `string-append` function to produce strings without using my 1 exception as it contained `string` and I could append a list of characters into array like so `(string-append "h" "i") == "hi"`.

From there I attempted to use `eval` to execute the string: `(eval (string-append "(" "e" "x" "i" "t" ")"))`. Unfortunately `eval` cannot execute string and as such I continued to my search until I found `string->symbol`, a function which converts a string into symbols which eval can interpret as syntax.

Putting all of this together with the function `system` and arguments `/bin/sh` we get:

```racket
((eval (string->symbol (string-append "s" "y" "s" "t" "e" "m"))) (string-append "/" "b" "i" "n" "/" "s" "h"))
```

This pops us a shell in which we can `get-flag`.

## Solve

`maple{Gr390R_W0uLD_B3_pR0Ud}`
