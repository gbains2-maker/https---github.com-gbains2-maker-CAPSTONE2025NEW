from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simple in-memory list of reviews
reviews = [
    {
        "id": 1,
        "artist": "Daft Punk",
        "album": "Random Access Memories",
        "rating": 9,
        "text": "A warm, nostalgic blend of electronic and live instruments."
    },
    {
        "id": 2,
        "artist": "Taylor Swift",
        "album": "1989",
        "rating": 8,
        "text": "Pure pop songwriting with huge hooks."
    },
]


def next_id():
    if not reviews:
        return 1
    return max(r["id"] for r in reviews) + 1


@app.route("/")
def index():
    return render_template("index.html", reviews=reviews)


@app.route("/review/<int:review_id>")
def review_detail(review_id):
    review = next((r for r in reviews if r["id"] == review_id), None)
    return render_template("review_detail.html", review=review)


@app.route("/add", methods=["GET", "POST"])
def add_review():
    if request.method == "POST":
        artist = request.form.get("artist", "").strip()
        album = request.form.get("album", "").strip()
        rating = request.form.get("rating", "").strip()
        text = request.form.get("text", "").strip()

        if artist and album and rating:
            try:
                rating_val = int(rating)
            except ValueError:
                rating_val = 0

            reviews.append({
                "id": next_id(),
                "artist": artist,
                "album": album,
                "rating": rating_val,
                "text": text or "No comments yet."
            })
            return redirect(url_for("index"))

    return render_template("page1.html")  # reuse page1 as "Add Review" page


@app.route("/page1")
def page1():
    # Add Review page
    return render_template("page1.html")


@app.route("/page2")
def page2():
    # About / How AI Helped
    return render_template("page2.html")


if __name__ == "__main__":
    app.run(debug=True)
