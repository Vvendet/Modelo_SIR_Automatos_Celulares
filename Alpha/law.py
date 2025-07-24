import powerlaw
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

file_path = 'datatonumpy.dat'
df = pd.read_csv(file_path,header=(0))
df = df.dropna(axis='rows')

data = df['Alpha']
data = np.array(data)
index = np.where(data <=0)
data = np.delete(data,index)
n = len(data)

results = powerlaw.Fit(data)
xmin = results.power_law.xmin
alpha_hat = results.power_law.alpha
print('Alpha estimado:',alpha_hat)
print('xmin estimado:',xmin)


fig = plt.figure(figsize=(8,6))
nb = 500
p,bins=np.histogram(data,bins=nb,density=True)
bins_mean=[0.5*(bins[i]+bins[i+1]) for i in range(len(p))]
plt.loglog(bins_mean,p,'o',color='gray',alpha=0.6,linewidth=1)

y=np.linspace(xmin,np.max(data),100)
print(y)
f_hat=(alpha_hat-1)*xmin**(alpha_hat-1)*y**(-alpha_hat)
plt.plot (y,f_hat,'--',color='gray',label='Modelo Estimado')
plt.xlabel('Alpha',fontsize=20)
plt.ylabel('f(x)',fontsize=20)
plt.show()
