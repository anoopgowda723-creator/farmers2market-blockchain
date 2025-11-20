from flask import Blueprint, render_template, redirect, url_for

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return render_template("home.html")

@main_bp.route("/index")
def index():
    # simple alias – always send to home
    return redirect(url_for("main.home"))
