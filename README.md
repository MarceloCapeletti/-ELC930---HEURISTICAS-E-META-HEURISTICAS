# PROPOSTA DE SOLUÇÃO DO PROBLEMA DE SEQUENCIAMENTO EM PROCESSADORES PARALELOS IDÊNTICOS ATRAVÉS DE HEURISTICAS E METAS HEURISTICAS 

# Código desenvolvido durante a disciplina ELC930 do PPGEP-UFSM

O presente instrumento tem a objetivo de abordar o problema de Sequenciamento (Scheduling), 
do qual pode ser representado por P | tpds | Cmax, assim sendo, caracteriza se pelo sequenciamento n tarefas a m processadores paralelos idênticos

1 ALOCAÇÃO INICIAL ( FASE 1) 

O trabalho utilizara como (Solução Inicial), a resolução da Busca Local com o algoritmo Best Fit, onde os passos serão:  
•	Passo 1: Execute o algoritmo BEST FIT e armazene a solução encontrada como solução incumbente e seu valor de função objetivo como limitante superior.  
•	Passo 2: Calcule o limitante inferior.  
•	Passo 3: Vá para a FASE 2 (Fase Busca Local)  

3.2 FASE BUSCA LOCAL  (FASE 2)

•	Passo 1: Encontra-se a máquina com maior (A) e menor (B) custo. 
•	Passo 2: Seleciona-se aleatoriamente uma tarefa alocada na máquina A. 
•	Passo 3: Seleciona-se aleatoriamente uma tarefa alocada na máquina B. 
•	Passo 4: Realiza-se a permuta de tarefas selecionadas entre as máquinas; 
•	Passo 5: Se solução antes da permuta for maior que solução após a permuta, admite-se que solução após a permuta é a nova solução incumbente, caso contrário, realiza-se novamente as etapas 1,2 até o limite de 300 trocas, ou 100 trocas sem aprimoramento. 

3.3	FASE BUSCA TABU (FASE 3) PÓS OTIMIZAÇÃO

•	Passo 1: Escolhe a melhor e a pior máquinas
•	Passo 2: Sorteia tarefas a e b dentro destas duas máquinas
•	Passo 3: Verifica se a troca oferece melhora
•	Se sim, verifica se está na lista tabu
•	Se está na lista tabu, verifica o critério de aspiração
•	Se ganho > critério de aspiração
•	Realiza a troca
•	Contador de trocas por critério de aspiração + +
•	Vida de todos os registros da busca tabu - - 
•	Remove os registros da lista com vida 0
•	Renova a vida para n iterações caso o critério de aspiração tenha sido utilizado
•	Se ganho < ou = critério de aspiração 
•	não realiza a troca
•	Contador Sorteios ++ 

•	Se não está na lista tabu
•	Realiza a troca
•	Decrementa 1 na vida de todos os registros da busca tabu
•	Remove os registros da lista com vida 0
•	Adiciona a troca na lista tabu com uma vida de n iterações

•	Se não,
•	adiciona o par na lista de critérios sorteados 
•	Contador Sorteios ++ 

•	Passo 4: Se contador de sorteios = m sorteios sem melhora, 
  
•	Realiza a troca com melhor resultado dentro das sorteadas (considerar lista tabu neste ponto?)
•	Decrementa 1 na vida de todos os registros da busca tabu
•	Remove os registros da lista com vida 0
