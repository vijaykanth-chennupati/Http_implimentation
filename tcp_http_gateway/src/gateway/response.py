class Response:
  #constuctor for the response class 
  def __init__(self, status: int = 200, body: bytes= b"OK"):
    self.status = status
    self.body = body
    self.headers = {
      "content_length": str(len(body)),
      "content_type": "text/plain",
      "connection": "close"
    }

  def to_bytes(self):
    #trying to build the response

    #stutus line
    status_line = f"HTTP/1.1 {self.status} OK\r\n"
    #header using the loop on headers dictionary
    headers = "".join(f"{key}: {value}\r\n" for key, value in self.headers.items())
    return (status_line + headers + "\r\n").encode() + self.body



'''
requester = Response()
print(requester.to_bytes())
'''
