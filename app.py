from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index_page():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def receive_data():
    error = None
    if request.method == "POST":
        pass


if __name__ == '__main__':
    app.run()
