from cltk.prosody.lat.hexameter_scanner import HexameterScanner
from cltk.lemmatize.lat import LatinBackoffLemmatizer
from cltk.phonology.lat.phonology import LatinSyllabifier
from cltk.stem.lat import stem

def InfoLatin(vars):
    Lat_data=[]
    if(isinstance(vars,list)):
        for i in range(0,len(vars)):
            tokens=vars[1]
            info = { 'Lemma': stem(tokens) }
            Lat_data.append(info)
    else:
        info = { 'Lemma': stem(vars) }
        Lat_data.append(info)
    
    return Lat_data

def Lemmatize(tokens):
    lemmatizer= LatinBackoffLemmatizer()
    LemmatizeList= lemmatizer.lemmatize(tokens) 
    List=[]
    for i in LemmatizeList:
        List.append(i[1])
    return List

def Scan_Hexameter(Hex):
    scanner = HexameterScanner()
    hexameter = scanner.scan(Hex)
    return hexameter

def syllabifier(word):
    syll = LatinSyllabifier.syllabify(word)
    return syll
