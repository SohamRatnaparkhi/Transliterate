from flask import Flask, redirect, render_template, request, send_from_directory, url_for

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
