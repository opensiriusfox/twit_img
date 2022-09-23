# `twit_img` - Twitter Image Download Helper
A simple flask container based Tweepy frontend designed to download and name photos from tweets.

Enabled by the hard work of the [Tweepy](https://www.tweepy.org/) developers.

# `twit_img_secrets.py`
The `twit_img_secrets.py` file takes the following form.

See [Twitter's Developer Apps](https://developer.twitter.com/en/portal/projects-and-apps) page for registering for a key/secret pair.

See [Flask's Sessions Page](https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions) for generating a random junk secret key.
```
#!/usr/bin/env python3

consumer_key = '<your twitter API key>'
consumer_secret = '<your twitter API secret>'

flask_secret = b'<your random flask API secret key>'
```

## License
MIT. See [LICENSE](LICENSE)