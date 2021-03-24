import sys
import math
import numpy
import networkx as nx
import matplotlib.pyplot as plt
import itertools
import timeit
numpy.set_printoptions(threshold=numpy.inf, linewidth=numpy.inf)  #Output full matrix

start = timeit.default_timer()
if(len(sys.argv) >= 2 and sys.argv[1]>=1 and sys.argv[2]>=1):	#get w and l from commandline or user
	w = int(sys.argv[1])
	l = int(sys.argv[2])
else:
	w=int(raw_input("enter W: "))
	l=int(raw_input("enter L: "))

n = (l+1)*w		#Number of nodes
m = ((w-1)*(l-1))/2.0 	#Number of matchsticks
of = False		#Odd flag for creating plus and normal graphs and matrices in case if w and l are both odd.
j=0 	#Counter
k=1		#Normal counter
kp=2	#Plus counter
HM_0 = numpy.zeros((n,n),dtype = int)		#Initialize hammock blocks matrix
HG_0 = nx.Graph()		#Initialize hammock blocks graph
HM_1 = numpy.zeros((n,n),dtype = int)		#Initialize hammock matches matrix
HG_1 = nx.Graph()		#Initialize hammock matches graph



def Poly_Hammock(G0,G1,of):	#calculate polynomials
	poly = []
	G = nx.compose(G0,G1)
	counter = 0
	perm = []
	edges= list(G0.edges())
	for i in range(len(edges)):
		iter = itertools.permutations(list(range(len(edges))),i)
		for j in iter:
			j = list(j)
			j.sort()
			if j not in perm:	
				perm.append(j)
		for j in range(len(perm)):
			for k in range(len(perm[j])):
				G.remove_edge(*edges[(perm[j][k])])
			if nx.has_path(G,0,len(G)-1):
				counter += 1
			G = nx.compose(G0,G1)
		if (counter == 0):
			break
		else:
			poly.append(counter)
			counter = 0
			perm = []
	if(of):
		print "polynomials plus :",poly[::-1]
	else:
		print "polynomials :",poly[::-1]
	return poly


def plot_Rel(poly,w,l,of):	#plot reliablity
	power = w*l
	counter = 0
	R = 0
	P = numpy.arange(0,1,0.001)
	for i in poly:
			R = R + (P**power)*((1-P)**counter)*i
			power -= 1
			counter +=1
	if(of == False):
		plt.figure("Reliability")
		plt.plot(P,R,label = 'H(%d,%d)'%(w,l))
		plt.title('Reliability of %dx%d  Hammock network' % (w,l))
		plt.xlabel('Probability')
		plt.ylabel('Reliability')
		plt.grid(color = 'black', alpha=.1,linestyle='--')
		plt.legend()
		plt.savefig("%dx%d Hammock Network Reliability" % (w,l))
	else:
		plt.figure("Reliability Plus")
		plt.plot(P,R,'--',label = 'H(%d,%d) Plus'%(w,l))
		plt.title('Reliability of %dx%d plus Hammock network' % (w,l))
		plt.xlabel('Probability')
		plt.ylabel('Reliability')
		plt.grid(color = 'black', alpha=.1,linestyle='--')
		plt.legend()
		plt.savefig("%dx%d Plus Hammock Network Reliability" % (w,l))

def output_network(w,l,HG,HM,title,of):
	if(of):
		plt.figure("%dx%d Hammock Network %s Plus" % (w,l,title))
		nx.draw_networkx(HG,node_color='green',node_size=30)
		plt.savefig("%dx%d Hammock Network %s Plus" % (w,l,title))
		nx.write_gexf(HG, "%dx%d Hammock Network %s Plus.gexf" % (w,l,title))
		with open("%dx%d plus %s hammock Adjacency.txt" % (w,l,title), 'w') as f:
			f.write(numpy.array2string(HM, separator=', '))
	else:
		plt.figure("%dx%d %s Normal Hammock Network" % (w,l,title))
		nx.draw_networkx(HG,node_color='green',node_size=30)
		plt.savefig("%dx%d %s Normal Hammock Network" % (w,l,title))
		nx.write_gexf(HG, "%dx%d %s Normal Hammock Network.gexf" % (w,l,title))
		with open("%dx%d %s Normal hammock Adjacency.txt" % (w,l,title), 'w') as f:
			f.write(numpy.array2string(HM, separator=', '))

		
##Main routine
#create seprate matrix and graphs for bloacks and matches
if(m-int(m) > 0):
	of = True 		#Both w and l are odd.
	if(l==2):
		kp	= 4	#Counter
	HMP_0 = numpy.zeros((n,n),dtype = int)	#Initialize hammock blocks matrix plus
	HGP_0 = nx.Graph()#		Initialize hammock blcoks graph plus
	HMP_1 = numpy.zeros((n,n),dtype = int)	#Initialize hammock matches matrix plus
	HGP_1 = nx.Graph()#		Initialize hammock matches graph plus
	for i in range(n):
		HGP_0.add_node(i)	#Add nodes to the blocks graph plus
		HGP_1.add_node(i)	#Add nodes to the matches graph	plus
for i in range(n):
	HG_0.add_node(i)	#Add nodes to the blocks graph
	HG_1.add_node(i)	#Add nodes to the matches graph
for i in range(n):
	if(l==2):	# L == 2 is an exception, add metches to the graph and matrix
		if((i == k) and (i+3 < n)):
			HG_1.add_edge(i,i+3)
			HM_1[i][i+3] = HM_1[i+3][i] = 1
			k+=6
		if(of and (i == kp) and (i+3 < n)):	#second(plus) hammock 
			HGP_1.add_edge(i,i+3)
			HMP_1[i][i+3] = HM_1[i+3][i] = 1
			kp+=6
	else:	#add metches to the graph and matrix
		if((i == k) and (i+l+1<n)):
			HG_1.add_edge(i,i+l+1)
			HM_1[i][i+l+1] = HM_1[i+l+1][i] = 1
			if(k+2==l+j*(l+1)):
				if(l%2 == 0):
					k+=4
				else:
					k+=5
			elif(k+2>l+j*(l+1)):
				if(l%2 == 0):
					k+=4
				else:
					k+=3
			else:
				k+=2
		if(of and (i == kp) and (i+l+1<n)):	#second(plus) hammock matches
			HGP_1.add_edge(i,i+l+1)
			HMP_1[i][i+l+1] = HMP_1[i+l+1][i] = 1
			if(kp+2==l+j*(l+1)):
				if(l%2 == 0):
					kp+=4
				else:
					kp+=5
			elif(kp+2>l+j*(l+1)):
				if(l%2 == 0):
					kp+=4
				else:
					kp+=3
			else:
				kp+=2
	if(i == (l+j*(l+1))):	#right and left column of matches
		j+=1
		if((l+j*(l+1)) < n):
			HG_1.add_edge(i,l+j*(l+1))
			HG_1.add_edge(i-l,j*(l+1))
			HM_1[i][l+j*(l+1)] = HM_0[l+j*(l+1)][i] = 1
			HM_1[i-l][j*(l+1)] = HM_0[j*(l+1)][i-l] = 1
		if(of and ((l+j*(l+1)) < n)):
			HGP_1.add_edge(i,l+j*(l+1))
			HGP_1.add_edge(i-l,j*(l+1))
			HMP_1[i][l+j*(l+1)] = HMP_0[l+j*(l+1)][i] = 1
			HMP_1[i-l][j*(l+1)] = HMP_0[j*(l+1)][i-l] = 1
		continue
	HM_0[i][i+1] = HM_0[i+1][i] = 1 #add vertical matches acording to last column border
	HG_0.add_edge(i,i+1)
	if(of):
		HMP_0[i][i+1] = HMP_0[i+1][i] = 1
		HGP_0.add_edge(i,i+1)
		
print "Number of nodes: %d" % (n)
output_network(w,l,HG_0,HM_0,"Blocks",0)
output_network(w,l,HG_1,HM_1,"Matches",0)
output_network(w,l,nx.compose(HG_0,HG_1),HM_1+HM_0,"Composed",0)
plot_Rel(Poly_Hammock(HG_0,HG_1,0),w,l,0)
if(of):
	output_network(w,l,HGP_0,HMP_0,"Blocks",of)
	output_network(w,l,HGP_1,HMP_1,"Matches",of)
	output_network(w,l,nx.compose(HGP_0,HGP_1),HMP_1+HMP_0,"Composed",of)
	plot_Rel(Poly_Hammock(HGP_0,HGP_1,of),w,l,of)
stop = timeit.default_timer()
print 'Total computation time (seconds): ', int(stop - start)
exit()