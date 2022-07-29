from tr_manager import trManager
transaction = trManager()
count_all_instructions = 0
count_all_instructions_by_history = 0

def read_instruction(id,count_instructions):
  print('\n')
  count = count_all_instructions
  arq = open("in.txt")
  linhas = arq.readlines()
  allEntries = []
  
  if id == -1:
    print("\n  =-=-= INCIANDO LEITURA DAS INSTRUCOES PELO SCHEDULER  =-=-= ")
    for linha in linhas:
      print('execução', count, ': ',linha)
      allEntries.append(list(linha))
      count += 1
  else:
    print("\n =-=-= Executando as instrucoes da transacao de id: ",id, '=-=-= ')
    for linha in linhas:
      if linha[0] == 'B' and linha[3] == id:
        print('execução', count, ': ',linha)
      elif linha[0] == 'C' and linha[2] == id:
        print('execução', count, ': ',linha)
        allEntries.append(list(linha))
        count += 1
      elif linha[1] == id:
        print('execução', count, ': ',linha)
        allEntries.append(list(linha))
        count += 1
  
  print("\n =-=-= Iniciando as operacoes do scheduler no SGBD por instrucao =-=-= \n")
  for x in range(count):
    if allEntries[x][0] == 'B':
        transaction.addTransaction(allEntries[x][3], 'active')
        continue
    elif allEntries[x][0] == 'C':
        transaction.removeTransaction(allEntries[x][2])
        continue
    else: 
        result = transaction.addOperation(allEntries[x][0],allEntries[x][1], allEntries[x][3])
        if result == 0:
          continue
  return count

count_all_instructions_by_history = read_instruction(-1,0)
print("\n =-=-= AGORA O SGBD VAI VERIFICAR SE EXISTE TRANSACOES EM AWAIT E ROLLBACK\n =-=-= ")

if len(transaction.wait_q) > 0:
  for x in transaction.wait_q:
    print('Transação de id:',x[2].id,' Em estado de:',x[2].state)
    print("Executando operações em await da transação de ID: ",x[2].id)
    for operation in x[2].getOperations():
      if(operation[0] != 'C'):
        print(operation[0],operation[1],"(",operation[2],") sucesso")
      else:
        print(operation[0],operation[1],"(",operation[2],") finalizada")
    # if x  in transaction.wait_q:transaction.wait_q.remove(x)
        
if len(transaction.list_rollback) > 0:
  print("Transações em rollback:")
  transaction.lockManager.blockList = []
  for x in transaction.list_transactions:
    if x.state == 'rollback':
      print('Transação de id:',x.id,'Em estado de:',x.state)
      list(filter(lambda transation: transation.id == x.id, transaction.list_transactions))[0].state = 'active'
      count_all_instructions_by_history = read_instruction(x.id,count_all_instructions_by_history)
      if x in transaction.list_transactions: transaction.list_transactions.remove(x)
      
      
 