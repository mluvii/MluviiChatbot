# MluviiChatbot
Mluvii chatbot which uses public chatbot API

**To start Bot**

1. Create bot and API key in APP

2. Set bot id, client id and client secret in main.py

```
botOne = bot(2, "aa126d12c2203d29b3f0a40f8bd06402", "e80ed73d11ea404f9a1d46f9cb61a2f3")
```

3. Run bot `python3 wsgi.py -hostname https://local.mluvii.com`

Configure your chatbot in settings.py

the way to go: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04
