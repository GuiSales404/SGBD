#O fluxo do programa vai ser, cria-se a classe log, log list será preenchido com toda a historia do arquivo
#O list_log vai receber todas as linhas mesmo, para salvar essa história.
#O list_commit vai receber todas as alterações que comitaram 
#O list_undo vai receber todas as alterações que não comitaram, para ter essa informação, ele vai receber todas as ações(igual o list_log) contudo, quando finalizar o arquivo será removido todas as transações que estão também na list_commit
#Obs: Perceba que list_undo união list_commit = list_log
#list_file vai receber todos os arquivos criados durante a história, antes de criar um arquivo é necessário verificar se ele já existe na lista, caso exista, adiciona só a transação que está acessando ele
