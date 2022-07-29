class lockManager():
#  a variavel operation e mesmo necessaria?
  def __init__(self, tr_manager, controlMethod):
      self.tr_manager = tr_manager
      self.controlMethod = controlMethod
      self.lock = ""
      self.blockList = []

  def waitDieMethod(self,oldTransaction, actualTransaction, filename, lockType, operation):
    print(" - VAMOS USAR O METODO WAIT-DIE\n")
    if oldTransaction.ts > actualTransaction.ts:
      print(" - SETANDO ESTADO DA TRANSACAO DE ID: ",   actualTransaction.id ," PARA AWAIT\n")
      actualTransaction.operations.append((operation,actualTransaction.id,filename))
      self.tr_manager.wait_q.append((lockType, filename, actualTransaction))
      posT = self.tr_manager.list_transactions.index(actualTransaction)
      if(posT != -1):
        self.tr_manager.list_transactions[posT].setState('await')
    else: 
      print(" - SETANDO ESTATO DA TRANSACAO DE ID: ",actualTransaction.id," PARA ROLLBACK\n")
      posT = self.tr_manager.list_transactions.index(actualTransaction)
      if(posT != -1):
        self.tr_manager.list_transactions[posT].setState('rollback')
        self.tr_manager.list_rollback.append(actualTransaction.id)
 
  def woundWaitMethod(self,oldTransaction, actualTransaction, filename, lockType, operation):
    print(" - VAMOS USAR O METODO WOUND-WAIT")
    if oldTransaction.ts > actualTransaction.ts:
      print(" - SETANDO ESTATO DA TRANSACAO DE ID: ",oldTransaction.id," PARA ROLLBACK\n")
      posT = self.tr_manager.list_transactions.index(oldTransaction)
      if(posT != -1):
        self.tr_manager.list_transactions[posT].setState('rollback')
        self.tr_manager.list_rollback.append(oldTransaction.id)
    else: 
      print(" - SETANDO ESTADO DA TRANSACAO DE ID: ", actualTransaction.id ," PARA AWAIT\n")
      actualTransaction.operations.append((operation,actualTransaction.id,filename))
      self.tr_manager.wait_q.append((lockType, filename, actualTransaction))
      posT = self.tr_manager.list_transactions.index(actualTransaction)
      if(posT != -1):
        self.tr_manager.list_transactions[posT].setState('await')

  
  def addOperation(self,transaction, filename, lockType, operation):
    transactionBlock = [item for item in self.blockList if item[1] == filename]
    # tratando cada um dos casos de borda para uma operacao de acesso a um arquivo
    if len(list(transactionBlock)) == 0 :
      self.blockList.append((lockType, filename, transaction, operation))
      return 1
    else:
      if len(transactionBlock) == 1 and lockType == "EX" and len(list(filter(lambda transationBlock: transationBlock[0] == 'CP', transactionBlock))) != 0 and (transactionBlock[0][2].id == transaction.id):
        return 1
      if len(transactionBlock) > 1:
        print("AVISO: EXISTE MAIS DE UMA TRANSACAO ACESSANDO ESTE ARQUIVO")
        if lockType == "CP" and len(list(filter(lambda transationBlock: transationBlock[0] == 'EX', transactionBlock))) != 0 and (transactionBlock[0][2].id == transaction.id):
          print("AVISO: O ARQUIVO EM QUESTAO ESTA EM MODO COMPARTILHADO COM MAIS DE UMA OUTRA TRANSACAO")
          
        if lockType == "EX" and len(list(filter(lambda transationBlock: transationBlock[0] == 'CP', transactionBlock))) != 0  and (transactionBlock[0][2].id == transaction.id):
          print("AVISO: O ARQUIVO EM QUESTAO ESTA EM MODO EXCLUSIVO COM MAIS DE UMA OUTRA TRANSACAO")
          
      if lockType == "EX" and transactionBlock[0][0] == "EX":
        print("JA EXISTE UMA TRANSACAO ACESSANDO ESTE ARQUIVO DE MODO EXCLUSIVO")
        return 0;
      if (lockType == "CP" and transactionBlock[0][0] == "CP") and  transactionBlock[0][3] == 'r':
        self.blockList.append((lockType, filename, transaction, operation))
        return 1
      if(lockType == "CP" and  transactionBlock[0][0] == "EX") and  (transactionBlock[0][1] == filename) and (transactionBlock[0][2].id == transaction.id):
        self.blockList.append((lockType, filename, transaction, operation))
        return 1
      if self.controlMethod == 'wait-die':
         self.waitDieMethod(transactionBlock[0][2], transaction, filename, lockType, operation)
      elif self.controlMethod == 'wound-wait':
         self.woundWaitMethod(transactionBlock[0][2], transaction, filename, lockType, operation)
      return 0



