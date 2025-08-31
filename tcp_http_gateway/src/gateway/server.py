import socket
from request import Request
from response import Response
from parser import HttpParser
from router import Router
import handlers
import middleware
from session import Sessionstore

class TcpServer:
  def __init__(self, host: str='127.0.0.1', port: int= 8081):
    self.host = host
    self.port = port
    self.parser = HttpParser()
    self.router = Router()
    self.session_store = Sessionstore()

    # adding routes
    self.router.add("GET","/", handlers.root)
    self.router.add("POST","/echo", handlers.echo)
    self.router.add("GET","/hello", handlers.hello)
    self.router.add("GET","/login", handlers.login_page)
    self.router.add("POST","/login", handlers.login)
    self.dispatch = middleware.logging_middleware(self.router.dispatch)

  def start(self):
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server_socket:
      server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      server_socket.bind((self.host, self.port))
      server_socket.listen()
      print(f"Listenin  on {self.host}:{self.port}...")

      while True:
        conn, addr = server_socket.accept()
        with conn:
          print(f"connected by {addr}")
          #raw request data
          data =  conn.recv(65536)

          try:
            method, path, headers, body,_ = self.parser.parse(data)
            req = Request(method, path, body, headers)
            req.session_store = self.session_store
            print(f"Request: {req.method} {req.path} headers = headers={len(req.headers)} body={len(req.body)} sid={req.sid}B")
            print(req.session_store.get(req.sid))

            #instead of running here lets try to run in logging middleware so we can get response status also to log
          

            resp = self.dispatch(req)

          except ValueError as e:
            resp = Response(400, f"Bad Request: {e}".encode())
          
          conn.sendall(resp.to_bytes())