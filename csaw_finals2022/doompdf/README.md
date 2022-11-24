# DOOM PDF

## Challenge

Waiting for them to post at <https://github.com/osirislab/CSAW-CTF-2022-Final-WriteUps>

## Walkthrough

We were given a modified version of [php-goof](https://github.com/snyk-labs/php-goof) without source provided. The mailer had been stripped out and XSS didn't get you anywhere. Given the challenge name it was pretty clear we'd be doing something with DOMPDF but after many attempts I realized that many tags had likely been blacklisted etc.

My first hint came after I got the `/composer.json` endpoint which discloses used libraries and associated versions.

```json
{
    ...
    "require": {
        "league/commonmark": "0.18.2", 
        "dompdf/dompdf": "2.0.0",
        "monolog/monolog": "1.27.0"
    }
}
```

DOMPDF had been updated to mitigate the initial exploit in php-goof but interesting monolog had been added, seemed pretty unnecessary for a CTF.

Interestingly [many CVEs](https://github.com/dompdf/dompdf/releases/tag/v2.0.0) had been patched in this release and after a lot of digging I found a post about [CVE-2022-41343](https://tantosec.com/blog/cve-2022-41343/) which took advantage of the lax patches for the vulnerabilities fixed in `2.0.0`.

The blog post is pretty comprehensive so check it out if you want more information but in essence they found it was possible to create a polyglot TrueType Font / PHAR file that would be written to the font cache with a predictable filename. Using this you could upload the given polyglot file and execute it as the server still wrote the file to disk regardless of it throwing errors.

## Solve

`flag{DAAAMN_MAN!Th3_name_is_DOMPDF_OR_DOOMPDF??_L0L_ee983ad5}`
