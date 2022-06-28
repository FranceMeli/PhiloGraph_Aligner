from .latin_use_cltk import Scan_Hexameter
import nltk


class Textual_Object:

    "Classe che descrive un insieme di token (es. uno o più versi)"
    Tokenize = []

    def __init__(self,text=""):
        self.text = str(text)

    def Token(self):
        t = self.text
        tokenizer = nltk.RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(t)
        self.Tokenize=tokens   
        return self.Tokenize
    
    def Len(self):
        return len(self.text)

    def Metric_Scan(self):
        verse = self.text
        Metrica= Scan_Hexameter(verse)
        Scansione = Metrica.scansion
        Sillabe = Metrica.syllables

        return Sillabe, Scansione
    
