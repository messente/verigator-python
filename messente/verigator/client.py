import requests
from .exceptions import *


class RestClient(object):
    def __init__(self, endpoint, username, password):
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.headers = {
            "X-Service-Auth": ":".join([self.username, self.password])
        }

    def get(self, path, params=None, headers=None):
        new_headers = self.__get_headers(headers)
        return self._request("GET", self.__url(path), params=params, headers=new_headers)

    def post(self, path, headers=None, json=None):
        new_headers = self.__get_headers(headers)
        new_headers['Content-Type'] = "application/json"
        new_headers['Accept'] = "application/json"
        return self._request("POST", self.__url(path), headers=new_headers, json=json)

    def put(self, path, headers=None, json=None):
        new_headers = self.__get_headers(headers)
        new_headers['Content-Type'] = "application/json"
        new_headers['Accept'] = "application/json"
        return self._request("PUT", self.__url(path), headers=new_headers, json=json)

    def delete(self, path, headers=None):
        new_headers = self.__get_headers(headers)
        return self._request("DELETE", self.__url(path), headers=new_headers)

    def __get_headers(self, headers):
        new_headers = self.headers.copy()
        if headers:
            new_headers.update(headers)
        return new_headers

    def __url(self, path):
        return "/".join([self.endpoint.strip("/"), path])

    @staticmethod
    def _request(method, path, params=None, headers=None, json=None):
        resp = requests.request(method, path, params=params, headers=headers, json=json)

        status_code = resp.status_code
        resp_json = resp.json()
        message = resp_json.get('message', None)

        if status_code == 400:
            raise InvalidDataError(400, message)
        elif status_code == 401:
            raise WrongCredentialsError(401, message)
        elif status_code == 403:
            raise ResourceForbiddenError(403, message)
        elif status_code == 404:
            raise NoSuchResourceError(404, message)
        elif status_code == 409:
            raise ResourceAlreadyExistsError(409, message)
        elif status_code == 422:
            raise InvalidDataError(422, message)
        elif status_code == 500:
            raise InternalError(500, resp_json)
        elif 300 <= status_code <= 600:
            raise VerigatorError(status_code, resp_json)

        return resp_json
