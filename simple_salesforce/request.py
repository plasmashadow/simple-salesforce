try:

    #check whether it is appengine env or not.
    from google.appengine.api import urlfetch
    import json

    try:
        from urllib import urlencode  # For python 2
        from collections import OrderedDict

    except ImportError:

        from urllib.parse import urlencode


    _method = {
        "GET": urlfetch.GET,
        "POST": urlfetch.POST,
        "PUT": urlfetch.PUT,
        "DELETE": urlfetch.DELETE
    }


    class Response(object):

        def __init__(self, response):

            self.response = response
            self.status_code = response.status_code
            self.content = response.content

        def json(self, **kwargs):
            return json.JSONDecoder(**kwargs).decode(self.content)

        def __getattr__(self, item):
            return getattr(self.response, item)

    def url_concat(url, **kwargs):
        if not kwargs:
            return url

        if url[-1] not in ('?', '&'):
            url += '&' if ('?' in url) else '?'

        return url + urlencode(kwargs)

    def get(url, headers={}, params={}):
        url = url_concat(url, **params)
        result = urlfetch.fetch(url, method=urlfetch.GET, headers=headers)
        return Response(result)

    def post(url, headers={}, data=None):
        result = urlfetch.fetch(url, method=urlfetch.POST, headers=headers, payload=data)
        return Response(result)

    def request(method, url, headers={}, **kwargs):
        result = urlfetch.fetch(url, method=_method[method], headers=headers, **kwargs)
        return Response(result)

except ImportError:

    import requests

    get = requests.get
    post = requests.post
    request = requests.request