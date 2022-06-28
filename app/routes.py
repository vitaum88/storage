from app import app, db
from app.forms import LoginForm, RegistrationForm, UploadForm
from app.models import User, Files

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
from utils import s3_upload
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

import datetime


@app.route("/")
@app.route("/index")
@login_required
def index():
    u = User.query.filter_by(username=current_user.username).first()
    files = Files.query.filter_by(
        owner=u
    ).all()
    return render_template("index.html", title="Home Page", files=files)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/buckets")
@login_required
def buckets():
    try:
        return True
    except Exception as e:
        return {"message": e}


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data
        ).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/upload_file", methods=["GET", "POST"])
@login_required
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=current_user.username).first()
        try:
            date_string = datetime.date.today().strftime("%Y/%m/%d")
            path = f"{u.username}/{date_string}"
            output = s3_upload(form.file, path)
            file = form.file.data
            filename = secure_filename(file.filename)
            f = Files(filename=filename,
                      address=f"{output}",
                      owner=u)
            db.session.add(f)
            db.session.commit()
        except IntegrityError as e:
            flash("Duplicated file detected!")
            return redirect(url_for("upload_file"))
        except Exception as e:
            flash("Error uploading file to S3!")
            return redirect(url_for("upload_file"))
        flash(f"Uploaded to S3: {filename}")
        return redirect(url_for("index"))
    return render_template("upload.html", form=form)
