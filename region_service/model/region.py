from .. import db, ma
from marshmallow import post_load
from webargs import fields, ValidationError


class Region(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(30), nullable=False)


class RegionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Region
        dump_only = ("id",)

    @post_load
    def to_region(self, data, **kwargs):
        return Region(**data)


region_args = {
    "id": fields.Int(validate=lambda val: val >= 0),
    "description": fields.Str()
}