import sys
import math
import numpy
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib import cm

def cap(a,c):
	if(a>0 and c<1 and a!=c):
		return math.log((((((1-a)**((1-a)*c))*(a**(a*c)))/(((1-c)**((1-c)*a))*(c**(a*c))))**(1/(c-a))) + (((((1-c)**((1-a)*(1-c)))*(c**((1-a)*c)))/(((1-a)**((1-c)*(1-a)))*(a**(a*(1-c)))))**(1/(c-a))) , 2)
	elif((a<=1 and a>=0) and a==c):
		return 0
	elif((a>0 and a<1) and c==0):
		return math.log(1+a*(1-a)**((1-a)/a),2)
	elif((a==0) and (c>0 and c<1)):
		return math.log(1+c*(1-c)**((1-c)/c),2)
	elif((a>0 and a<1) and c==1):
		return math.log(1+(1-a)*(a)**((a)/(1-a)),2)
	elif(a==1 and (c>0 and c<1)):
		return math.log(1+(1-c)*(c)**((c)/(1-c)),2)
	elif((a==1 and c==0) or (a==0 and c==1)):
		return 1
	
C =[]
x = numpy.linspace(0,1,1000)
y = numpy.linspace(0,1,1000)
X, Y = numpy.meshgrid(x, y)
for i in x.tolist():
	for j in y.tolist():
		C.append(cap(i,j))
C = numpy.asarray(C)	
C = C.reshape(1000,1000)

plot = plt.figure()
ax = plt.axes()
ax.contourf(X,Y,C,100, cmap=cm.jet)
Cplot = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, C, cmap=plt.cm.jet,linewidth=0, antialiased=1)
plt.show()
