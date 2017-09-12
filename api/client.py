import requests


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
        return requests.get(self.__url(path), params=params, headers=new_headers)

    def post(self, path, headers=None, json=None):
        new_headers = self.__get_headers(headers)
        return requests.post(self.__url(path), headers=new_headers, json=json)

    def put(self, path, headers=None, json=None):
        new_headers = self.__get_headers(headers)
        return requests.put(self.__url(path), headers=new_headers, json=json)

    def delete(self, path, headers=None):
        new_headers = self.__get_headers(headers)
        return requests.delete(path, headers=new_headers)

    def __get_headers(self, headers):
        new_headers = self.headers.copy()
        if headers:
            new_headers.update(headers)
        return new_headers

    def __url(self, path):
        return "/".join([self.endpoint.strip("/"), path])
