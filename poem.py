
import nltk, pronouncing
from nltk.sentiment import SentimentIntensityAnalyzer
from line import Line

class Poem:
    #global

    def __init__(self, lines):
        self.lines = lines
        self.sentiment = 0
        self.rhyme_scheme = ""
        self.analyzed = False
        self.text = ""
        for line in self.lines:
                self.text += line.input
    
    def analyze_sentiment(self):
        if not self.analyzed:
            sia = SentimentIntensityAnalyzer()
            self.sentiment = sia.polarity_scores(self.text)
            self.analyzed = True
    
    def find_rhyme_scheme_half(self, index1, index2):
        i1 = index1
        i2 = index2
        
        if self.lines[i1].last_word[0] in self.lines[i2].last_word[1]:
            return "AA"
        else:
            return "AB"

    def final_rhyme_scheme(self, half1, half2):
        if half1 == "AA" and half2 == "AA":
            #AAAA
            if self.lines[0].last_word[0] == self.lines[1].last_word[0] \
                == self.lines[2].last_word[0] == self.lines[2].last_word[0]:
                return "AAAA"
            #if not same word, if each pair matches...
            if self.lines[0].last_word[0] in self.lines[2].last_word[1] or\
                self.lines[1].last_word[0] in self.lines[2].last_word[1] :
                return "AAAA"
            #AABB
            elif self.lines[0].last_word[0] not in self.lines[2].last_word[1]:
                return "AABB"
            elif self.lines[0].last_word[0] == self.lines[1].last_word[0] \
                and self.lines[2].last_word[0] == self.lines[3].last_word[0]:
                return "AABB"
        if half1 == "AB" and half2 == "AA":
            
            #ABAA
            if self.lines[0].last_word[0] in self.lines[2].last_word[1]:
                return "ABAA"
            #ABCC
            if self.lines[0].last_word[0] not in self.lines[2].last_word[1] and\
                self.lines[1].last_word[0] not in self.lines[2].last_word[1] :
                return "ABCC"
            #ABBB
            if self.lines[1].last_word[0] in self.lines[2].last_word[1]:
                return "ABBB"
            return
        if half1 == "AA" and half2 == "AB":
            
            #AAAB
            if self.lines[0].last_word[0] in self.lines[2].last_word[1] and \
            self.lines[0].last_word[0] not in  self.lines[3].last_word[1]:
                return "AAAB"
            #AABC
            #AABA
            return
            
            
        if half1 == "AB" and half2 == "AB":
            #ABCD
            #ABAC
            #ABBA
            #ABAB
            #ABBC
            #ABCA
            #ABCB
            return
    
        
def main():
    l = Line("Roses are red")
    l2 = Line("Violets are red")
    l3 = Line("Sugar is sweet")
    l4 = Line("And so are sweet")

    p = Poem([l,l2,l3,l4])
    print(p.analyze_sentiment)
    h1 = p.find_rhyme_scheme_half(0,1)
    h2 = p.find_rhyme_scheme_half(2,3)
    print(h1,h2)
    print(p.final_rhyme_scheme(h1,h2))

main()
"""
Roses are red
Violets are blue
Sugar is sweet
And so are you.
"""
        
        

