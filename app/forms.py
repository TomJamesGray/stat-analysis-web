from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField,validators


class NewProjectForm(FlaskForm):
    project_name = StringField("Project Name", validators=[validators.DataRequired()])
    upload_data = FileField("Upload Data",validators=[FileRequired()])


class SaveCollateDataForm(FlaskForm):
    name = StringField()


class CollateDataForm(FlaskForm):
    condition = StringField()
    condition_col = StringField()
    action = StringField()
    action_col = StringField()
