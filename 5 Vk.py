'''Некоторые отрывки кода взяты из лекций
Антиплагиат, выйди отсюда розбiйник!!!'''

import requests
import numpy as np
import  time
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm


version = '5.103'
group_id = 'jasonstatham_officialgroup'
bdate = 'bdate'

with open('secret_token.txt') as f:
    token = f.read()


def vkDownload(method, parameters, token=token, version=version):

    url = 'https://api.vk.com/method/{method}?{parameters}&access_token={token}&v={version}'
    url = url.format(method=method, parameters=parameters, token=token, version=version)
    response = requests.get(url).json()

    return response


def getGroupMembers(group_id):

    count = vkDownload('groups.getMembers', 'group_id=' + group_id)['response']['count']

    n = int(np.ceil(count / 1000))

    members = []

    for i in range(n):
        current_members = vkDownload('groups.getMembers', 'group_id=' + group_id + '&offset=' + str(1000 * i))
        members.extend(current_members['response']['items'])
        time.sleep(0.4)

    return members


jason1 = getGroupMembers(group_id)

dict_dates = {}
Count = vkDownload('groups.getMembers', 'group_id=' + group_id)['response']['count']
N = Count // 50

for i in tqdm(range(N)):
    jason11 = jason1[(i * 50): (i * 50 + 49)].copy()

    jason1_str = ','.join([str(user) for user in jason11])

    fun = vkDownload('users.get', 'user_ids={}&fields={}'.format(jason1_str, bdate))['response']

    time.sleep(0.4)

    for el in fun:
        try:
            if len(el['bdate']) > 5:
                dict_dates.update({el['id']: el['bdate'][:-5]})
            else:
                dict_dates.update({el['id']: el['bdate']})
        except:
            pass



jason11 = jason1[(N * 50):].copy()
jason1_str = ','.join([str(user) for user in jason11])
fun = vkDownload('users.get', 'user_ids={}&fields={}'.format(jason1_str, bdate))['response']

for el in fun:
    try:
        if len(el['bdate']) > 5:
            dict_dates.update({el['id']: el['bdate'][:-5]})
        else:
            dict_dates.update({el['id']: el['bdate']})
    except:
        pass


dict_num_date = {}
dict_with_months = {i + 1 : 0 for i in range(12)}
cnt = 0
for k, v in dict_dates.items():
    dict_num_date.update({cnt : v})
    v = dict_dates[k].split('.')[1]
    dict_with_months[int(v)] += 1
    cnt +=1


df = pd.DataFrame({'Month':[i for i in dict_with_months.keys()] , 'Values': [i for i in dict_with_months.values()]})

fig, ax = plt.subplots()
ax.bar(df['Month'], df['Values'])
ax.set_facecolor('#f3da0b')
fig.set_facecolor('#d5b3f5')
ax.set_xlabel('months')
ax.set_ylabel('number of birthdays')
plt.title('number of birthdays depends on the month')
plt.show()


'''в задании сказано держать дату рождения и id в одном месте, и это - dict_dates - всегда можно посмотреть эти данные
но мне этим пользоваться не нравится, поэтому я делаю другие словари с другими парами ключ-значение'''
M = len(dict_num_date) // 50
counter = 0
for m in range(M):
    for i in range(m*50, m*50 + 49):
        if dict_num_date[i] == dict_num_date[i+1]:
            counter +=1
            break

for i in range(M*50, len(dict_num_date)-1):
    if dict_num_date[i] == dict_num_date[i + 1]:
        counter += 1
        break

print('Вероятность совпадений др в 1 день в данном паблике у людей с выставленной датой рождения: {}%'.format(round(counter/(M+1)*100, 4)))