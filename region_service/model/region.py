from .. import db, ma
from marshmallow import post_load

class Region(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(30), nullable=False)

class RegionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Region
        load_instance = True

    # @post_load
    # def create_object(self, data, **kwargs):
    #     return Region(**data)