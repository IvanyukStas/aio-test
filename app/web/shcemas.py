from marshmallow import Schema, fields


class OKResponseSchema(Schema):
    status = fields.Str()
    data = fields.Dict()
