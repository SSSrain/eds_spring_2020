import numpy as np
from scipy.stats import poisson
from scipy.stats import bernoulli
import random
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

'''Поскольку n нигде явно не указано, выбираю, какое мне нравится\n
   Полагаю, больше 10 часов бега - издевательство над животными, поэтому ставлю n=10'''

n = 10
N = pow(10,4)

winner = {0:'Winnie', 1:'Piglet', 2:'Rabbit', 3:'Ia'}


matr = np.zeros(N*4*n)
matr = matr.reshape(N,4,n)


for index ,v in np.ndenumerate(matr):

    if index[1] % 4 == 0:
        k = random.expovariate(1)
        matr[index] = k
    elif index[1] % 4 == 1:
        k = np.random.normal(1,1)
        matr[index] = k
    elif index[1] % 4 == 2:
        k = poisson.rvs(1, size=1)[0]
        matr[index] = k
    elif index[1] % 4 == 3:
        k = bernoulli.rvs(0.5, size=1)[0]
        matr[index] = k*2


sum_matr = matr.sum(axis = 2)

result_arr = np.argmax(sum_matr, axis = 1)

def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]


result_list = list(result_arr)
winnie_cnt = result_list.count(0)
piglet_cnt = result_list.count(1)
rabbit_cnt = result_list.count(2)
ia_cnt = result_list.count(3)


print('{} has the most wins: {}'.format(winner[most_frequent(result_arr)], result_list.count(most_frequent(result_arr))))


df = pd.DataFrame({'Name':['Winnie', 'Piglet', 'Rabbit', 'Ia'],
                   'Victories':[winnie_cnt, piglet_cnt, rabbit_cnt, ia_cnt]
                   } ,index= ['W','P','R','I'])


fig, ax = plt.subplots()
ax.bar(df['Name'], df['Victories'])
ax.set_facecolor('#f3da0b')
fig.set_facecolor('#d5b3f5')
ax.set_xlabel('participants')
ax.set_ylabel('number of victories')
plt.title('number of victories depends on the participants')
plt.show()



'''Part 2'''
sum_matr2 = np.zeros(N*2)
sum_matr2 = sum_matr2.reshape(N,2)
sum_matr2[:,:1] = sum_matr[:,:1] + sum_matr[:,1:2]
sum_matr2[:,1:2] = sum_matr[:,2:3] + sum_matr[:,3:]

result_arr2 = np.argmax(sum_matr2, axis = 1)
result_list2 = list(result_arr2)

w_p_cnt = result_list2.count(0)
r_i_cnt = result_list2.count(1)

df2 = pd.DataFrame({'Pairs':['Winnie + Piglet', 'Rabbit + Ia'],
                   'Victories':[w_p_cnt, r_i_cnt]
                   } ,index= ['W+P', 'R+I'])


fig2, ax2 = plt.subplots()
ax2.bar(df2['Pairs'], df2['Victories'])
ax2.set_facecolor('#f3da0b')
fig2.set_facecolor('#d5b3f5')
ax2.set_xlabel('participants')
ax2.set_ylabel('number of victories')
plt.title('number of victories depends on the participants')
plt.show()
