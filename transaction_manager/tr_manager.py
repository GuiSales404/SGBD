from transaction import Tr
from lock_manager import lockManager

class trManager():
  
  def __init__(self): 
    self.controlMethod = input('Type your deadlock control method (wound-wait | wait-die): ')
    self.lockManager = lockManager(self, self.controlMethod)
    self.Timestamp = 0
    self.wait_q = [] #Wait_queue
    self.list_transactions = []
    self.list_rollback = []
    return

  def addOperation(self,operationType,transactionID, filename):
    teste = list(filter(lambda transation: transation.id == transactionID, self.list_transactions))
    if len(teste) > 0 and teste[0].state == 'active':
      if operationType == 'r':
          print('\n -- EXECUTANDO INSTRUCAO: ',operationType,transactionID,"(",filename,")\n")
          result = self.lockManager.addOperation(list(filter(lambda transation: transation.id == transactionID, self.list_transactions))[0], filename, "CP","r")
          if result == 1:
            print('transação de id', transactionID,'lendo o arquivo', filename,"\n")
          #printar wait_q
          
          print("ESTADO DA BLOCK_KEY: \n")
          if(len(self.lockManager.blockList) > 0):
            for transactionBlock in self.lockManager.blockList:
              print("( ",transactionBlock[1], " ",transactionBlock[0]," ",transactionBlock[2].id,")\n")
          else:
            print("VAZIO")
          print("\nESTADO DA AWAIT_Q: \n")
          if(len(self.wait_q) > 0):
            for transactionAwait in self.wait_q:
              print("A TRANSACAO DE ID: ",transactionBlock[2].id, " ESTA EM MODO DE AWAIT")
          else:
            print("VAZIO")
          print("\nESTADO DO ROLLBACK_Q: \n")
          if(len(self.list_rollback) > 0):
            for transactionRollback in self.list_rollback:
              print("A TRANSACAO DE ID: ",transactionRollback, " ESTA EM MODO DE ROLLBACK")
          else:
            print("VAZIO") 
          print("\n")
          return 0
            
      elif operationType == 'w':
          print('\n -- EXECUTANDO INSTRUCAO: ',operationType,transactionID,"(",filename,")\n")
          result = self.lockManager.addOperation(list(filter(lambda transation: transation.id == transactionID, self.list_transactions))[0], filename, "EX","w")
          if result == 1:
            print('id de transação ', transactionID,'escrevendo no arquivo ', filename)

         
          print("ESTADO DA BLOCK_KEY: \n")
          if(len(self.lockManager.blockList) > 0):
            for transactionBlock in self.lockManager.blockList:
              print("( ",transactionBlock[1], " ",transactionBlock[0]," ",transactionBlock[2].id,")\n")
          else:
            print("VAZIO")
          print("\nESTADO DA AWAIT_Q: \n")
          if(len(self.wait_q) > 0):
            for transactionAwait in self.wait_q:
              print("A TRANSACAO DE ID: ",transactionBlock[2].id, " ESTA EM MODO DE AWAIT")
          else:
            print("VAZIO")
          print("\nESTADO DO ROLLBACK_Q: \n")
          if(len(self.list_rollback) > 0):
            for transactionRollback in self.list_rollback:
              print("A TRANSACAO DE ID: ",transactionRollback, " ESTA EM MODO DE ROLLBACK")
          else:
            print("VAZIO") 
          print("\n")
        
          # quando der rollback
          return 0
    elif len(list(filter(lambda transation: transation.id == transactionID, self.list_transactions))) > 0 and list(filter(lambda transation: transation.id == transactionID, self.list_transactions))[0].state == 'rollback':
      print("Instrucao vai para rollback!!!")
      
      return
    elif len(list(filter(lambda transation: transation.id == transactionID, self.list_transactions))) > 0 and list(filter(lambda transation: transation.id == transactionID, self.list_transactions))[0].state == 'await':
      print("Ocorreu uma falha!")
      
      list(filter(lambda transation: transation.id == transactionID, self.list_transactions))[0].add_operation((operationType,transactionID,filename))  
      return 1
    
  def addTransaction(self,transactionID, action):
    print('\n -- EXECUTANDO INSTRUCAO: BT',"(",transactionID,")\n")
    print('Criando nova transação de id ', transactionID)
    transaction = Tr(transactionID,self.Timestamp,action)
    self.Timestamp += 1
    self.list_transactions.append(transaction)
    return

  def removeTransaction(self, transactionID):
     print('\n -- EXECUTANDO INSTRUCAO: C',"(",transactionID,")\n")
     if len(list(filter(lambda transation: transation.id == transactionID, self.list_transactions))) > 0 and list(filter(lambda transation: transation.id == transactionID, self.list_transactions))[0].state == 'active':
      print('transação de id ', transactionID, 'finalizada')
      self.list_transactions = list(filter(lambda transaction: transaction.id != transactionID, self.list_transactions))
      return
     else:
      print('falha (possui operacoes incompletas)')
      if len(list(filter(lambda transation: transation.id == transactionID, self.list_transactions))) > 0:list(filter(lambda transation: transation.id == transactionID, self.list_transactions))[0].add_operation(('C',transactionID," "))
      return
    
