import uuid

class Sessionstore:
  def __init__(self):
    self._data : dict[str, dict] = {}

#assign the new session id
  def new_id(self) -> str:
    return str(uuid.uuid4())
  
  def has(self, session_id: str) -> bool:
    return session_id in self._data
  #return a bool value based of return condition

  def get(self, session_id: str) -> dict:
    return self._data.get(session_id)