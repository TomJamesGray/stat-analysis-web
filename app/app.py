import logging
import os
import csv
import re
import redis
from collections import OrderedDict
from flask import Flask,render_template,request,flash,redirect,url_for,session,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_kvsession import KVSessionExtension
from simplekv.memory.redisstore import RedisStore
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict

logger = logging.getLogger(__name__)
store = RedisStore(redis.StrictRedis())
app = Flask(__name__)
app.config.from_object('app.config')
app.secret_key = "SECRET"
KVSessionExtension(store,app)
db = SQLAlchemy(app)

from app.models import *
from app.forms import *
from app import collate


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
            session["project_id"] = project.id

            return redirect(url_for("new_project_columns"))
        else:
            print(form.errors)
            print("Stuff missing??")

    return render_template("new_project.html")


@app.route("/new/column_setup", methods=["GET","POST"])
def new_project_columns():
    # Read in header row from data file for project
    project = Project.query.filter_by(id=session["project_id"]).first()
    with open("/home/tom/uploads/{}".format(project.dataset_location),'r') as f:
        reader = csv.reader(f)
        headers = next(reader)

    return render_template("new_project_col_setup.html", headers=enumerate(headers))


@app.route("/view/<project_id>")
def view_project(project_id):
    # Read data from data file
    # Assuming there is a header row
    project = Project.query.filter_by(id=project_id).first()
    collate_data_saves = CollateDataSave.query.filter_by(project_id=project_id).all()

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
    session["project_id"] = project_id
    session["active_data"] = "project"

    return render_template("view_data.html",headers=headers,view_data=view_data,
                           truncated=truncated,project_name=project.project_name,rows=len(data),
                           collate_data_saves=collate_data_saves)


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
        for row in session["{}_data".format(session["active_data"])]:
            matched = 0
            for i in range(0,len(cols)):
                if re.search(regexes[i],row[cols[i]]):
                    matched += 1
            if matched == len(cols):
                output.append(row)
        return render_template("search_results.html",data=output,
                               headers=session["{}_headers".format(session["active_data"])])


@app.route("/collate",methods=["GET","POST"])
def project_collate_data():
    if request.method == "POST":
        form = CollateDataForm(request.form,csrf_enabled=False)
        if form.validate_on_submit():
            output_data = collate_data(form.condition.data,form.condition_col.data,
                                       form.action.data,form.action_col.data)

            session["collate_data"] = output_data
            session["active_data"] = "collate"
            session["collate_headers"] = [form.condition_col.data,form.action_col.data]

            # Set session variables so collate data commands can be saved
            session["collate_data_condition"] = form.condition.data
            session["collate_data_condition_col"] = form.condition_col.data
            session["collate_data_action"] = form.action.data
            session["collate_data_action_col"] = form.action_col.data

            return render_template("view_data.html",view_data=output_data,headers=[
                form.condition_col.data,form.action_col.data],already_collated=True)


@app.route("/collate/save",methods=["POST"])
def save_collated():
    form = SaveCollateDataForm(request.form,csrf_enabled=False)
    if form.validate_on_submit():
        save_name = form.name.data
        # Create collate data save instance
        collated = CollateDataSave(save_name=save_name,project_id=session["project_id"],
                                   condition=session["collate_data_condition"],
                                   condition_col=session["collate_data_condition_col"],
                                   action=session["collate_data_action"],action_col=session["collate_data_action_col"])
        db.session.add(collated)
        db.session.commit()

        return redirect(url_for("view_project",project_id=session["project_id"]))


@app.route("/collate/view/<collate_id>")
def view_collate_data(collate_id):
    # Get save data for the collated data
    save = CollateDataSave.query.filter_by(id=collate_id).first()
    data = collate_data(save.condition,save.condition_col,save.action,save.action_col)
    # Set the active data
    session["active_data"] = "collate"
    session["collate_data"] = data
    session["collate_headers"] = [save.condition_col, save.action_col]
    return render_template("view_data.html",headers=[save.condition_col, save.action_col],view_data=data,
                           project_name=save.save_name,already_collated=True)


@app.route("/api/get_active_data")
def get_active_data():
    """
    Gets the active data set and headers for it
    :return: In JSON format the headers and data for the active data set
    """
    return jsonify(headers=session["{}_headers".format(session["active_data"])],
            data=session["{}_data".format(session["active_data"])])


def collate_data(c_func_name,c_col,a_func_name,a_col):
    """
    Generic collate data function
    :param c_func_name: Condition function
    :param c_col: Condition column the condition function will work on
    :param a_func_name: The action function, ie what will happen with the result
    of the condition function
    :param a_col: Action column - The column the action function will work on
    :return: The collated data set
    """
    collate_conditions = {
        "matches": collate.conditions.matches
    }
    collate_actions = {
        "sum": collate.actions.sum
    }
    c_func = collate_conditions[c_func_name]
    collate_data = c_func(session["project_data"], c_col)
    a_func = collate_actions[a_func_name]
    final_data = a_func(collate_data, a_col)

    # Change the format of the final_data output so it's the same format as the
    # view raw project data for example
    output_data = []
    for key, val in final_data.items():
        output_data.append({c_col: key, a_col: val})

    return output_data
