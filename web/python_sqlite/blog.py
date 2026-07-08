from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash,
)
from models import get_db
from utils import login_required

blog_bp = Blueprint("blog", __name__, url_prefix="")


@blog_bp.route("/")
def index():
    db = get_db()
    posts = db.execute("""
        SELECT p.id, p.title, p.body, p.created_at, u.username
        FROM posts p
        JOIN users u ON u.id = p.author_id
        ORDER BY p.created_at DESC
    """).fetchall()
    return render_template("index.html", posts=posts)


@blog_bp.route("/post/<int:post_id>")
def view_post(post_id):
    db = get_db()
    post = db.execute("""
        SELECT p.id, p.title, p.body, p.created_at, u.username
        FROM posts p
        JOIN users u ON u.id = p.author_id
        WHERE p.id = ?
    """, (post_id,)).fetchone()
    if post is None:
        flash("Post not found.")
        return redirect(url_for("blog.index"))
    return render_template("post.html", post=post)


@blog_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()

        if not title or not body:
            flash("Title and body are required.")
            return render_template("create_post.html")

        db = get_db()
        db.execute(
            "INSERT INTO posts (title, body, author_id) VALUES (?, ?, ?)",
            (title, body, session["user_id"]),
        )
        db.commit()
        flash("Post created!")
        return redirect(url_for("blog.index"))

    return render_template("create_post.html")
