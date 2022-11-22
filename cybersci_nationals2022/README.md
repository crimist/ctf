# CyberSci Nationals 2022

Team Baple 2nd place.

Unfortunately, I didn't keep most of my files for this CTF and those that I found were super simple so I won't write them up.

Instead, while you're here I might as well write a little tidbit about our setup for their Defense only (yes not A/D) round.

---

## Signature server

We ended up encountering some trouble trying to patch certain binaries and programs. Most notably a JAR running an HTTP "signature" server. Fortunately we had done a little prep work and one of my teammates had pointed out that [mitmproxy](https://mitmproxy.org/), the well known interactive HTTPS proxy, actually has a [python API](https://docs.mitmproxy.org/stable/api/mitmproxy/http.html)!

Because their attack consisted of automated attacks from a bot we were able to pretty easily identify some of the other exploits based on traffic (stuff like shell commands in the packet lol) and drop the request.

Furthermore, because they updated score every minuit we were able to use this script to drop 1 of the 5 requests and determine whether it was malicious. Using this method I noticed that the requests with `8QwLuE7BanGz4oI8YiOWg` in the signature seemed to be an attack and we blocked it. Didn't even have to look at the services code!

Their defense only CTF concept was pretty fun and unique but of course being security students we found ways to exploit it. We'll have to see how they change it up next year!

### Blocking script

```py
from mitmproxy import http
from pprint import pprint
import base64

def request(flow):
    if "private.key" in str(flow.request.data):
        flow.kill()
        return

    if "Authtoken" in flow.request.headers:
        if b"pwned" in base64.b64decode(flow.request.headers[b'Authtoken']):
            print('Killed authtoken request')
            flow.kill()
            return

    if "Signature" in flow.request.headers:
        if "8QwLuE7BanGz4oI8YiOWg" in flow.request.headers[b'Signature']:
            print('Killed signature request')
            flow.kill()
            return

    return flow.request

def response(flow):
    return flow.response
```
