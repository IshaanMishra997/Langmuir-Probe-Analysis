# -*- coding: utf-8 -*-
"""
Created on Fri May 13 17:03:05 2022
@author: mishrai
Langmuir Probe Analysis
EP490: Introduction to Plasma Physics
Rose-Hulman Institute of Technology
"""
#-----------------------references-----------------------#
'''
https://www.seas.ucla.edu/~ffchen/Publs/Chen210R.pdf
https://davidpace.com/example-of-langmuir-probe-analysis/
https://advlabs.aapt.org/wiki/File%3A4409
'''
#-----------------------initializing-----------------------#
import matplotlib.pyplot as pl

#Te=3.57#eV
#Te_hot=7.69#eV
#Vf=-38.97#V
Isat=-0.000129#A

me=9.109e-31#kg
e=1.602e-19#C
k=1.38e-23#J/K
M=6.62e-26#kg: Mass of Argon atom
A=0.738e-4#m^2: Area of probe


'''
Notes:
    L2[i][0] is probe bias (V)
    L2[i][1] is probe current (A)
'''
#-----------------------functions-----------------------#
def initial_dataset_reading():
    with open("sampleIV.txt","r") as f:
        a=f.read()
        L=[]
        L2=[[-66.40,-0.0001290]]
        for i in a: 
            L=a.split(",")
            
        for i in range(1,len(L)-1):
            l=L[i][2:len(L[i])-3]
            l=l.split('\t')
            for j in range(len(l)): 
                l[j]=float(l[j])
            if l not in L2:
                L2.append(l)
    L2=lol_sort(L2)
    with open("sampleIV_optimized.txt",'w') as f: 
        for i in range(len(L2)): 
            tl=''
            tl+=str(L2[i][0])+'\t'+str((L2[i][1]+Isat))+'\n'
            f.write(tl)
    
    print("Number of data points collected by Langmuir probe: ", len(L)-1)
    return(L2)

def optimized_dataset_reading():
    with open("sampleIV_optimized.txt","r") as f:
        a=f.read()
        L=a.split("\n")
        del L[len(L)-1]
        for i in range(len(L)): 
            L[i]=L[i].split('\t')
            L[i][0]=float(L[i][0])
            L[i][1]=float(L[i][1])
    print("Number of unique data points: ",len(L))
    return L

def lol_sort(L):
    for i in range(len(L)):
        for j in range(len(L)-1-i):
            if L[j][0]>L[j+1][0]:
                L[j],L[j+1]=L[j+1],L[j]

    return(L)

def average(L,N):
    pass

def plotIV_lin(L):
    X=[]
    Y=[]
    for i in L: 
        X.append(i[0])
        Y.append(i[1])
    pl.plot(X,Y)
    #pl.yscale('log')
    pl.xlabel('Probe bias (V)')
    pl.ylabel('Probe current (A)')
    pl.show()
    #pl.savefig('IV_linear')

def plotIV_log(L):
    X=[]
    Y=[]
    for i in L: 
        X.append(i[0])
        Y.append(i[1])
    pl.plot(X,Y)


    pl.yscale('log')
    pl.xlabel('Probe bias (V)')
    pl.ylabel('Electron current (A)')
    pl.savefig('IV_log')
    pl.show()
    
def derivative(L): 
    L2=[L[0],]
    for i in range(1,len(L)):
        for j in range(len(L2)):
            if L[i][0]==L2[j][0]:
                break
        else: 
            L2.append(L[i])
    print(len(L2))
    
    L=L2
    dL=[]
    #E0=abs(phi_p-L[0])
    dL.append([L[0][0],(L[1][1]-L[0][1])/(L[1][0]-L[0][0])])
    
    for i in range(1,len(L)-1):
        dL.append([L[i][0],(L[i+1][1]-L[i-1][1])/(L[i+1][0]-L[i-1][0])])
        
    dL.append([L[len(L)-1][0],(L[len(L)-1][1]-L[len(L)-2][1])/(L[len(L)-1][0]-L[len(L)-2][0])])
    
    
    #Uncomment this if you want to show and ave dI/dV plot
    X=[]
    Y=[]
    for i in dL: 
        X.append(i[0])
        Y.append(i[1])
    pl.plot(X,Y)


    #pl.yscale('log')
    pl.xlabel('Probe bias (V)')
    pl.ylabel('d2Ie/dV2')
    pl.savefig('d2IdV2')
    pl.show()
    print(dL) 
    return(dL)

def EEDF(L):
    for i in range(len(L)):
        L[i][0]=abs(phi_p-L[i][0])
        L[i][1]=abs(2/(2*A*e)*(2*me*L[i][0]/e)**(1/2)*L[i][1])
        
    print(L)
    L=lol_sort(L)
    edf=[]
    for i in range(0,int(50/1)):
       edf.append([i*1,0])
    for i in L:
        sl=int(i[0]//1)
        edf[sl][1]+=i[1]
    
        
    
    
    
    X=[]
    Y=[]
    for i in edf: 
        X.append(i[0])
        Y.append(i[1])
    pl.plot(X,Y)


    #pl.yscale('log')
    pl.xlabel('Electron energy (eV)')
    pl.ylabel('EEDF (eV^-1)')
    pl.savefig('EEDF')
    pl.show()
    
#-----------------------main code-----------------------#

#L=initial_dataset_reading() #<< execute this if running code for the first time
L=optimized_dataset_reading()

plotIV_log(L)

phi_p=-17.19#V
print('The plasma potential is', phi_p, 'V')
#phi_f=(-38.4-36.4-36-33.6-32.8-32.4)/6#V
phi_f=-34.93#V
print('The floating potential is',phi_f,'V')

#Te=(-17.31+23.85)/(-2.5+3.7)#eV
Te=5.45
print("The electron temperature is",Te,"eV")

Isat=-0.000129#A
EEDF(derivative(derivative(L)))

#--------------------------------------------------------#



