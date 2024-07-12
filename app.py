from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from login import login_required

app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/nl")

@app.route("/nl")
def nl():
    return render_template("index.html")