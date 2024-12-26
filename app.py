from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

def get_likes_from_db():
    conn = sqlite3.connect("likes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, like_count FROM likes")
    posts = cursor.fetchall()
    conn.close()
    return posts

def update_likes_in_db(post_id, new_like_count):
    conn = sqlite3.connect("likes.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE likes SET like_count = ? WHERE id = ?", (new_like_count, post_id))
    conn.commit()
    conn.close()

@app.route("/")
def index():
    posts = get_likes_from_db()
    return render_template("Helloworld.html", posts=posts)

@app.route("/like/<int:post_id>", methods=["POST"])
def like_post(post_id):
    conn = sqlite3.connect("likes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT like_count FROM likes WHERE id = ?", (post_id,))
    result = cursor.fetchone()

    if result:
        new_like_count = result[0] + 1
        update_likes_in_db(post_id, new_like_count)
        conn.close()
        return jsonify({"likes": new_like_count})
    else:
        conn.close()
        return jsonify({"error": "Post não encontrado"}), 404

if __name__ == "__main__":
    app.run(debug=True)
