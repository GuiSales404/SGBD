from transaction import Transaction
from file import File
class Log: 
  list_logs = [] #historia completa do log
  list_transactions_undo = [] #transacoes que sofrerao undo
  list_file = [] #lista de arquivos criados
  list_commit = [] #lista de arquivos que comitaram 
  
  def __init__(self):
    self.list_transaction = []
    self.list_undo = []
    self.list_file = []
    return

  def OperationType(self,instrucao,transactionChoosen):
    if instrucao[4] == 'c':
     
      self.list_transaction[transactionChoosen].setStatus('Committed')
      # salvar os dados das operacoes da transacao em seus files em list_file
      for operation in self.list_transaction[transactionChoosen].operations:
        # filterFiles = list(filter(lambda file: file.name == instrucao[5],self.list_file))
          for file in self.list_file:
            if file.name == operation[0]:
              print('commitou para ', operation[2])
              self.list_file[self.list_file.index(file)].setValue(operation[2])
              print('valor alterado no file: ',  self.list_file[self.list_file.index(file)].value)
        
    elif instrucao[4] == 'w':
      
      filterFile = list(filter(lambda file: file.name == instrucao[5],self.list_file))

      if len(filterFile) == 0:

        newFile = File(instrucao[5])
        self.list_file.append(newFile)
      else:
      #                                                            Objeto    |  ImgAnte   |   ImgPost
        self.list_transaction[transactionChoosen].addNewOperation((instrucao[5],instrucao[6],instrucao[7]))
    elif instrucao[4] == 'a':
      self.list_transaction[transactionChoosen].setStatus('Roll')
      self.list_undo.append(instrucao[5])

  def addFileToFileList(self, file):
    return self.list_file.append(file)
  
  def addTransationToUndoList(self, newLog):
    return self.list_undo.append(newLog)

  def removeTransactionOfUndoList(self, transactionCommited):
    indexTransaction = self.list_undo.index(transactionCommited)
    if indexTransaction != -1:
      self.list_undo.remove(transactionCommited)
  
  def addTransactionToLog(self, newLog):
    if newLog[5] != 'r':
      filterTransactionList = list(filter(lambda transaction: transaction.Tn == newLog[3],self.list_transaction))
      if len(filterTransactionList) == 0:
        
        filterFile = list(filter(lambda file: file.name == newLog[5],self.list_file))

        if len(filterFile) == 0:
          newFile = File(newLog[5])
          self.list_file.append(newFile)
        newTransaction = Transaction(newLog[3],(newLog[5],newLog[6],newLog[7]))
        self.list_transaction.append(newTransaction)
        return
      elif len(filterTransactionList) == 1 and filterTransactionList[0].Tn == newLog[3]: 
        self.OperationType(newLog,self.list_transaction.index(filterTransactionList[0]))
    

  def getUndoList(self):
    return self.list_undo
  def getLogList(self):
    return self.list_logs
  def getFileList(self):
    return self.list_file
  def getCommitList(self):
    return self.list_commit