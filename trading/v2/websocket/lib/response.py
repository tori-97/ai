class SocketResponse():
    def __init__(self, data) -> None:
        self._data = self._parse_request(data)

    def _parse_request(self, data):
        tmp = data.split(b"\r\n\r\n")

        req = {
            'method': None,
            'query': None,
            'version': None,
            'headers': None,
            'data': None,
            'raw': data
        }

        headers = {}

        if len(tmp) > 1:
            _headers = tmp[0].split(b"\r\n")
            method, query, version = _headers[0].decode().split(" ")
            _header = _headers[1::]
            
            for i in _header:
                key, val = i.decode().split(": ")
                key, val = key.strip(), val.strip()

                headers[key.lower()] = val

            req['method'] = method
            req['query'] = query
            req['version'] = version
            req['headers'] = headers
            req['data'] = tmp[1::]

        return req

    @property
    def method(self): return self._data.get("method")
    
    @property
    def query(self): return self._data.get("query")
    
    @property
    def version(self): return self._data.get("version")
    
    @property
    def headers(self): return self._data.get("headers")
    
    @property
    def data(self): return self._data.get("data")
    
    @property
    def raw(self): return self._data.get("raw")


    def __repr__(self):
        return f"<Response: {self.method}| {self.query} | {self.version}>"