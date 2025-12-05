from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory "database" of rules
rules = [
    {"id": 1, "text": "Brush your teeth.", "completed": False},
    {"id": 2, "text": "Put on pajamas.", "completed": False},
    {"id": 3, "text": "Read one bedtime story.", "completed": False},
]

def next_id():
    if not rules:
        return 1
    return max(r["id"] for r in rules) + 1


@app.route("/")
def index():
    return render_template("index.html", rules=rules)


@app.route("/add", methods=["POST"])
def add_rule():
    text = request.form.get("rule_text", "").strip()
    if text:
        rules.append({"id": next_id(), "text": text, "completed": False})
    return redirect(url_for("index"))


@app.route("/toggle/<int:rule_id>")
def toggle_rule(rule_id):
    for r in rules:
        if r["id"] == rule_id:
            r["completed"] = not r["completed"]
            break
    return redirect(url_for("index"))


@app.route("/page1")
def page1():
    # “Why Bedtime Rules Matter”
    return render_template("page1.html")


@app.route("/page2")
def page2():
    # “Rewards & Consequences”
    return render_template("page2.html")


if __name__ == "__main__":
    app.run(debug=True)
