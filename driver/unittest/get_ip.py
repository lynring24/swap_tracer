from requests import get
from flask import Flask

app = Flask(__name__)

ip = get('https://api.ipify.org').text
print 'My public IP address is:', ip


@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(host=ip)
