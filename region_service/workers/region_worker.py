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
        elif 'description' in kwargs:
            query = query.filter(Region.description.ilike(f"%{kwargs['description']}%"))

        schema = RegionSchema(many=True)
        return schema.dump(query.all())

    def post(self, region):
        try:
            schema = RegionSchema()
            db.session.add(region)
            db.session.commit()
            return schema.dump(region)
        except ValidationError as error:
            logger.info(f"Invalid region received: {error.messages}")
            return error.messages
        except Exception as e:
            logger.error(f"Error saving new region {region}", e)
            db.session.rollback()
            raise e