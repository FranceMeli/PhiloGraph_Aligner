import nltk
from .latin_use_cltk import Scan_Hexameter, Lemmatize
import numpy as np
from difflib import SequenceMatcher

def Split(word):
    char=[]
    for i in word:
        char.append(i)
    return char

def transformArray(x):
    y=[]
    for i in x:
        y.append(i)
    return y

def Token(frasi):
    tokensTot=[]
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(frasi)
    return tokens

def ParallelStringResult(lezione,variante): 
    align_array=[]
    for i in range(0,len(lezione)):
        d={"S":lezione[i], "T":variante[i]}
        align_array.append(d)     
    return align_array

def CheckLen(Verso1,Verso2):
    if (len(Verso1)<len(Verso2)):
        Verso1.append("-")
        ''' CheckLen(Verso1,Verso2) '''
    elif (len(Verso1)>len(Verso2)):
        Verso2.append("-")
        ''' CheckLen(Verso1,Verso2) '''
    return Verso1,Verso2


def MetricAlignPedecerto(pedecerto,cltk):
    cltk_scan = trasformCltkHesameter(cltk)
    ped_scan = ""
    A=[]
    for i in pedecerto:
        if(i=="A" or i=="T"):
            ped_scan=ped_scan+"-"
        if (i=="b" or i=="c" or i=="X"):
            ped_scan=ped_scan+"U"
    cltk_scan = transformArray(cltk_scan)
    ped_scan = transformArray(ped_scan)
    A.append(cltk_scan)
    A.append(ped_scan)
    V1,V2=cltk_pedecerto_Alignment(A)
    Res = ParallelStringResult(V1,V2)     
    return Res

def trasformCltkHesameter(he_cltk):
    cltk_scan = he_cltk[0]
    x = cltk_scan.replace(" ", "")
    return x

def cltk_pedecerto_Alignment(Var):
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
    Variante1=[]
    Variante2=[]

    while(n<len(V1) and m<len(V2)):
        ProvaN=V1[n]
        ProvaM=V2[m]
        L1=len(V1)-n
        L2=len(V2)-m
        if (ProvaN == ProvaM):
            Variante1.append(ProvaN)
            Variante2.append(ProvaM)
            n=n+1
            m=m+1
        else: 
            if (L1>L2):
                Variante1.append(ProvaN)
                Variante2.append("gap")
                n=n+1
            elif (L2>L1):
                Variante2.append(ProvaM)
                Variante1.append("gap")
                m=m+1
            else :
                Variante1.append(ProvaN)
                Variante2.append(ProvaM)
                n=n+1
                m=m+1
                
    while(n<len(V1)):
        
        Variante1.append(V1[n])
        n=n+1
    while(m<len(V2)):
        Variante2.append(V2[m])
        m=m+1

    return Variante1, Variante2

def SingleMetricAlignment(verse):
    Scansione=[]
    Sillabe=[]
    Metri = Scan_Hexameter(verse)
    for i in Metri.syllables:
        Sillabe.append(i)
    Scansione.append(Metri.scansion)
    Res=ParallelStringResult(Sillabe,Sillabe)
    return Scansione,Res

def SingleWordAlignment(word):
    char=Split(word)
    Res=ParallelStringResult(char,char)
    return Res

def SingleVerseAlignment(g,Verse):
    if (g=="parole"):
        V1=Token(Verse)
        Res=ParallelStringResult(V1,V1) 
    else: 
        Tok=Token(Verse)
        V1=Lemmatize(Tok)
        Res=ParallelStringResult(V1,V1) 
    return Res

def levenshtein(seq1, seq2):
        size_x = len(seq1) + 1
        size_y = len(seq2) + 1
        matrix = np.zeros ((size_x, size_y))
        for x in range(size_x):
            matrix [x, 0] = x
        for y in range(size_y):
            matrix [0, y] = y
        sol=[]
        for x in range(1, size_x):
            minus=max(size_x,size_y)
            for y in range(1, size_y):
                if seq1[x-1] == seq2[y-1]:
                    matrix [x,y] = min(
                        matrix[x-1, y] + 1,
                        matrix[x-1, y-1],
                        matrix[x, y-1] + 1
                    )
                else:
                    matrix [x,y] = min(
                        matrix[x-1,y] + 1,
                        matrix[x-1,y-1] + 1,
                        matrix[x,y-1] + 1
                    )

                if matrix[x,y]< minus:
                    minus=matrix[x,y]
            sol.append(minus)        
            """     print (matrix)      
            print (sol) """
        return (matrix[size_x - 1, size_y - 1])

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
    return [v1,v2]

