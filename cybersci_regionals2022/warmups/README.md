# Warmups

## Challenge

We were given an IP and flag format. No other info.

## Walkthrough

The only warmup worth talking about was a classic vhost issue.

Inspecting the certificate for the webserver running on `10.0.2.21` showed that the certificate was signed for 2 domains: `warmup.nuber.int` and `internal.nuber.int`. As such I tried setting the `Host` header and voila, the flag.

```py
import httpx

r = httpx.get('https://10.0.2.21/', headers={'Host': 'internal.nuber.int'}, verify=False)
print(r.status_code, r.text)
```

I actually solved this 3 mins after the CTF ended because I couldn't get it working. Turns out using `http` instead of `https` was the culprit :|

## Solve

`SERVERADMIN-sX2dq4Cmrv1HcmGDYbTa3vIav8GB_erLz3Eo0A7psQ0`
