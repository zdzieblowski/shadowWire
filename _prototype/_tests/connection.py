import requests

url = "http://bebok.tech:60606/read"
myobj = {"key": "value"}

x = requests.post(url, json = myobj)

print(x.text)
