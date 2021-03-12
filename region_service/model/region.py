from .. import db, ma
from marshmallow import post_load
from webargs import fields, ValidationError


class Region(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(30), nullable=False, unique=True)
    active = db.Column(db.Boolean(), nullable=False, default=True)


class RegionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Region
        dump_only = ("id",)
        load_instance = True


region_args = {
    "id": fields.Int(),
    "description": fields.Str(),
    "active": fields.Boolean()
}