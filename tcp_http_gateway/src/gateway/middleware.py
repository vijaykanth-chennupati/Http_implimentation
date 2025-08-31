from typing import Callable
from request import Request
from response import Response

Handler = Callable[[Request], Response]
#handler is one parameter function which takes Request and returns Response

def logging_middleware(handler: Handler) -> Handler:
  #logging middleware is recieving reference of the  router's dispatch method
  def wrapper(req: Request):
    resp = handler(req)
    print(f'{req.method} {req.path} -> {resp.status}')
    return resp
  return wrapper
  
  