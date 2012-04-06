# -*- coding: utf-8 -*- 
# AUTHOR: Zeray Rice <fanzeyi1994@gmail.com>
# FILE: wobbuffet.py
# CREATED: 15:57:06 06/04/2012
# MODIFIED: 16:22:30 06/04/2012

from flask import Flask
from flask import request
from flask import render_template
from flaskext.sqlalchemy import SQLAlchemy

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

@app.route("/")
def index():
    page = request.args.get("p", 0, type=int)
    links = db.session.query(Link).order_by(Link.id.desc())
    link_count = links.count()
    links = links.limit(app.config["LINKS_PER_PAGE"]).offset(page * app.config["LINKS_PER_PAGE"]).all()
    return render_template("index.html", links = links)

if __name__ == "__main__":
    app.run(debug = True)
