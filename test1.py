from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/reg", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        name = request.form["name"]
        lastname = request.form["lastname"]
        group = request.form["group"]
        mail = request.form["mail"]

        print("Success!")
        return "Registration successful"

    return render_template("/templates/reg.html")


if __name__ == "__main__":
    app.run(debug=True)
