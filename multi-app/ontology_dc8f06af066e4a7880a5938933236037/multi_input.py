from decimal import *
from datetime import *
from typing import *
from marshmallow import Schema, fields, post_load
from openfabric_pysdk.utility import SchemaUtil



################################################################
# MultiInput concept class - AUTOGENERATED
################################################################
class MultiInput:
    option: str = None
    text: str = None
    voice: str = None
    attachment: str = None
    

################################################################
# MultiInputSchema concept class - AUTOGENERATED
################################################################
class MultiInputSchema(Schema):
    option = fields.String()
    text = fields.String(allow_none=True)
    voice = fields.String(allow_none=True)
    attachment = fields.String(allow_none=True)
    
    
    @post_load
    def create(self, data, **kwargs):
        return SchemaUtil.create(MultiInput(), data)
