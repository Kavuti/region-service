from .. import db

class Region(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(30), nullable=False)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()