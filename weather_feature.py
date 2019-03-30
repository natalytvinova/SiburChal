import urllib
from bs4 import BeautifulSoup
import requests as req
import fake_useragent as fa
import math
import pickle
ua = fa.FakeUserAgent()
print(ua.random)

temp_dict = {}
for y in range(2016, 2018):
    for m in range(1, 13):
        if y == 2016:
            m = 10
        quote_page = 'https://www.gismeteo.ru/diary/4590/' + str(y) + '/' +str(m)
        res = req.get(quote_page, headers={'User-Agent': ua.random})
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'lxml')
        else:
            print(res.status_code)
        temp_temp = soup.find_all('td', class_='first_in_group')
        temp = []
        for t in range(1, len(temp_temp) + 1):
            if t % 2 == 1:
                try:
                    temp.append(int(temp_temp[t - 1].get_text()))
                except:
                    temp.append(-10000)
        for t in range(0, len(temp)):
            if temp[t] == -10000:
                    try:
                        temp[t] = round((temp[t - 1] + temp[t + 1]) / 2)
                    except:
                        temp[t] = np.mean(temp)
            temp_dict[str(y) + '-' + str(m) + '-' + str(t + 1)] = temp[t]
    
quote_page = 'https://www.gismeteo.ru/diary/4590/2018/1'
res = req.get(quote_page, headers={'User-Agent': ua.random})
if res.status_code == 200:
    soup = BeautifulSoup(res.text, 'lxml')
else:
    print(res.status_code)
temp_temp = soup.find_all('td', class_='first_in_group')
temp_temp = temp_temp[:16]
temp = []
for t in range(1, len(temp_temp) + 1):
    if t % 2 == 1:
        try:
            temp.append(int(temp_temp[t - 1].get_text()))
        except:
            temp.append(-10000)
for t in range(0, len(temp)):
    if temp[t] == -10000:
            try:
                temp[t] = round((temp[t - 1] + temp[t + 1]) / 2)
            except:
                temp[t] = np.mean(temp)
    temp_dict['2018-1-' + str(t + 1)] = temp[t]
pickle.dump( temp_dict, open( "temperatures.p", "wb" ) )
temp_dict
