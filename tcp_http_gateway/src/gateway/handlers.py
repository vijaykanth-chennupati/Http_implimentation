from request import Request
from response import Response
import json


html_login_form = b"""
<!doctype html>
<html>
  <head><meta charset="utf-8"><title>Login</title></head>
  <body>
    <h1>Login</h1>
    <form method="POST" action="/login">
      <label>Username: <input name="username" required></label>
      <button type="submit">Login</button>
    </form>
  </body>
</html>"""

def login_page(req: Request) -> Response:
  resp = Response(200, html_login_form)
  resp.headers["content_type"] = "text/html"
  return resp

def login(req: Request) -> Response:
  raw = req.body.decode().strip()
  if "username=" not in raw:
    return Response(400, b"bad request")
  else:
    username = raw.split("username=")[1]

  if not username:
    return Response(400, b"username required")
  
  #here by i am done by getting name
  
  if not hasattr(req, "session_store"):
    return Response(500, b"no session store available")
  
  sid = req.session_store.new_id()
  req.session_store._data[sid]={"username": username}

#creating the response by also setting the cookie
  resp = Response(200, f"logged in as {username}".encode())
  resp.headers["Set-Cookie"] = f"sid={sid}"
  return resp
    
  
  
def root(req: Request) -> Response:
  return Response()

def hello(req: Request) -> Response:
  if req.sid == None:
    payload = json.dumps({"message": "Hello, world!"})
    r = Response(200, payload.encode())
    r.headers["content_type"] = "application/json"
    return r
  if  not hasattr(req, "session_store"):
    return Response(500, b"no session store available")
  
  sessiondata = req.session_store.get(req.sid)
  
  payload = json.dumps({"message": f"Hello, {sessiondata['username']}!"})
  r = Response(200, payload.encode())
  r.headers["content_type"] = "application/json"
  return r


def echo(req: Request) -> Response:
  r = Response(200, req.body)
  return r
