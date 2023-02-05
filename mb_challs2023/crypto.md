# The Matrix Exchange

## Challenge

Author: vEvergarden

Alice and Bob are having a great time exchanging their little secret messages… until they realize they’re living in a simulation.

## Walkthrough

We are given a script which performs [Diffie-Hellman](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange) and uses the shared secret to AES encrypt the flag. We are also given the output of the script which contains the public keys (A, B) and p. The contents of the script also contain the constant g.

```py
# given variables (from output)
g = 1337
p = 146635760303605976983894071500931857745973394259316464700291483611526724218460127444254168689045959985005212817040847174467141482547356061539722956992438198039196888496774232353702637340110963371323293180453107143830592752177650175267498096676840496849442055749071547763221826370121367266367265736640016224849
A = 122593569202713047256910856823064610802102165848412863419714367343535068432181229651183057378109240921706373026419955238421640119452077037295962596003436443748125952314067117706872613751900101093292596858137281488155807864319911989756603206024363635538681795330100292400684134799357570963098198243796012905071
B = 142857700274726494408753852766748133062989262570137331655228102720787303055171574691107864588269598429108651878879476731967757999196356469620766415382477392868604610906632622085379260676352636736367989787236537655987365802465995407192642985159206280944380481606853288780557358104659172496832399866770779719373
ciphertext = b'!N\xde%Nx\x9f\x9c\xd1S\xb5L\xa1\x15\xd5\xc2\xdc\xe4\x06\xdc\x95R\xbf\xd0\x02A\xed Tpo\x91'
```

After investing the code I determined there was a mathematical error that meant DH was not being performed as desired.

```py
# multiply two 2x2 matrices A and B:
def mult(A, B):
    result = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            result[i][j] = (A[i][0] * B[0][j] + A[i][1] * B[1][j]) % p
    return result

# compute A^n with exponentiation by squaring
def exp(A, n):
    if n == 0:
        return [[1, 0], [0, 1]]
    half = exp(A, n // 2)
    if n % 2 == 0:
        return mult(half, half)
    return mult(A, mult(half, half))

# ...
alice_secret = randint(0, p)
alice_public = exp(G, alice_secret)
```

Rather than perform `g^a mod p` as defined in DH, the script was performing `g*a mod p` making it easy to brute-force the secret given a public key, g, and p.

```py
# brute.py
from Crypto.Cipher import AES
from hashlib import sha256

a = int(A)
while True:
    if a % g == 0:
        a = a // g
        break
    a += p

print("a:", a)

s = B * a % p 

print("s:", s)

key = str(s+2).encode()
key = sha256(key).digest()
cipher = AES.new(key, AES.MODE_ECB)
plaintext = cipher.decrypt(ciphertext)

print(plaintext)
```

```
a: 142121094362283061511892096821637861175645211467212591361478822471406614009976100426297929326621262095365338048686848950017479326864830349088434698505019373900155644394642257304227216132532234605053819944311825753738798370930723177981426057144751538560632867606864438777691061543834351668592900020338531805598
s: 14769252168361940999707084997601635824307518171525151482342703166357034302938389457875600598384419084251671625666492051620050967488404369452330736960113457843463427603580442852743874191888615111593150369232876849297076387356389656265115928075774764245626667709269992022833152076009883274663389058696698164661
b'maple{y0u_8rOke_mY_dlo9!??}\x05\x05\x05\x05\x05'
```

Big thanks to my friend JV who reminded me about some mathematical properties.

## Solve

`maple{y0u_8rOke_mY_dlo9!??}`
