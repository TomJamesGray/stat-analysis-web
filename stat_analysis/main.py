import logging
import os
import csv
import re
import redis
from collections import OrderedDict
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField
from flask import Flask,render_template,request,flash,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy
from flask_kvsession import KVSessionExtension
from simplekv.memory.redisstore import RedisStore
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict

logger = logging.getLogger(__name__)
store = RedisStore(redis.StrictRedis())
app = Flask(__name__)
app.config.from_object('stat_analysis.config')
app.secret_key = "SECRET"
KVSessionExtension(store,app)

db = SQLAlchemy(app)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(50), index=True)
    dataset_location = db.Column(db.String(50), index=True)

    def __repr__(self):
        return "<Project name={}>".format(self.project_name)


class NewProjectForm(FlaskForm):
    project_name = StringField("project_name")
    upload_data = FileField(validators=[FileRequired()])

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/new", methods=["GET","POST"])
def new():
    if request.method == "POST":
        # TODO: Actually enable CSRF
        form = NewProjectForm(CombinedMultiDict((request.files,request.form)),csrf_enabled=False)
        if form.validate_on_submit():
            f = form.upload_data.data
            fname = secure_filename(f.filename)
            f.save(os.path.join("/home/tom/uploads",fname))

            # Add project to database
            project = Project(project_name=form.project_name.data,dataset_location=fname)
            db.session.add(project)
            db.session.commit()

            return redirect(url_for("index"))
        else:
            print(form.errors)
            print("Stuff missing??")

    return render_template("new_project.html")


@app.route("/view/<project_id>")
def view_project(project_id):
    # Read data from data file
    # Assuming there is a header row
    project = Project.query.filter_by(id=project_id).first()
    print(project)
    with open("/home/tom/uploads/{}".format(project.dataset_location),'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        data = []
        for row in reader:
            tmp = OrderedDict()
            for i,val in enumerate(row):
                tmp[headers[i]] = val
            data.append(tmp)

    if len(data) > 10:
        view_data = data[:10]
        truncated = True
    else:
        view_data = data
        truncated = False
    print("Setting project_data")
    session["project_data"] = data
    session["project_headers"] = headers

    return render_template("view_project.html",headers=headers,view_data=view_data,
                           truncated=truncated,project_name=project.project_name,rows=len(data))


@app.route("/view")
def view():
    projects = Project.query.all()
    print(projects)
    return render_template("view_projects.html", projects=projects)

@app.route("/search", methods=["GET","POST"])
def project_search():
    if request.method == "POST":
        # Use WTForms?
        cols = request.form.getlist("column_select[]")
        regexes = request.form.getlist("regex_search[]")
        output = []
        for row in session["project_data"]:
            matched = 0
            for i in range(0,len(cols)):
                if re.search(regexes[i],row[cols[i]]):
                    matched += 1
            if matched == len(cols):
                output.append(row)
        return render_template("search_results.html",data=output,headers=session["project_headers"])
