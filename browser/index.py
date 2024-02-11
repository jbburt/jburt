from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    query = request.args.get("msg")
    response = f"{query}? what a dumb question! lmao"
    return response


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
