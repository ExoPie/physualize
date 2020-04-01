from pandas import read_csv, DataFrame 
import numpy as np
import math
import matplotlib
import os
matplotlib.use("pdf")
import matplotlib.pyplot as plt


## define a function 

def expo(x, a, b):
    return  np.exp( a + x/b) 


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
plt.scatter(x_india_, y_india_, c="Black", marker="o", s=50, label="India")


from scipy import optimize



params_india, params_covariance = optimize.curve_fit(expo,x_india_, y_india_, p0=[2.0,2] )
xnew_=range(40,80)
plt.plot(xnew_, expo(xnew_, params_india[0], params_india[1]), label='', color="Black")

plt.legend(numpoints=1,fontsize=22, loc=2)
#plt.semilogy()
plt.ylabel("confirmed with COVID-19",fontsize=22)
plt.xlabel("day (w.r.t first case in China)",fontsize=22)
plt.title("COVID-19 analysis", fontsize=22)
plt.tick_params(axis='both', which='major', labelsize=22)
plt.locator_params(axis='y', nbins=15)
plt.locator_params(axis='x', nbins=20)

plt.ylim(0.01,5000.0)
plt.xlim(30,80.0)
plt.grid(b=True, which='major', axis='both')


plt.savefig("covid_19_confirmed.png")


xnew_=range(80)



''' France before lockdown''' 
print ("---------------------- FRANCE before lockdown -----------------------")
day_france_ = 40
day_frace_max_ = 53
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
plt.scatter(x_france_, y_france_,c="Red", marker="v", s=60, label="France before lock down")


print ("---------------------- FRANCE after lockdown -----------------------")
''' France after lockdown: post lock down (pld)''' 
day_france_pld_ = 54
## this will drop first N entries from the dataframe
drop_france_pld_ = [i for i in range (day_france_pld_-1)]
df_skimmed_ = df.drop(drop_france_pld_)
y_france_pld_ = df_skimmed_["France"]
x_france_pld_ = [i for i in range(day_france_pld_,len(df)+1)]

print (x_france_pld_)
print (y_france_pld_)
print (len(x_france_pld_), len(y_france_pld_))
plt.scatter(x_france_pld_, y_france_pld_, c="Blue", marker="^", s=70, label="France after lock down")



''' Style and cosmetics '''
plt.legend(numpoints=1,fontsize=22, loc=2)
#plt.semilogy()
plt.ylabel("confirmed with COVID-19",fontsize=22)
plt.xlabel("day (w.r.t first case in China)",fontsize=22)
plt.title("COVID-19 analysis", fontsize=22)
plt.tick_params(axis='both', which='major', labelsize=22)
plt.locator_params(axis='y', nbins=25)
plt.locator_params(axis='x', nbins=20)

plt.ylim(0.01,30000.0)
plt.xlim(30,80.0)
plt.grid(b=True, which='major', axis='both')





params_france, params_covariance = optimize.curve_fit(expo,x_france_, y_france_, p0=[1,3] )
params_france_pld, params_covariance = optimize.curve_fit(expo,x_france_pld_, y_france_pld_, p0=[1,3] )
print ("paramaters india = ",params_india)
print ("paramaters before lockdopwn= ",params_france)
print ("paramaters after lockdopwn= ",params_france_pld)

xnew_ = range(80)
print (xnew_, expo(xnew_, params_india[0], params_india[1]))



plt.plot(xnew_, expo(xnew_, params_france[0], params_france[1]), label='',  color="Red")
plt.plot(range(54,80), expo(range(54,80), params_france_pld[0], params_france_pld[1]), label='',  color="Blue")

plt.savefig("covid_19_confirmed_fitted.png")
plt.legend()

os.system("cp covid_19_confirmed.png /afs/cern.ch/work/k/khurana/public/Research")
os.system("cp covid_19_confirmed_fitted.png /afs/cern.ch/work/k/khurana/public/Research")
