from pandas import read_csv, DataFrame 
import numpy as np
import math
import matplotlib
import os
matplotlib.use("pdf")
import matplotlib.pyplot as plt


df = read_csv('covid_19/data/skimmed_onfirmed_global.csv')
print (df)


plt.figure(figsize=(18, 10))

print ("---------------------- INDIA -----------------------")
''' India '''
day_india_ = 42
drop_india_ = [i for i in range (day_india_-1)] ## -1 is needed because dataframe index starts from 0 and to make data alligned it is needed
df_skimmed_ = df.drop(drop_india_)
y_india_ = df_skimmed_["India"]
x_india_ = [i for i in range(day_india_,len(df)+1)]
print (x_india_)
print (y_india_)
print (len(x_india_), len(y_india_))
plt.scatter(x_india_, y_india_)

''' France before lockdown''' 
print ("---------------------- FRANCE before lockdown -----------------------")
day_france_ = 40
day_frace_max_ = 51
## this will drop first N entries from the dataframe
drop_france_ = [i for i in range (day_france_-1)]
drop_france_lokd_ = [i for i in range (day_frace_max_,len(df))]
df_skimmed_ = df.drop(drop_france_)
df_skimmed_ = df_skimmed_.drop(drop_france_lokd_)

y_france_ = df_skimmed_["France"]
x_france_ = [i for i in range(day_france_,day_frace_max_+1)]
print (x_france_)
print (y_france_)
print (len(x_france_), len(y_france_))
plt.scatter(x_france_, y_france_)


print ("---------------------- FRANCE after lockdown -----------------------")
''' France after lockdown: post lock down (pld)''' 
day_france_pld_ = 52
## this will drop first N entries from the dataframe
drop_france_pld_ = [i for i in range (day_france_pld_-1)]
df_skimmed_ = df.drop(drop_france_pld_)
y_france_pld_ = df_skimmed_["France"]
x_france_pld_ = [i for i in range(day_france_pld_,len(df)+1)]

print (x_france_pld_)
print (y_france_pld_)
print (len(x_france_pld_), len(y_france_pld_))
plt.scatter(x_france_pld_, y_france_pld_)




#plt.semilogy()
plt.ylabel("confirmed with COVID-19")
plt.xlabel("day (w.r.t first case in China)")
plt.title("COVID-19 analysis")


plt.ylim(0.01,30000.0)
plt.xlim(30,80.0)
plt.grid(b=True, which='major', axis='both')
plt.savefig("covid_19_confirmed.png")

from scipy import optimize


## define a function 

def expo(x, a, b):
    return a * np.exp(x/b)
    

params_india, params_covariance = optimize.curve_fit(expo,x_india_, y_india_, p0=[1,3] )
params_france, params_covariance = optimize.curve_fit(expo,x_france_, y_france_, p0=[1,3] )
#print ("paramaters = ",params)
xnew_ = range(70)
#print (expo(xnew_, params[0], params[1]))

plt.plot(xnew_, expo(xnew_, params_india[0], params_india[1]), label='Fitted function')
plt.plot(xnew_, expo(xnew_, params_france[0], params_france[1]), label='Fitted function')

plt.savefig("covid_19_confirmed_fitted.png")
plt.legend()

os.system("cp covid_19_confirmed.png /afs/cern.ch/work/k/khurana/public/Research")
os.system("cp covid_19_confirmed_fitted.png /afs/cern.ch/work/k/khurana/public/Research")
