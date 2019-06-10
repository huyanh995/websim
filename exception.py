import random
from data import alldata, operators

data = alldata.data['ASI']
#ope = random.choice(operators.operators())
# for ope in operators.operators():
#     complete = ope[0].format(*random.sample(data, ope[1]))
#     print(complete)

# def get_combo_data(num, data):
#     # Get combination data from operators and datas.
#     # Input: num := number of {} in template. 
#     # data = data available according to each region.
#     rndData = []
#     for x in range(0,num):
#         ope = random.choice(operators.operators())
#         rndData.append(ope[0].format(*random.sample(data,ope[1])))
#     return rndData

# get_combo_data(3, data)
input = ['a', 'b']
string = "Here {} is {} and {}".format(*input, "c")
print(string)