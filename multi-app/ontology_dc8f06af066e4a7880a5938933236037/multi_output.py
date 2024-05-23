from decimal import *
from datetime import *
from typing import *
from marshmallow import Schema, fields, post_load
from openfabric_pysdk.utility import SchemaUtil



################################################################
# MultiOutput concept class - AUTOGENERATED
################################################################
class MultiOutput:
    response: str = None
    attachment: str = None
    

################################################################
# MultiOutputSchema concept class - AUTOGENERATED
################################################################
class MultiOutputSchema(Schema):
    response = fields.String()
    attachment = fields.String(allow_none=True)
    
    
    @post_load
    def create(self, data, **kwargs):
        return SchemaUtil.create(MultiOutput(), data)