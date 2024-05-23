from decimal import *
from datetime import *
from typing import *
from marshmallow import Schema, fields, post_load
from openfabric_pysdk.utility import SchemaUtil


################################################################
# TextInput concept class - AUTOGENERATED
################################################################
class TextInput:
    audioInput: str = None
    

################################################################
# TextInputSchema concept class - AUTOGENERATED
################################################################
class TextInputSchema(Schema):
    audioInput = fields.String()
    
    
    @post_load
    def create(self, data, **kwargs):
        return SchemaUtil.create(TextInput(), data)