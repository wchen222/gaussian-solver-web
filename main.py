import flask, gaussian

app = flask.Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if flask.request.method == "POST":
        try:
            matrix_txt = flask.request.form["matrix"]
            result = gaussian.display(matrix_txt)
        except ValueError:
            result = "Invalid input"
    return flask.render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True, port=5001)