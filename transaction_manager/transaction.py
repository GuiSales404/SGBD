  class Tr():
  def __init__(self, id, ts, state):
    self.id = id
    self.ts = ts
    self.state = state
    self.operations = []

  def setState(self, state):
    self.state = state

  def add_operation(self, newOperation):
    self.operations.append(newOperation)

  def getId(self):
    return self.id
  def getTs(self):
    return self.ts
  def getState(self):
    return self.state
  def getOperations(self):
    return self.operations