import numpy as np
from difflib import SequenceMatcher
from cltk.tag.pos import POSTag

a = "dsa jld lal"
b = "dsajld kll"
c = "dsc jle kal"
d = "dsd jlekal"

''' Tag = POSTag('lat')
A = Tag.tag_tnt('arma uirum cano qui primus ab oris')
print(A) '''

def findBestVariants2(variants):

    s = SequenceMatcher()
    Score=[]
    for i in range(len(variants)):
        x = variants[i]
        s.set_seq1(x)
        for j in range(i+1,len(variants)):
            Dict={}
            y = variants[j]
            s.set_seq2(y)
            Dict={ "v1": x, "v2": y, "ratio": s.ratio()}
            Score.append(Dict)
    best=Score[0]
    max=0
    for i in range(0,len(Score)):
        ratio=Score[i]['ratio']
        if ratio > max:
            max=ratio
            best=Score[i]
    v1=best['v1']
    v2=best['v2']
    return [v1,v2]

def findBestVariants(variants):
    
    s = SequenceMatcher()
    Score=[]
    x = variants[0]
    s.set_seq1(x)
    for j in range(1,len(variants)):
        Dict={}
        y = variants[j]
        s.set_seq2(y)
        Dict={ "v1": x, "v2": y, "ratio": s.ratio()}
        Score.append(Dict)
    best=Score[0]
    max=0
    for i in range(0,len(Score)):
        ratio=Score[i]['ratio']
        if ratio > max:
            max=ratio
            best=Score[i]
    v1=best['v1']
    v2=best['v2']
    print(Score)
    return [v1,v2]

''' variants = ["Nec", "et", "haut", "haud", "non"]
CC,DD=findBestVariants(variants)
print (CC,DD) '''

def Split(word):
    char=[]
    for i in word:
        char.append(i)
    return char
    
def ParallelStringResult(lezione,variante): 
    align_array=[]
    for i in range(0,len(lezione)):
        d={"S":lezione[i], "T":variante[i]}
        align_array.append(d)     
    return align_array

def levenshtein_distance(string1, string2):
    n1 = len(string1)
    n2 = len(string2)
    return _levenshtein_distance_matrix(string1, string2)[n1, n2]

def damerau_levenshtein_distance(string1, string2):
    n1 = len(string1)
    n2 = len(string2)
    return _levenshtein_distance_matrix(string1, string2, True)[n1, n2]

def get_ops(string1, string2, is_damerau=False):
    dist_matrix = _levenshtein_distance_matrix(string1, string2, is_damerau)
    i, j = _levenshtein_distance_matrix(string1, string2, is_damerau).shape
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

def execute_ops(ops, string1, string2):
    strings = [string1]
    string = list(string1)
    shift = 0
    for op in ops:
        i, j = op[1], op[2]
        if op[0] == 'delete':
            del string[i + shift]
            shift -= 1
        elif op[0] == 'insert':
            string.insert(i + shift + 1, string2[j])
            shift += 1
        elif op[0] == 'replace':
            string[i + shift] = string2[j]
        elif op[0] == 'transpose':
            string[i + shift], string[j + shift] = string[j + shift], string[i + shift]
        strings.append(''.join(string))
    return strings

def _levenshtein_distance_matrix(string1, string2, is_damerau=False):
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


W_Al = get_ops( "Insequitur", "Itcaelo", is_damerau=False)
def al(W_Al):
    lezione = "Insequitur"
    variante = "Itcaelo"
    for i in range(0,len(W_Al)):
            operation=W_Al[i][0]
            posS=W_Al[i][1]
            posT=W_Al[i][2]
            if( not(posS<0) ):
                if operation=="insert":
                    lezione= lezione[:posS] + "-" + lezione[posS:]      
                elif operation=="delete":
                    variante= variante[:posT] + "-" + variante[posT:]

        
    S1=Split(lezione)     
    S2=Split(variante) 
    return S1,S2    

def alignMetr(Var):
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
       
        return Verso1, Verso2


def Metric_Scan(v1):
        verse = v1
        Metrica=v1 
        ''' ffffffffffffffffffffffffffffff '''
        Scansione = Metrica.scansion
        Sillabe = Metrica.syllables

        return Sillabe, Scansione

def metric(v1,v2):
            Sillabe = []
            Scansione = []
            syll1,scan1=Metric_Scan(v1)
            syll2,scan2=Metric_Scan(v2)
            Sillabe.append(syll1)
            Sillabe.append(syll2)
            Scansione.append(scan1)
            Scansione.append(scan2)
            V1=[]
            V2=[]
           
            if( len(Sillabe[0]) != len(Sillabe[1]) ):
                V1,V2=alignMetr(Sillabe)
                Res=ParallelStringResult(V1,V2)
            else: 
                Res=ParallelStringResult(Sillabe[0],Sillabe[1])

            return Res
Au=['Insequitur clamorque uirum stridorque rudentum.', 'it caelo clamorque uirum stridorque rudentem', 'it caelo clamorque uirum stridorque rudentem']




''' A=metric(Au[0],Au[1])
print(A) '''
''' Al=ParallelStringResult(S1,S2) '''
''' Op=W_Al
print(al(W_Al)) '''
''' print(S1)
print(S2) '''

''' string1 = ["Arma","virum","cano","Enea"]
string2 = ["Arma","Lavinaque","canto"]
for is_damerau in [True, False]:
    if is_damerau:
        print('=== damerau_levenshtein_distance ===')
    else:
        print('=== levenshtein_distance ===')

print(dist_matrix)
ops = get_ops(string1, string2, is_damerau=is_damerau)
print(ops)
res = execute_ops(ops, string1, string2)
print(res) '''
