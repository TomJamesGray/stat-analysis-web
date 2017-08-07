from app.app import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(50), index=True)
    dataset_location = db.Column(db.String(50), index=True)

    def __repr__(self):
        return "<Project name={}>".format(self.project_name)


class CollateDataSave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), index=True)
    save_name = db.Column(db.String(50), index=False)
    condition = db.Column(db.String(50), index=False)
    condition_col = db.Column(db.String(50), index=False)
    action = db.Column(db.String(50), index=False)
    action_col = db.Column(db.String(50), index=False)
