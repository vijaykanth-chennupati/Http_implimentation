class HttpParser:
  def parse(self, data: bytes):
    sep = data.find(b"\r\n\r\n")
    if sep == -1:
       raise ValueError("incomplete headers")
    #header is the from beginning to the \r\n\r\n which is in sep
    head= data[:sep].decode("ascii")
    lines = head.split("\r\n")
    if not lines or " " not in lines[0]:
      raise ValueError("bad start line")
    
    parts = lines[0].split(" ")
    if len(parts) != 3:
      raise ValueError("bad start-line")
    method, path, version = parts[0], parts[1], parts[2]

# after finishin the start line we will have key values in the form of the srting need to convert it to dictionary

    headers: dict[str, str] = {}
    for raw in lines[1:]:
      if not raw:
        continue
      if ": " not in raw:
        raise ValueError("bad header line")
      #lets upack the list after spliting it by ": "
      k,  v = raw.split(": ", 1)
      headers[k.strip().title()] = v.strip()
      """ so for this loop i will getting and header output as {'Host': 'example.com', 'User-Agent': 'test'} """

      # lets make the body
      consumed = sep + 4
      body = b""
      if "Content-Length" in headers:
        try :
          n = int(headers["Content-Length"])
        except ValueError:
          raise ValueError("content length invalid")
        if len(data) - consumed < n:
          raise ValueError("incomplete body")
        body = data[consumed: consumed + n]

    return method, path, headers, body, consumed


  