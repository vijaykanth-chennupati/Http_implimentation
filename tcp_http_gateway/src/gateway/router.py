from typing import  Union, Callable
from response import Response
from request import Request

Handler = Union[Callable[[],Response],Callable[[Request],Response]]
# some handlers does need a parameter and some dont

class Router:
  def __init__(self):
    self.routes: dict[tuple[str,str], Handler]={}
  
  def add(self, method: str, path: str, handler: Handler):
    self.routes[(method,path)] = handler
  
  def dispatch(self, req: Request) -> Response:
    handler= self.routes.get((req.method, req.path))
    #finding the handler
    if handler is None:
      return Response(404, b"Not Found")
    return handler(req)
  # handlers module does not have to import so used directly where routes dict storing name along with module

  #it is better to have same shape to avoid return on codition of parameter length check
