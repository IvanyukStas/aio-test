from marshmallow import Schema, fields

from app.web.shcemas import OKResponseSchema


class UserAddSchema(Schema):
    email = fields.Str(required=True)

class UserSchema(UserAddSchema):
    id = fields.UUID(required=True)

class UserGetRequestSchema(Schema):
    id = fields.UUID(required=True)

class GetUserSchema(Schema):
    user = fields.Nested(UserSchema)

class UserGetResponseSchema(OKResponseSchema):
    data =fields.Nested(GetUserSchema)

class ListUsersSchema(Schema):
    data = fields.Nested(UserSchema, many=True)

class ListUsersResponseSchema(OKResponseSchema):
    data = fields.Nested(ListUsersSchema)