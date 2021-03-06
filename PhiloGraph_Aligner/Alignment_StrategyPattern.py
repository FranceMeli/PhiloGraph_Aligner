from .latin_use_cltk import Lemmatize
import numpy as np
from .utils import Split, ParallelStringResult, CheckLen
from .Textual_object import Textual_Object
from abc import ABC, abstractmethod

class Strategy(ABC):
    """
    Declare an interface common to all supported algorithms. Alignment
    uses this interface to call the algorithm defined by a
    ConcreteStrategy.def execute(self) -> str:
        return "ConcreteStrategy B"
    """
    @abstractmethod
    def align(self,v1,v2):
        pass

class Character(Strategy):
    
    def align(self,v1,v2):
        lezione = v1
        variante = v2
        '''  W_Al=Lev.editops(lezione, variante) '''
        ''' W_Al= self.ch_edit_distance(lezione, variante,costs) '''
        W_Al= self.get_ops(lezione, variante, is_damerau=False)
        for i in range(0,len(W_Al)):
            operation=W_Al[i][0]
            posS=W_Al[i][1]
            posT=W_Al[i][2]
            if( not(posS<0) or not(posT<0) ):
                if operation=="insert":
                    lezione= lezione[:posS] + "-" + lezione[posS:]      
                elif operation=="delete":
                    variante= variante[:posT] + "-" + variante[posT:]
        
        S1=Split(lezione)     
        S2=Split(variante) 
        Al=ParallelStringResult(S1,S2)
        Op=W_Al
        return Al,Op
    
    def get_ops(self,string1, string2, is_damerau=False):
        dist_matrix = self._levenshtein_distance_matrix(string1, string2, is_damerau)
        i, j = self._levenshtein_distance_matrix(string1, string2, is_damerau).shape
        i -= 1
        j -= 1
        ops = list()
        while i != -1 and j != -1:
            ''' if is_damerau:
                if i > 1 and j > 1 and string1[i-1] == string2[j-2] and string1[i-2] == string2[j-1]:
                    if dist_matrix[i-2, j-2] < dist_matrix[i, j]:
                        ops.insert(0, ('transpose', i - 1, i - 2))
                        i -= 2
                        j -= 2
                        continue '''
            ''' argmin Returns the indices of the minimum values along an axis. '''
            index = np.argmin([dist_matrix[i-1, j-1], dist_matrix[i, j-1], dist_matrix[i-1, j]])
            if index == 0:
                if dist_matrix[i, j] > dist_matrix[i-1, j-1]:
                    ops.insert(0, ('replace', i - 1, j - 1))
                i -= 1
                j -= 1
            elif index == 1:
                ops.insert(0, ('insert', i - 1, j - 1))
                j -= 1
            elif index == 2:
                ops.insert(0, ('delete', i - 1, i - 1))
                i -= 1
        return ops

    def _levenshtein_distance_matrix(self,string1, string2, is_damerau=False):
        n1 = len(string1)
        n2 = len(string2)
        d = np.zeros((n1 + 1, n2 + 1), dtype=int)
        for i in range(n1 + 1):
            d[i, 0] = i
        for j in range(n2 + 1):
            d[0, j] = j
        for i in range(n1):
            for j in range(n2):
                if string1[i] == string2[j]:
                    cost = 0
                else:
                    cost = 1
                d[i+1, j+1] = min(d[i, j+1] + 1, # insert
                                d[i+1, j] + 1, # delete
                                d[i, j] + cost) # replace
                if is_damerau:
                    if i > 0 and j > 0 and string1[i] == string2[j-1] and string1[i-1] == string2[j]:
                        d[i+1, j+1] = min(d[i+1, j+1], d[i-1, j-1] + cost) # transpose
        return d

class Metric(Strategy):

    def align(self,Var):
        L1=len(Var[0])
        L2=len(Var[1])
        if(L1>L2):
            V1=Var[0]
            V2=Var[1]
        else: 
            V1=Var[1]
            V2=Var[0]
        n=0
        m=0
        Verso1=[]
        Verso2=[]

        while(n<len(V1) and m<len(V2)):
            Sillaba_V1=V1[n]
            check=False
            for x in V2:
                if Sillaba_V1==x:
                    check=True
                    Verso1.append(Sillaba_V1)
            if not check:
                Verso1.append(Sillaba_V1)
                Verso2.append("-")
            Sillaba_V2=V2[m]
            check=False
            for y in V1:
                if Sillaba_V2==y:
                    check=True
                    Verso2.append(Sillaba_V2)
            if not check:
                Verso2.append(Sillaba_V2)
                Verso1.append("-")
            n=n+1
            m=m+1
        while(n<len(V1)):
            Verso1.append(V1[n])
            n=n+1
        while(m<len(V2)):
            Verso2.append(V2[m])
            m=m+1
        Verso1,Verso2 = CheckLen(Verso1,Verso2)
        return Verso1, Verso2

class Word(Strategy):

    def align(self,V1,V2):

            size_x = len(V1) + 1
            size_y = len(V2) + 1
            matrix = np.zeros ((size_x, size_y))
            for x in range(size_x):
                matrix [x, 0] = x
            for y in range(size_y):
                matrix [0, y] = y
            n=0
            for x in range(1, size_x):
                for y in range(1, size_y):
                    if V1[x-1] == V2[y-1]:
                        n=n+1
                        matrix [x,y] = n
                    else:
                        matrix [x,y] = 0
            Var1=[]
            Var2=[]
            Pos=1

            for y in range(1,size_y):
                v=0
                for x in range(1,size_x):
                    if matrix [x,y] != Pos:
                        v=v+1 
                    if matrix [x,y] > Pos:
                        Pos= int(matrix[x,y])+1
                if v==size_x-1 and size_x!=size_y:
                    Var1.append("-")
                    Var2.append(V2[y-1])
                elif v==size_x-1 and size_x==size_y:
                    Var1.append(V1[y-1])
                    Var2.append(V2[y-1])
                else:
                    Var1.append(V2[y-1])
                    Var2.append(V2[y-1])
                    Pos=Pos+1
            Res=ParallelStringResult(Var1,Var2)
            '''  else: 
            V1=Token(var)
            Res=ParallelStringResult(V1,V1) '''
            return Res



alignment=[]
operation=[]
scansione=[]

class Aligner:

    strategy: Strategy

    def __init__(self,v1="",v2="", strategy: Strategy = None ):
        self.strategy = strategy
        self.v1=v1
        self.v2=v2

    def setWordVariant(self,w1,w2):
        self.v1 = w1
        self.v2 = w2
        
    def setTextVariant(self,s1,s2):
        self.v1 = Textual_Object(s1)
        self.v2 = Textual_Object(s2)

    def setGranularity(self,g):
        self.g = g
    
    def setStrategy(self,strategy):
        self.strategy = strategy

    def alignment(self,g,v1,v2):

        self.setGranularity(g)
        if g=="carattere":
            self.setWordVariant(v1,v2)
            self.setStrategy(Character())
            self.alignment, self.operation = self.strategy.align(self.v1,self.v2)

            ''' Ritorno allineamento e operazioni '''
            return self.alignment,self.operation
            
        elif g=="metrica" or g=="pedecerto":
            self.setTextVariant(v1,v2)
            self.setStrategy(Metric())
            Sillabe = []
            Scansione = []
            syll1,scan1=self.v1.Metric_Scan()
            syll2,scan2=self.v2.Metric_Scan()
            Sillabe.append(syll1)
            Sillabe.append(syll2)
            Scansione.append(scan1)
            Scansione.append(scan2)
            V1=[]
            V2=[]
            if( len(Sillabe[0]) != len(Sillabe[1]) ):
                V1,V2=self.strategy.align(Sillabe)
                Res=ParallelStringResult(V1,V2)
            else: 
                Res=ParallelStringResult(Sillabe[0],Sillabe[1])
            self.alignment=Res
            self.scansione=Scansione
    
            ''' Ritorno allineamento e scansione metrica '''
            return self.alignment, self.scansione

        else :
            self.setTextVariant(v1,v2)
            self.setStrategy(Word())

            if (g=="paroleLemmatizzate"): 
    
                Tok1=self.v1.Token()
                Tok2=self.v2.Token()
                self.v1=Lemmatize(Tok1)
                self.v2=Lemmatize(Tok2)
                self.alignment = self.strategy.align(self.v1,self.v2)

            else:

                self.v1=self.v1.Token()
                self.v2=self.v2.Token()

                self.alignment = self.strategy.align(self.v1,self.v2)

            return self.alignment

   
    def ch_edit_distance(self,lezione, variante, costs):
        deletion, insertion, replace = costs
        size_x = len(variante) + 1
        size_y = len(lezione) + 1
        matrix = np.zeros ((size_x, size_y))
        for x in range(size_x):
            matrix [x, 0] = x
        for y in range(size_y):
            matrix [0, y] = y
        sol=[]
        for x in range(1, size_x):
            minus=max(size_x,size_y)
            for y in range(1, size_y):
                if variante[x-1] == lezione[y-1]:
                    matrix [x,y] = min(
                        matrix[x-1, y] + deletion,  
                        matrix[x-1, y-1],
                        matrix[x, y-1] + insertion
                    )
                else:
                    matrix [x,y] = min(
                        matrix[x-1,y] + deletion,
                        matrix[x-1,y-1] + replace,
                        matrix[x,y-1] + insertion
                    )
                if matrix[x,y]< minus:
                    minus=matrix[x,y]
            sol.append(minus)        
        ''' print (matrix)  ''' 
        '''  print ("Il minimum edit distance ?? " + str(matrix[size_x - 1, size_y - 1])) '''
        x=0
        y=0
        op=matrix[x,y]
        Results=[]
        while(x<size_x-1 and y<size_y-1):
            active = min(
                        matrix[x+1,y],
                        matrix[x+1,y+1],
                        matrix[x,y+1]
                    )
            if (op!=active):
                if ( (active!= matrix[x+1,y] and active!=matrix[x+1,y+1] and active==matrix[x,y+1]) or (active == matrix[x+1,y] and active!=matrix[x+1,y+1] and active==matrix[x,y+1]) ):
                    Results.append( ('insert',x,y) )
                    y=y+1
                elif (active == matrix[x+1,y] and active!=matrix[x+1,y+1] and active!=matrix[x,y+1] ):
                    Results.append( ('delete',x,y) )
                    x=x+1
                elif ( (active == matrix[x+1,y] and active==matrix[x+1,y+1] and active!=matrix[x,y+1]) or 
                        (active != matrix[x+1,y] and active==matrix[x+1,y+1] and active==matrix[x,y+1]) or
                       (active != matrix[x+1,y] and active==matrix[x+1,y+1] and active!=matrix[x,y+1]) ):
                    Results.append( ('replace',x,y))
                    y=y+1
                    x=x+1      
                else :  
                    '''  if (size_x == size_y):
                        Results.append( ('replace',x,y))
                        y=y+1
                        x=x+1
                    elif (size_x > size_y):
                        Results.append( ('insert',x,y))
                        y=y+1
                    else :
                        Results.append( ('delete',x,y))
                        x=x+1 '''
                    Results.append( ('replace',x,y))
                    y=y+1
                    x=x+1
                op=active
            else :
                if ( (active != matrix[x+1,y] and active!=matrix[x+1,y+1] and active==matrix[x,y+1]) or (active == matrix[x+1,y] and active!=matrix[x+1,y+1] and active==matrix[x,y+1] ) ):
                    y=y+1
                elif (active == matrix[x+1,y] and active!=matrix[x+1,y+1] and active!=matrix[x,y+1] ):   
                    x=x+1
                elif ( (active == matrix[x+1,y] and active==matrix[x+1,y+1] and active!=matrix[x,y+1]) or 
                       (active != matrix[x+1,y] and active==matrix[x+1,y+1] and active==matrix[x,y+1]) or 
                       (active != matrix[x+1,y] and active==matrix[x+1,y+1] and active!=matrix[x,y+1])
                    ): 
                    y=y+1
                    x=x+1
                else : 
                    y=y+1
                    x=x+1
        while (x<size_x-1):
            Results.append( ('delete',x,y))
            x=x+1
        while (y<size_y-1):
            Results.append( ('insert',x,y) )
            y=y+1

        return Results


    ''' Per ogni sillaba cerco se ?? presente nel'intera parola, se non ?? presente allora aggiungo - '''

    
''' def VerseAlignment(self,var):
        if(isinstance(var, list)):
            V1=Token(var[0])
            V2=Token(var[1])
            size_x = len(V1) + 1
            size_y = len(V2) + 1
            matrix = np.zeros ((size_x, size_y))
            for x in range(size_x):
                matrix [x, 0] = x
            for y in range(size_y):
                matrix [0, y] = y
            n=0
            for x in range(1, size_x):
                for y in range(1, size_y):
                    if V1[x-1] == V2[y-1]:
                        n=n+1
                        matrix [x,y] = n
                    else:
                        matrix [x,y] = 0
            Var1=[]
            Var2=[]
            Pos=1
            operazione=[]
            for y in range(1,size_y):
                v=0
                for x in range(1,size_x):
                    if matrix [x,y] != Pos:
                        v=v+1 
                    if matrix [x,y] > Pos:
                        Pos= int(matrix[x,y])+1
                if v==size_x-1 and size_x!=size_y:
                    Var1.append("-")
                    Var2.append(V2[y-1])
                elif v==size_x-1 and size_x==size_y:
                    Var1.append(V1[y-1])
                    Var2.append(V2[y-1])
                else:
                    Var1.append(V2[y-1])
                    Var2.append(V2[y-1])
                    Pos=Pos+1
            Res=ParallelStringResult(Var1,Var2)
        else: 
            V1=Token(var)
            Res=ParallelStringResult(V1,V1)
        return Res '''

''' aligner = Aligner()

Sillabe, Scansione = aligner.align("metrica","Arma virumnque cano","Arma virumnque canone")

print(Sillabe) '''