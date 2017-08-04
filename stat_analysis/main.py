import logging
import os
import csv
from collections import OrderedDict
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField
from flask import Flask,render_template,request,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict

logger = logging.getLogger(__name__)
app = Flask(__name__)
app.config.from_object('stat_analysis.config')
app.secret_key = "SECRET"

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
        print(f)
        reader = csv.reader(f)
        headers = next(reader)
        data = []
        for row in reader:
            tmp = OrderedDict()
            for i,val in enumerate(row):
                tmp[headers[i]] = val
            data.append(tmp)

        print(data)

    return render_template("view_project.html",headers=headers,data=data,project_name=project.project_name)


@app.route("/view")
def view():
    projects = Project.query.all()
    print(projects)
    return render_template("view_projects.html", projects=projects)
