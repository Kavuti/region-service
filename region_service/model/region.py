from .. import db
from webargs import fields, ValidationError

def __check_region_existence(description):
    if Region.query.filter_by(description=description).first():
        raise ValidationError("The region already exists")

class Region(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(30), nullable=False)

region_args = {
    "id": fields.Int(validate=lambda val: val > 0),
    "description": fields.Str(validate=__check_region_existence)
}