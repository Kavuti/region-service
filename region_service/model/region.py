from .. import db, ma
from flask_marshmallow import post_load

class Region(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(30), nullable=False)

class RegionSchema(ma.Schema):
    class Meta:
        fields = ("id", "description")

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)