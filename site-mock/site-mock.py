from flask import Flask

app = Flask(__name__)
@app.route('/')
def index():
    with open('index.html') as f:
        page = f.read()
    return page


if __name__ == '__main__':
	app.run(host="0.0.0.0")
