import requests

class API_Functions:
        
    def api_call (method, url, **kwargs):
        DEFAULT_REQUESTS_TIMEOUT = (5, 15)
        if 'timeout' not in kwargs:
            kwargs['timeout'] = DEFAULT_REQUESTS_TIMEOUT
    
        try:
            response = requests.request(method, url, **kwargs)
        except BaseException as exception:
            return (False, exception)
        return (True, response)