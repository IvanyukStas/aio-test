import base64
from typing import Any, Optional

from aiohttp.web_response import Response
from aiohttp.web import json_response as aiohttp_json_responce


def json_response(data: Any = None, status: str = 'ok')-> Response:
    if data is None:
        data = {}
    return aiohttp_json_responce(data={
        'status': status,
        'data': data
        })


def error_json_response(http_status: int, status: str = 'error', message: Optional[str] = None, data: Optional[dict] = None ):
    if data is None:
        data = {}
    status = http_status
    return aiohttp_json_responce(data={
        'status': status,
        'message':message,
        'data': data
        })


def check_basic_auth(raw_credentials: str, username: str, password: str)->bool:
    credentials = base64.b64decode(raw_credentials).decode()
    parts = credentials.split(':')
    if not len(parts) == 2:
        return False
    return parts[0] == username and parts[1] == password


def check_validation_for_answers(aswers:list):
    pass