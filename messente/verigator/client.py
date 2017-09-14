import requests


class RestClient(object):
    def __init__(self, endpoint, username, password):
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.headers = {
            "X-Service-Auth": ":".join([self.username, self.password])
        }

    def _request(self, method, path, params=None, headers=None, json=None):
        resp = requests.request(method, path, params=params, headers=headers, json=json)

        status_code = resp.status_code
        resp_json = resp.json()

        if status_code == 500:
            raise InternalServerError(resp_json)
        elif status_code == 400:
            raise BadRequestError(resp_json)
        elif status_code == 401:
            raise UnauthorizedError(resp_json)
        elif status_code == 403:
            raise ForbiddenError(resp_json)
        elif status_code == 404:
            raise NotFoundError(resp_json)

        return resp_json

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


class InternalServerError(Exception):
    pass

class BadRequestError(Exception):
    pass

class NotFoundError(Exception):
    pass

class ForbiddenError(Exception):
    pass

class UnauthorizedError(Exception):
    pass