Desenvolvimento de uma prova de conceito de um sistema multiagente para análise de crédito utilizando LangGraph, simulando fluxos reais de validação, compliance e tomada de decisão financeira.# credit-ai-agent


Primeiro, comecei procurando dataset que poderiam me ajudar nesse agente:
''''
pip install ucimlrepo

'''

importar o projeto
''''
from ucimlrepo import fetch_ucirepo 
  
# fetch dataset 
statlog_german_credit_data = fetch_ucirepo(id=144) 
  
# data (as pandas dataframes) 
X = statlog_german_credit_data.data.features 
y = statlog_german_credit_data.data.targets 
  
# metadata 
print(statlog_german_credit_data.metadata) 
  
# variable information 
print(statlog_german_credit_data.variables) 
'''