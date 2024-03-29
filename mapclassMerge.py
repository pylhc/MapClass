'''
.. module:: mapclassMerge

MAPCLASS is conceived to optimize
the non-linear aberrations  of the
Final Focus System of CLIC.

Written February 2006

.. moduleauthor:: Rogelio Tomas <Rogelio.Tomas@cern.ch>

'''
#!/usr/bin/env python

from math import *
from string import split
import sys

#dependency for 'zeros(...)'
from numpy import zeros

################
def gammln(xx):
###############
   g=[0.57236494292474305, 0.0, -0.12078223763524987, -4.4408920985006262e-16, 0.28468287047291829, 0.69314718055994429, 1.2009736023470738, 1.7917594692280547, 2.4537365708424441, 3.1780538303479453, 3.9578139676187165, 4.787491742782044, 5.6625620598571462, 6.5792512120101181, 7.5343642367587762, 8.5251613610654982, 9.5492672573011443, 10.604602902745485, 11.689333420797617, 12.801827480081961, 13.940625219404433, 15.104412573076393, 16.292000476568372, 17.502307845875293, 18.734347511938164, 19.987214495663956, 21.260076156247152, 22.552163853126299, 23.862765841692411, 25.191221182742492, 26.536914491119941, 27.899271383845765, 29.277754515046258, 30.671860106086712, 32.081114895954009, 33.505073450144195, 34.943315776884795, 36.395445208041721, 37.861086508970466, 39.339884187209584]
   return g[int(xx/0.5-1)]



#################
def gammlnGOOD( xx):
#################
    
    cof=[76.18009172947146,-86.50532032941677,24.01409824083091,-1.231739572450155,0.1208650973866179e-2,-0.5395239384953e-5]
    y=x=xx
    tmp=x+5.5
    tmp -= (x+0.5)*log(tmp)
    ser=1.000000000190015;
    for c in cof:
        y=y+1
        ser += c/y        
    return -tmp+log(2.5066282746310005*ser/x)



#########################
class Map:
#########################
    '''
    MAP coefficients from madx-PTC output

    :param int order: Calculate map up to this order
    :param string filename: Input filename
    :param boolean gaussianDelta: Use gaussianDelta or not
    '''

    def __init__(self, order=6, filename='fort.18', gaussianDelta=False): 
        ietall=0
        self.order=order
        self.gaussianDelta = gaussianDelta
        xyzd=['x', 'px', 'y', 'py', 'd','s' ]
        strord=str(order+1)
        for line in open(filename):
            if ("etall" in line) :
                ietall=ietall+1
                exec "self."+xyzd[ietall-1]+"=[]"
                #TODO
                exec "self."+xyzd[ietall-1]+"r=1.0*zeros(["+strord+","+strord+","+strord+","+strord+","+strord+"])"
            sline=split(line)
            if (len(sline)==8):
                a=[float(sline[1]), int(sline[3]), int(sline[4]), int(sline[5]), int(sline[6]), int(sline[7]) ]
                if ((a[1]+a[2]+a[3]+a[4]+a[5]) <= self.order ):
                    exec "self."+xyzd[ietall-1]+".append("+str(a)+")"
                    #TODO
                    exec "self."+xyzd[ietall-1]+"r"+str(a[1:])+" = "+sline[1]
        print "Initialized map with # of coefficients in x,px,y,py:",len(self.x), len(self.px), len(self.y), len(self.py)



    def comp(self, map2):
        if (len(self.x) < len(map2.x)):
            print "Self map has fewer elements than map2!!"
            print "This gives a wrong result"
        chi2=0
        for v in self.x:
            if v[5]==0: chi2+=(v[0]-map2.xr[v[1],v[2],v[3],v[4],v[5]])**2
        for v in self.y:
            if v[5]==0: chi2+=(v[0]-map2.yr[v[1],v[2],v[3],v[4],v[5]])**2
        for v in self.py:
            if v[5]==0: chi2+=(v[0]-map2.pyr[v[1],v[2],v[3],v[4],v[5]])**2
        for v in self.px:
            if v[5]==0: chi2+=(v[0]-map2.pxr[v[1],v[2],v[3],v[4],v[5]])**2
        return chi2



    def compc(self, map2):
        if (len(self.x) < len(map2.x)):
            print "Self map has fewer elements than map2!!"
            print "This gives a wrong result"
        chi2=0
        for v in self.x:
            chi2+=(v[0]-map2.xr[v[1],v[2],v[3],v[4],v[5]])**2
        for v in self.y:
            chi2+=(v[0]-map2.yr[v[1],v[2],v[3],v[4],v[5]])**2
        for v in self.py:
            chi2+=(v[0]-map2.pyr[v[1],v[2],v[3],v[4],v[5]])**2
        for v in self.px:
            chi2+=(v[0]-map2.pxr[v[1],v[2],v[3],v[4],v[5]])**2
        return chi2



    def xf(self, vx,vpx,vy,vpy,vd):
        suma=0
        for  coeff in self.x:
            suma += coeff[0]*vx**coeff[1]*vpx**coeff[2]*vy**coeff[3]*vpy**coeff[4]*vd**coeff[5]
        return suma

    def pxf(self, vx,vpx,vy,vpy,vd):
        suma=0
        for  coeff in self.px:
            suma += coeff[0]*vx**coeff[1]*vpx**coeff[2]*vy**coeff[3]*vpy**coeff[4]*vd**coeff[5]
        return suma

    def yf(self, vx,vpx,vy,vpy,vd):
        suma=0
        for  coeff in self.y:
            suma += coeff[0]*vx**coeff[1]*vpx**coeff[2]*vy**coeff[3]*vpy**coeff[4]*vd**coeff[5]
        return suma

    def pyf(self, vx,vpx,vy,vpy,vd):
        suma=0
        for  coeff in self.py:
            suma += coeff[0]*vx**coeff[1]*vpx**coeff[2]*vy**coeff[3]*vpy**coeff[4]*vd**coeff[5]
        return suma

    def f(self, i):
        return [self.xf(i[0],i[1],i[2],i[3],i[4]),  self.pxf(i[0],i[1],i[2],i[3],i[4]), self.yf(i[0],i[1],i[2],i[3],i[4]),  self.pyf(i[0],i[1],i[2],i[3],i[4]) ]



    def offset(self, xory, i):
        '''
        Calculate the beam offset

        :param string xory: Which coordinate to calculate for (x,y,px, or py)
        :param list i: Size of beam in sigma [x,px,y,py]
        '''
        sx=0
        exec 'mapxory=self.'+xory
        for coeff1 in mapxory:
            jj=coeff1[1]
            kk=coeff1[2] 
            ll=coeff1[3] 
            mm=coeff1[4] 
            nn=coeff1[5]
            if ((jj/2==jj/2.) & (kk/2==kk/2.) & (ll/2==ll/2.) & (mm/2==mm/2.) & (nn/2==nn/2.)):
                sigmaprod = self.__sigma(jj,kk,ll,mm,nn,i)
                if (sigmaprod > 0):
                    Gammasumln = self.__gamma(jj,kk,ll,mm,nn)
                    factor = self.__factor(jj,kk,ll,mm,nn)
                    sx += coeff1[0]*factor*exp(Gammasumln)*sigmaprod  
        return sx


    def sigma(self, xory, i):
        '''
        Calculate the beam size in sigma.

        :param string xory: Which coordinate to calculate for (x,y,px, or py)
        :param list i: Size of beam in sigma [x,px,y,py]
        '''
        sx2=0
        exec 'mapxory=self.'+xory
        for coeff1 in mapxory:
            for coeff2 in mapxory:
                if (coeff1[1:] >= coeff2[1:]):
                    countfactor=2.0
                    if (coeff1[1:] == coeff2[1:]):
                        countfactor=1.0
                    jj=coeff1[1] + coeff2[1]
                    kk=coeff1[2] + coeff2[2]
                    ll=coeff1[3] + coeff2[3]
                    mm=coeff1[4] + coeff2[4]
                    nn=coeff1[5] + coeff2[5]
                    if ((jj/2==jj/2.) & (kk/2==kk/2.) & (ll/2==ll/2.) & (mm/2==mm/2.) & (nn/2==nn/2.)):
                        sigmaprod = self.__sigma(jj,kk,ll,mm,nn,i)
                        if (sigmaprod >0):
                            Gammasumln = self.__gamma(jj,kk,ll,mm,nn)
                            factor = countfactor*self.__factor(jj,kk,ll,mm,nn)
                            sxt = coeff1[0]*coeff2[0]*factor*exp(Gammasumln)*sigmaprod   
                            #print jj,kk,ll,mm,nn,":",coeff1[1],coeff1[2],coeff1[3],coeff1[4],coeff1[5], ":" ,sxt
                            sx2 += sxt             
        return sx2


    #Correlation from mapclass.py
    def correlation(self, x1, x2, i):
        sx2=0
        exec 'mapxory1=self.'+x1
        exec 'mapxory2=self.'+x2
        for coeff1 in mapxory1:
            for coeff2 in mapxory2:
                jj=coeff1[1] + coeff2[1]
                kk=coeff1[2] + coeff2[2]
                ll=coeff1[3] + coeff2[3]
                mm=coeff1[4] + coeff2[4]
                nn=coeff1[5] + coeff2[5]

                countfactor=1.0
                
                if ((jj/2==jj/2.) & (kk/2==kk/2.) & (ll/2==ll/2.) & (mm/2==mm/2.) & (nn/2==nn/2.)):
                    sigmaprod = self.__sigma(jj,kk,ll,mm,nn,i)
                    if (sigmaprod > 0):
                        Gammasumln = self.__gamma(jj,kk,ll,mm,nn)
                        factor = countfactor*self.__factor(jj,kk,ll,mm,nn)
                        sxt = coeff1[0]*coeff2[0]*factor*exp(Gammasumln)*sigmaprod   
                        #print jj,kk,ll,mm,nn,":",coeff1[1],coeff1[2],coeff1[3],coeff1[4],coeff1[5], ":" ,sxt
                        sx2 += sxt             
        return sx2


    #Correlation from mapclass.GaussianDelta.py
    def correlation3(self, x1, x2, x3, i):
        sx2=0
        exec 'mapxory1=self.'+x1
        exec 'mapxory2=self.'+x2
        exec 'mapxory3=self.'+x3
        for coeff1 in mapxory1:
            for coeff2 in mapxory2:
              for coeff3 in mapxory3:
                jj=coeff1[1] + coeff2[1] + coeff3[1]
                kk=coeff1[2] + coeff2[2] + coeff3[2]
                ll=coeff1[3] + coeff2[3] + coeff3[3]
                mm=coeff1[4] + coeff2[4] + coeff3[4]
                nn=coeff1[5] + coeff2[5] + coeff3[5]
                
                countfactor=1.0
                    
                if ((jj/2==jj/2.) & (kk/2==kk/2.) & (ll/2==ll/2.) & (mm/2==mm/2.) & (nn/2==nn/2.)):
                        sigmaprod = self.__sigma(jj,kk,ll,mm,nn,i)
                        if (sigmaprod > 0):
                            Gammasumln = self.__gamma(jj,kk,ll,mm,nn)
                            factor = countfactor*self.__factor(jj,kk,ll,mm,nn)
                            sxt = coeff1[0]*coeff2[0]*coeff3[0]*factor*exp(Gammasumln)*sigmaprod   
                            #print jj,kk,ll,mm,nn,":",coeff1[1],coeff1[2],coeff1[3],coeff1[4],coeff1[5], ":" ,sxt
                            sx2 += sxt             
        return sx2


    def generatelist(self,xory,i):
        sx2=0
        exec 'mapxory=self.'+xory
        exec "self.list"+xory+"=[]"
        for coeff1 in mapxory:
            for coeff2 in mapxory:
                if (coeff1 >= coeff2):
                    countfactor=2.0
                    if (coeff1 == coeff2):
                        countfactor=1.0
                    jj=coeff1[1] + coeff2[1]
                    kk=coeff1[2] + coeff2[2]
                    ll=coeff1[3] + coeff2[3]
                    mm=coeff1[4] + coeff2[4]
                    nn=coeff1[5] + coeff2[5]
                    if ((jj/2==jj/2.) & (kk/2==kk/2.) & (ll/2==ll/2.) & (mm/2==mm/2.) & (nn/2==nn/2.)):
                        sigmaprod = self.__sigma(jj,kk,ll,mm,nn,i)
                        if (sigmaprod >0):
                            Gammasumln = self.__gamma(jj,kk,ll,mm,nn)
                            factor = countfactor*self.__factor(jj,kk,ll,mm,nn)
                            sxt = coeff1[0]*coeff2[0]*factor*exp(Gammasumln)*sigmaprod
                            elist = [-abs(sxt),sxt,coeff1[1], coeff1[2],coeff1[3],coeff1[4], coeff1[5], coeff2[1], coeff2[2],coeff2[3],coeff2[4], coeff2[5]]
                            exec "self.list"+xory+".append(elist)"
        exec "self.list"+xory+".sort()"

    #Auxiliary functions (private)
    def __sigma(self, jj, kk, ll, mm, nn, i):
        if (self.gaussianDelta):
            sigmaprod = pow(i[0], jj)*pow(i[1], kk)*pow(i[2], ll)*pow(i[3], mm)*pow(i[4], nn)
        else:
            sigmaprod = pow(i[0], jj)*pow(i[1], kk)*pow(i[2], ll)*pow(i[3], mm)*pow(i[4]/2., nn)
        return sigmaprod


    def __gamma(self, jj, kk, ll, mm, nn):
        if (self.gaussianDelta):
            Gammasumln = gammln(0.5+jj/2.)+gammln(0.5+kk/2.)+gammln(0.5+ll/2.)+gammln(0.5+mm/2.)+gammln(0.5+nn/2.)
        else:
            Gammasumln = gammln(0.5+jj/2.)+gammln(0.5+kk/2.)+gammln(0.5+ll/2.)+gammln(0.5+mm/2.)
        return Gammasumln

    def __factor(self, jj, kk, ll, mm, nn):
        if (self.gaussianDelta):
               factor = pow(2, (jj+kk+ll+mm+nn)/2.)/pow(pi, 2.5)
        else:
               factor = pow(2, (jj+kk+ll+mm)/2.)/pow(pi, 2.)/(nn+1)
        return factor

############################################
#### some examples of usage #####################
############################################
#sigmaFFSstart=[3.9e-6,5.75e-8, 3.76e-7, 1.773e-8,0.01]
#map=Map(4)
#map.generatelist('x',sigmaFFSstart)
#map.generatelist('y',sigmaFFSstart)
#print map.listx[0:9]
#print
#print map.listy[0:20]

#i=[3.9e-6,5.75e-8,3.76e-7,1.773e-8,0]
#print map.offset('x',i), sqrt(map.sigma('x',i)-map.offset('x',i)**2)

#map=Map(1)
#print sqrt(map.sigma('x',sigmaFFSstart)), sqrt(map.sigma('y',sigmaFFSstart))
#map=Map(2)
#print sqrt(map.sigma('x',sigmaFFSstart)), sqrt(map.sigma('y',sigmaFFSstart))
#map=Map(3)
#print sqrt(map.sigma('x',sigmaFFSstart)), sqrt(map.sigma('y',sigmaFFSstart))
#map=Map(4)
#print sqrt(map.sigma('x',sigmaFFSstart)), sqrt(map.sigma('y',sigmaFFSstart))
#map=Map(5)
#print sqrt(map.sigma('x',sigmaFFSstart)), sqrt(map.sigma('y',sigmaFFSstart))
#map=Map(6)
#print sqrt(map.sigma('x',sigmaFFSstart)), sqrt(map.sigma('y',sigmaFFSstart))
#map=Map(7)
#print sqrt(map.sigma('x',sigmaFFSstart)), sqrt(map.sigma('y',sigmaFFSstart))
#map=Map(8)
#print sqrt(map.sigma('x',sigmaFFSstart)), sqrt(map.sigma('y',sigmaFFSstart))