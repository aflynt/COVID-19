#!/home/flyntga/anaconda3/bin/python
from datetime import date
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, WEEKLY, WE

import csv
import matplotlib.pyplot as plt
import numpy as np

csv.register_dialect(\
    'mydialect', delimiter = ',',quotechar = '"', doublequote = True, \
    skipinitialspace = True, lineterminator = '\n' )

pwd = '/home/flyntga/git/COVID-19/csse_covid_19_data/csse_covid_19_time_series'
#filename = 'time_series_19-covid-Confirmed.csv'
filename = 'time_series_covid19_confirmed_global.csv'

#   0          1      2     3     4        N
# Province, Country, LAT, LONG, DATE0 ... DATE N

def getCountryData(key='Italy'):
  dates = []
  cdata = []
  with open(pwd+'/'+filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
  
    #print(dates)
    dates = next(csvreader)[4:]
  
    # find the row of interest aka keyCountry
    for row in csvreader:
      if row[1].find(key) != -1:
        cdata.append(row[4:])
        #print('LOOKING for <{}> FOUND <{}>'.format(key,row[0:1]))

  return dates,cdata

today = date.today()
def get_date_list(dates):
  # try to parse the dates
  dlist = []
  for d in dates:
    dvals = d.split('/')
    mo = int(dvals[0])
    dy = int(dvals[1])
    yr = int(2020)
    dobject = date(day=dy,month=mo,year=yr)
    delta = int((dobject - today).days)
    dlist.append(delta)
  return dlist

def makeInts(strList):
  IL = strList

  ncol = len(strList[0])
  nrow = len(strList)
  for i in range(0, nrow):
    for j in range(len(strList[i])):
      s = strList[i][j]
      if s == '':
        IL[i][j] = IL[i][j-1]
      else:
        IL[i][j] = int(s)
  return IL

def sum_cols(square):
  output = []
  ncol = len(square[0])
  for i in range(0, ncol):
    total = 0
    for row in square:
      total += row[i]
    output.append(total)
  return output


# CHOOSE COUNTRIES
S_ge = 'Germany'
S_us = 'US'
S_it = 'Italy'
S_ch = 'China'
S_ko = 'Korea, South'
S_uk = 'United Kingdom'
S_fr = 'France'
dates,C_ge = getCountryData(S_ge)
dates,C_us = getCountryData(S_us)
dates,C_it = getCountryData(S_it)
dates,C_ch = getCountryData(S_ch)
dates,C_ko = getCountryData(S_ko)
dates,C_uk = getCountryData(S_uk)
dates,C_fr = getCountryData(S_fr)

dlist = get_date_list(dates)

C_it = sum_cols(makeInts(C_it))
C_ge = sum_cols(makeInts(C_ge))
C_us = sum_cols(makeInts(C_us))
C_ch = sum_cols(makeInts(C_ch))
C_ko = sum_cols(makeInts(C_ko))
C_uk = sum_cols(makeInts(C_uk))
C_fr = sum_cols(makeInts(C_fr))

# Remove today's data
rmtoday = False
#rmtoday = True
if (rmtoday):
  dlist = dlist[0:-1]
  C_it = C_it[0:-1]
  C_ge = C_ge[0:-1]
  C_us = C_us[0:-1]
  C_ch = C_ch[0:-1]
  C_ko = C_ko[0:-1]
  C_uk = C_uk[0:-1]
  C_fr = C_fr[0:-1]

#print('Country: {}, values: {}'.format(S_us, C_us))
#print('Country: {}, values: {}'.format(S_it, C_it))
#print('Country: {}, values: {}'.format(S_uk, C_uk))

## CURVE FIT ##
DAYS = 7
x = np.array(dlist[-7:])
y = np.array(C_us[-7:])
fit = np.polyfit(x, np.log(y), 1, w = np.sqrt(y))
A = np.exp(fit[1])
B = fit[0]
print(fit)
#print('A = {}, B = {}'.format(A,B))

xd = []
yd = []
for d in range(7):
  xd.append(d)
  yd.append(A*np.exp(B*d))

#print('yd = {}'.format(yd))

plt.plot(dlist,C_ge,"b",label=S_ge)
plt.plot(dlist,C_us,"k--",label=S_us)
plt.plot(dlist,C_it,"k",label=S_it)
plt.plot(dlist,C_ch,"g-.",label=S_ch)
plt.plot(dlist,C_ko,"b--",label=S_ko)
plt.plot(dlist,C_uk,"r",label=S_uk)
plt.plot(dlist,C_fr,"r-.",label=S_fr)
plt.plot(xd,yd,'k.',label='US-FIT')
plt.yscale("log")
plt.ylim(100,1e6)
plt.xlim(-35,7.01)
plt.xticks(np.arange(-35,7,7))
plt.xlabel('Days Since {}'.format(today))
plt.ylabel('Confirmed Cases')
plt.title('Covid-19 Cases')
plt.legend()
plt.grid(True)
plt.savefig("test.pdf")
plt.show()
