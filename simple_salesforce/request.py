try:

    #check whether it is appengine env or not.
    from google.appengine.api import urlfetch

    try:
        from urllib import urlencode  # For python 2

    except ImportError:

        from urllib.parse import urlencode

    def url_concat(url, **kwargs):
        if not kwargs:
            return url

        if url[-1] not in ('?', '&'):
            url += '&' if ('?' in url) else '?'

        return url + urlencode(kwargs)

    def get(url, headers={}, params={}):
        url = url_concat(url, **params)
        return urlfetch.fetch(url, method=urlfetch.GET, headers=headers)

    def post(url, headers={}, data=None):
        return urlfetch.fetch(url, method=urlfetch.POST, headers=headers, payload=data)

except ImportError:

    import requests

    get = requests.get
    post = requests.post