# SaplingCTF 2023

I was a challenge author for SaplingCTF 2023!

My challenges and their solutions can be found at the following links:

* [Pager](https://github.com/ubcctf/sapling-ctf-2023-public/tree/main/web/pager)
* [BeeHive](https://github.com/ubcctf/sapling-ctf-2023-public/tree/main/web/beehive)

I also tested and wrote solve scripts for some of my teammates challenges.

* [El-pajaro](https://github.com/ubcctf/sapling-ctf-2023-public/blob/main/web/el-pajaro/solve/solve.py)
* [El-zorro](https://github.com/ubcctf/sapling-ctf-2023-public/blob/main/web/el-zorro/solve/solve.py)
* [La-culebra](https://github.com/ubcctf/sapling-ctf-2023-public/blob/main/web/la-culebra/solve/solve.py)

## BeeHive (easy)

This challenge was modeled after an exploit I found worked on my high schools routers. Unfortunately, after responsibility disclosing it to my school boards IT they were very displeased with 14 year old me. Regardless, I thought it made a good beginner challenge.

The challenge consists of a login page in which your login attempts are logged to a file in the same directory. Each login attempts includes the username and whether the login succeeded. The PHP code also uses the `include` directive to direct whether a user is to be on the login page or has logged in and can access the dashboard.

To get the flag, you must log in with a username that contains a php payload such as `<?php system('cat /flag')>` and then pass the log into the include directive like `index.php?file=login.log`. Your PHP payload will then be executed printing the flag!

## Pager (medium)

I wanted to experiment with request smuggling so I went digging for a request smuggling exploit. I found CVE-2019-20372, a request smuggling exploit in NGINX and decided to model a challenge around that.

The details of CVE-2019-20372 are well described [here](https://bertjwregeer.keybase.pub/2019-12-10%20-%20error_page%20request%20smuggling.pdf) but in the case of this specific challenge it allows users to bypass the vhost restriction and access the backend vhost that evaluates a POST parameter.

More detail on this challenge can be found in it's [README](https://github.com/ubcctf/sapling-ctf-2023-public/blob/main/web/pager/README.md).
