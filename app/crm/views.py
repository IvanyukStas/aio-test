import uuid

from aiohttp_apispec import docs, request_schema, response_schema, querystring_schema

from app.crm.models import User
from app.crm.schemas import UserSchema, ListUsersResponseSchema, UserGetRequestSchema, UserGetResponseSchema, \
    UserAddSchema
from app.web.app import View
from aiohttp.web_exceptions import HTTPNotFound, HTTPUnauthorized, HTTPForbidden

from app.web.shcemas import OKResponseSchema
from app.web.utils import json_response, check_basic_auth


class AddUserView(View):
    @docs(tags=['CRM'], summary='Add new user', description='Add new user to the database.')
    @request_schema(UserAddSchema)
    @response_schema(OKResponseSchema, 200)
    async def post(self):
        data = self.request['data']
        user = User(email=data['email'], id_=uuid.uuid4())
        await self.request.app.crmaccessor.add_user(user)
        return json_response()

class ListUsersView(View):
    @docs(tags=['CRM'], summary='List off users', description='Get list of users from database.')
    @response_schema(ListUsersResponseSchema, 200)
    async def get(self):
        if not self.request.headers.get('Authorization'):
            raise HTTPUnauthorized
        if not check_basic_auth(self.request.headers['Authorization'], username=self.request.app.config.username,
                                password=self.request.app.config.password):
            raise HTTPForbidden
        users = await self.request.app.crmaccessor.list_users()
        raw_users = [{'email': user.email, 'id': str(user.id_)}for user in users]
        return json_response(data={'users': raw_users})

class GetUserView(View):
    @docs(tags=['CRM'], summary='Get user from id', description='Get user from database.')
    @querystring_schema(UserGetRequestSchema)
    @response_schema(UserGetResponseSchema, 200)
    async def get(self):
        user_id = self.request.query['id']
        print(user_id)

        # try:
        #     uuid.UUID(user_id)
        # except:
        #     raise HTTPInternalServerError(reason='No right format for ID')
        user = await self.request.app.crmaccessor.get_user(uuid.UUID(user_id))
        if user:
            raw_user = {'email': user.email, 'id_': str(user.id_)}
            return json_response(data={'user': raw_user})
        else:
            raise HTTPNotFound