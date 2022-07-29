from log import Log

logFile = Log()

arq = open("in2.txt")
instrucoes = []
linhas = arq.readlines()
count = 0
for linha in linhas:
    instrucoes.append(linha.split('|'))

for instrucao in instrucoes:
    count += 1
    logFile.addTransactionToLog(instrucao)

# for transaction in logFile.list_transaction:
#     if transaction.status == "Rollback":
#         print('=-=-=-=-=-==-=-=-=-=-==-=-=-=-=-==-=-=-=-=-=')
#         print(' TRANSACAO ', transaction.Tn, ' ESTA EM ESTADO DE ROLLBACK')
#         print('=-=-=-=-=-==-=-=-=-=-==-=-=-=-=-==-=-=-=-=-=')
#         indexTransaction = list(filter(lambda transactionL: transactionL.Tn == transaction.Tn ,logFile.list_transaction))
#         if len(indexTransaction) == 1:
#           logFile.list_transaction[logFile.list_transaction.index(indexTransaction[0])].setStatus('active')
#         for operation in list(reversed(transaction.operations)):
#           filterFile = list(filter(lambda file: file.name == operation[0],logFile.list_file))
#           if len(filterFile) == 1:
#             logFile.list_file[logFile.list_file.index(filterFile[0])].setValue(operation[1])
#         print('=-=-=-=-=-==-=-=-=-=-==-=-=-=-=-==-=-=-=-=-=')
#         print(' MOSTRANDO OS VALORES DOS ARQUIVOS')
#         print('=-=-=-=-=-==-=-=-=-=-==-=-=-=-=-==-=-=-=-=-=')
#         for file in logFile.list_file:
#             print(file.name, " - ", file.value, ' \n')

for transaction in logFile.list_transaction:
  if transaction.status == "active":
    # print('=-=-=-=-=-==-=-=-=-=-==-=-=-=-=-==-=-=-=-=-=')
    # print(' TRANSACAO ', transaction.Tn, ' VAI SOFRER UNDO')
    # print('=-=-=-=-=-==-=-=-=-=-==-=-=-=-=-==-=-=-=-=-=')
    for operation in list(reversed(transaction.operations)):
      filterFile = list(filter(lambda file: file.name == operation[0],logFile.list_file))
      if len(filterFile) == 1:
        logFile.list_file[logFile.list_file.index(filterFile[0])].setValue(operation[1])
        
print('=-=-=-=-=-==-=-=-=-=-==-=-=-=-=-==-=-=-=-=-=')
print(' MOSTRANDO OS VALORES DOS ARQUIVOS')
print('=-=-=-=-=-==-=-=-=-=-==-=-=-=-=-==-=-=-=-=-=')
for file in logFile.list_file:
  print(file.name, " - ", file.value, ' \n')