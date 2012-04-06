# -*- coding: utf-8 -*- 
# AUTHOR: Zeray Rice <fanzeyi1994@gmail.com>
# FILE: wobbuffet.py
# CREATED: 15:57:06 06/04/2012
# MODIFIED: 17:36:02 06/04/2012

import datetime
from functools import wraps

from flask import Flask
from flask import abort
from flask import request
from flask import render_template
from flaskext.sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)

class Link(db.Model):
    __tablename__ = "link"
    id        = db.Column(db.Integer, primary_key = True)
    title     = db.Column(db.String())
    url       = db.Column(db.String())
    comment   = db.Column(db.String(), default = "")
    create_at = db.Column(db.DateTime, index = True)

try:
    db.create_all()
except Exception:
    pass

def authentication(f):
    @wraps(f)
    def _auth_decorator(*args, **kwargs):
        auth = request.args.get("auth", type=unicode)
        if auth != app.config["AUTH"]:
            return abort(404)
        return f(*args, **kwargs)
    return _auth_decorator

@app.route("/")
def index():
    page = request.args.get("p", 0, type=int)
    links = db.session.query(Link).order_by(Link.id.desc())
    link_count = links.count()
    links = links.limit(app.config["LINKS_PER_PAGE"]).offset(page * app.config["LINKS_PER_PAGE"]).all()
    return render_template("index.html", links = links)

@app.route("/add", methods=["POST", "GET"])
@authentication
def add_link():
    if request.method == 'POST':
        return post_link()
    url = request.args.get("link", type=unicode)
    title = request.args.get("title", type=unicode)
    auth = request.args.get("auth", type=unicode)
    if not url and title:
        return abort(400)
    return render_template("new.html", url = url, title = title, auth = auth)

def post_link():
    print str(request.form)
    url = request.form["url"]
    title = request.form["title"]
    comment = request.form["comment"]
    if not url and title:
        return render_template("new.html", url = url, title = title)
    link = Link()
    link.title = title
    link.url = url
    link.comment = comment
    link.create_at  = datetime.datetime.now()
    db.session.add(link)
    db.session.commit()
    return render_template("close.html")

if __name__ == "__main__":
    app.run(debug = True)
