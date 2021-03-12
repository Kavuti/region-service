from ..model.region import Region, RegionSchema
from ..utils import *
from .. import db
from marshmallow import ValidationError
import logging

logger = logging.getLogger()

class RegionWorker:
    def get(self, **kwargs):
        query = Region.query
        if 'id' in kwargs:
            schema = RegionSchema()
            region = query.get(kwargs['id'])
            return schema.dump(region)
        else:
            if 'description' in kwargs:
                query = query.filter(Region.description.ilike(f"%{kwargs['description']}%"))
            if 'active' in kwargs:
                query = query.filter_by(active=kwargs['active'])

        schema = RegionSchema(many=True)
        return schema.dump(query.all())

    def post(self, region):
        try:
            schema = RegionSchema()
            db.session.add(region)
            db.session.commit()
            return schema.dump(region)
        except ValidationError as e:
            raise e
        except Exception as ex:
            db.session.rollback()
            raise ex

    def put(self, id, region):
        try:
            schema = RegionSchema()
            logger.info(region)
            persistent_region = Region.query.get(id)
            if not persistent_region:
                raise ValidationError("The given id does not correspond to a region")
            persistent_region.description = region.description
            db.session.commit()
            return schema.dump(persistent_region)
        except ValidationError as e:
            raise e
        except Exception as ex:
            db.session.rollback()
            raise ex

    def delete(self, id):
        try:
            persistent_region = Region.query.get(id)
            if not persistent_region:
                raise ValidationError("The given id does not correspond to a region")
            db.session.delete(persistent_region)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            raise ex