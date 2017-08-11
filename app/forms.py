from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField,validators
from wtforms.fields import FieldList,FormField


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


class ColumnSetup(FlaskForm):
    name = StringField("Column Name",validators=[validators.DataRequired()])
    # TODO: Implement global dict for data types implemented
    d_type = StringField("Data Type",validators=[validators.DataRequired()])
    format = StringField()


class ColumnSetupForm(FlaskForm):
    columns = FieldList(FormField(ColumnSetup))


class SearchCriteria(FlaskForm):
    column = StringField()
    regex_search = StringField()


class SearchForm(FlaskForm):
    criterion = FieldList(FormField(SearchCriteria))
