class Request:
  def __init__(self, method: str, path: str, body: bytes = b"", headers: dict[str,str] | None = None):
    self.method = method
    self.path = path
    self.body = body
    self.headers = headers or {}
    #in the request the session are given by user or the browser
    self.sid: str | None = None

    if "Cookie"  in self.headers:
      cookies = self.headers["Cookie"].split("; ")
      for cookie in cookies:
        if cookie.startswith("sid="):
          self.sid = cookie.split("=",1)[1]
          break