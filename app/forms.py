from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField


class NewProjectForm(FlaskForm):
    project_name = StringField("project_name")
    upload_data = FileField(validators=[FileRequired()])


class SaveCollateDataForm(FlaskForm):
    name = StringField()


class CollateDataForm(FlaskForm):
    condition = StringField()
    condition_col = StringField()
    action = StringField()
    action_col = StringField()
