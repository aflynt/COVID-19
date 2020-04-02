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
filename = 'time_series_covid19_confirmed_US.csv'

#   0          1      2     3     4        N
# Province, Country, LAT, LONG, DATE0 ... DATE N
DATESTART = 11
NCOUNTY = 5
NSTATE = 6
NCOUNTRY = 7
NLABEL = 10

def getStateData(key='Tennessee'):
  dates = []
  cdata = []
  with open(pwd+'/'+filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
  
    #print(dates)
    dates = next(csvreader)[DATESTART:]
  
    # find the row of interest aka keyCountry
    for row in csvreader:
      if len(row) >= NSTATE:
        if row[NSTATE].find(key) != -1:
          cdata.append(row[DATESTART:])
          #print('LOOKING for <{}> FOUND <{}>'.format(key,row[0:NLABEL]))

  return dates,cdata

def getCountryData(key='Italy'):
  dates = []
  cdata = []
  with open(pwd+'/'+filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
  
    #print(dates)
    dates = next(csvreader)[DATESTART:]
    #print('KEY <{}> DATES <{}>'.format(key,dates))
  
    # find the row of interest aka keyCountry
    for row in csvreader:
      val = row[NSTATE]
      #print('KEY = {}, VAL = {}'.format(key,val))
      if row[NCOUNTRY].find(key) != -1:
        cdata.append(row[DATESTART:])
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

  ncol = 0
  nrow = len(strList)
  if nrow > 0:
    ncol = len(strList[0])
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
  ncol = 0
  if len(square) > 0:
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
S_tn = 'Tennessee'

#S_01 = 'Wyoming'
#S_02 = 'Wisconsin'
#S_03 = 'West Virginia'
S_04 = 'Washington'
#S_05 = 'Virgin Islands'
#S_06 = 'Virginia'
#S_07 = 'Vermont'
#S_08 = 'Utah'
S_09 = 'Texas'
#S_10 = 'Tennessee'
#S_11 = 'South Dakota'
#S_12 = 'South Carolina'
#S_13 = 'Rhode Island'
#S_14 = 'Puerto Rico'
#S_15 = 'Pennsylvania'
#S_16 = 'Oregon'
#S_17 = 'Oklahoma'
#S_18 = 'Ohio'
#S_19 = 'Northern Mariana Islands'
#S_20 = 'North Dakota'
#S_21 = 'North Carolina'
S_22 = 'New York'
#S_23 = 'New Mexico'
S_24 = 'New Jersey'
#S_25 = 'New Hampshire'
#S_26 = 'Nevada'
#S_27 = 'Nebraska'
#S_28 = 'Montana'
#S_29 = 'Missouri'
#S_36 = 'Mississippi'
#S_31 = 'Minnesota'
S_32 = 'Michigan'
#S_33 = 'Massachusetts'
#S_34 = 'Maryland'
#S_35 = 'Maine'
S_30 = 'Louisiana'
S_37 = 'Kentucky'
#S_38 = 'Kansas'
#S_39 = 'Iowa'
#S_40 = 'Indiana'
#S_41 = 'Illinois'
#S_42 = 'Idaho'
#S_43 = 'Hawaii'
#S_44 = 'Guam'
#S_45 = 'Grand Princess'
S_46 = 'Georgia'
S_47 = 'Florida'
S_48 = 'District of Columbia'
#S_49 = 'Diamond Princess'
#S_50 = 'Delaware'
#S_51 = 'Connecticut'
#S_52 = 'Colorado'
S_53 = 'California'
#S_54 = 'Arkansas'
#S_55 = 'Arizona'
#S_56 = 'American Samoa'
#S_57 = 'Alaska'
S_58 = 'Alabama'

pop_04 = 7.536e6    
pop_09 = 28.7e6
pop_22 = 19.453e6
pop_24 = 8.909e6
pop_30 = 4.66e6
pop_32 = 9.996e6
pop_37 = 4.468e6
pop_46 = 10.52e6
pop_47 = 21.3e6
pop_48 = 0.633427e6
pop_53 = 39.56e6
pop_58 = 4.888e6
pop_tn = 6.77e6
pop_us = 327.2e6

dates,C_ge = getCountryData(S_ge)
dates,C_us = getCountryData(S_us)
dates,C_it = getCountryData(S_it)
dates,C_ch = getCountryData(S_ch)
dates,C_ko = getCountryData(S_ko)
dates,C_uk = getCountryData(S_uk)
dates,C_tn = getStateData(S_tn)

#NEW
dates,C_04 = getStateData(S_04)
dates,C_09 = getStateData(S_09)
dates,C_22 = getStateData(S_22)
dates,C_24 = getStateData(S_24)
dates,C_30 = getStateData(S_30)
dates,C_32 = getStateData(S_32)
dates,C_37 = getStateData(S_37)
dates,C_46 = getStateData(S_46)
dates,C_47 = getStateData(S_47)
dates,C_48 = getStateData(S_48)
dates,C_53 = getStateData(S_53)
dates,C_58 = getStateData(S_58)

dlist = get_date_list(dates)

C_it = sum_cols(makeInts(C_it))
C_ge = sum_cols(makeInts(C_ge))
C_ch = sum_cols(makeInts(C_ch))
C_ko = sum_cols(makeInts(C_ko))
C_uk = sum_cols(makeInts(C_uk))
C_us = sum_cols(makeInts(C_us))
C_tn = sum_cols(makeInts(C_tn))

#NEW
C_04 = sum_cols(makeInts(C_04))
C_09 = sum_cols(makeInts(C_09))
C_22 = sum_cols(makeInts(C_22))
C_24 = sum_cols(makeInts(C_24))
C_30 = sum_cols(makeInts(C_30))
C_32 = sum_cols(makeInts(C_32))
C_37 = sum_cols(makeInts(C_37))
C_46 = sum_cols(makeInts(C_46))
C_47 = sum_cols(makeInts(C_47))
C_48 = sum_cols(makeInts(C_48))
C_53 = sum_cols(makeInts(C_53))
C_58 = sum_cols(makeInts(C_58))

Normalize = False
if Normalize:
  for i in range(len(C_04)):
    C_04[i] /= pop_04/perPPL
    C_09[i] /= pop_09/perPPL
    C_22[i] /= pop_22/perPPL
    C_24[i] /= pop_24/perPPL
    C_30[i] /= pop_30/perPPL
    C_32[i] /= pop_32/perPPL
    C_37[i] /= pop_37/perPPL
    C_46[i] /= pop_46/perPPL
    C_47[i] /= pop_47/perPPL
    C_48[i] /= pop_48/perPPL
    C_53[i] /= pop_53/perPPL
    C_58[i] /= pop_58/perPPL
    C_tn[i] /= pop_tn/perPPL
    C_us[i] /= pop_us/perPPL

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
  C_tn = C_tn[0:-1]
#NEW
  C_04 = C_04[0:-1]
  C_09 = C_09[0:-1]
  C_22 = C_22[0:-1]
  C_24 = C_24[0:-1]
  C_30 = C_30[0:-1]
  C_32 = C_32[0:-1]
  C_37 = C_37[0:-1]
  C_46 = C_46[0:-1]
  C_47 = C_47[0:-1]
  C_48 = C_48[0:-1]
  C_53 = C_53[0:-1]
  C_58 = C_58[0:-1]

#print('Country: {}, values: {}'.format(S_us, C_us))
#print('Country: {}, values: {}'.format(S_it, C_it))
print('Country: {}, values: {}'.format(S_tn, C_tn))

## CURVE FIT ##
def curve_fit(dlist, C_us):
  x = np.array(dlist[-9:-1])
  y = np.array(C_us[-9:-1])
  fit = np.polyfit(x, np.log(y), 1, w = np.sqrt(y))
  A = np.exp(fit[1])
  B = fit[0]
  #print(fit)
  #print('A = {}, B = {}'.format(A,B))
  
  xd = []
  yd = []
  for d in range(7):
    xd.append(d)
    yd.append(A*np.exp(B*d))
  return xd,yd

xd,yd = curve_fit(dlist, C_22)
L22 = 'Fit-NY'
#xt,yt = curve_fit(dlist, C_tn)
xt,yt = curve_fit(dlist, C_24)
FITLABEL = 'Fit-NJ'

#print('yd = {}'.format(yd))

#plt.plot(dlist,C_ge,label=S_ge)
plt.plot(dlist,C_us,"--",label=S_us)
#plt.plot(dlist,C_it,label=S_it)
#plt.plot(dlist,C_ch,label=S_ch)
#plt.plot(dlist,C_ko,label=S_ko)
#plt.plot(dlist,C_uk,label=S_uk)
plt.plot(dlist,C_tn,"m--",label=S_tn)

#NEW
plt.plot(dlist,C_04,"b--",label=S_04)
plt.plot(dlist,C_09,"k--",label=S_09)
plt.plot(dlist,C_22,"r--",label=S_22)
plt.plot(dlist,C_24,"g--",label=S_24)
plt.plot(dlist,C_30,"b-",label=S_30)
plt.plot(dlist,C_32,"k-",label=S_32)
#plt.plot(dlist,C_37,"r-",label=S_37)
plt.plot(dlist,C_46,"g-",label=S_46)
plt.plot(dlist,C_47,"b-.",label=S_47)
#plt.plot(dlist,C_48,"k-.",label=S_48)
plt.plot(dlist,C_53,"r-.",label=S_53)
#plt.plot(dlist,C_58,"g-.",label=S_58)
plt.plot(xd,yd,'k.',label=L22)
plt.plot(xt,yt,'b.',label=FITLABEL)
plt.yscale("log")
plt.ylim(10,1e6)
plt.xlim(-35,7.01)
plt.xticks(np.arange(-35,7,7))
plt.xlabel('Days Since {}'.format(today))
plt.ylabel('Confirmed Cases')
plt.title('Covid-19 Cases')
plt.legend()
plt.grid(True)
plt.savefig("test.pdf")
plt.show()
