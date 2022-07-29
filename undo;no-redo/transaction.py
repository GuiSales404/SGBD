class Transaction: 

  status = 'active'
  
  def __init__(self, Tn, operation):
    self.Tn = Tn
    self.operations = []
    self.status = 'active'
    self.operations.append(operation)

  def addNewOperation(self, newOperation):
    return self.operations.append(newOperation)
  
  def getTn(self):
    return self.Tn
  def getOperations(self):
    return self.operations
  def getStatus(self):
    return self.status

  def setStatus(self, status):
    self.status = status