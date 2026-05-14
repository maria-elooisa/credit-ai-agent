from ucimlrepo import fetch_ucirepo

statlog_german_credit_data = fetch_ucirepo(id=144)
X = statlog_german_credit_data.features
y = statlog_german_credit_data.target
 
print(statlog_german_credit_data.metadata)
print(statlog_german_credit_data.variables)