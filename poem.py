
import nltk, pronouncing
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import wordnet
from line import Line
import spacy
from collections import Counter
from string import punctuation
import random
import pronouncing

#nltk.download('vader_lexicon')

class Poem:
    """
    Defines a poem object
    """

    def __init__(self, lines):
        self.lines = lines
        self.sentiment = 0
        self.rhyme_scheme = ""
        self.analyzed = False
        self.sia = SentimentIntensityAnalyzer()
        self.nlp = spacy.load("en_core_web_sm")
        self.text = ""
        for line in self.lines:
                self.text += line.input

    
    def analyze_sentiment(self):
        if not self.analyzed:
            self.sentiment = self.sia.polarity_scores(self.text)['compound']
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
            
        if half1 == "AA" and half2 == "AB":
            #AAAB
            if self.lines[0].last_word[0] in self.lines[2].last_word[1] and \
            self.lines[0].last_word[0] not in  self.lines[3].last_word[1]:
                return "AAAB"
            #AABC
            if self.lines[0].last_word[0] not in self.lines[2].last_word[1] and\
            self.lines[2].last_word[1] not in  self.lines[3].last_word[1] and\
            self.lines[0].last_word[0] not in self.lines[3].last_word[1]:
                return "AABC"
            #AABA
            if self.lines[0].last_word[0] not in self.lines[2].last_word[1] and\
            self.lines[2].last_word[1] not in self.lines[3].last_word[1] and\
            self.lines[0].last_word[0] in self.lines[3].last_word[1]:
                return "AABA"
            
        if half1 == "AB" and half2 == "AB":
            not_1_list = [ self.lines[1].last_word[1],\
            self.lines[2].last_word[1],self.lines[3].last_word[1]]
            not_2_list = [ self.lines[0].last_word[1],\
            self.lines[2].last_word[1],self.lines[3].last_word[1]]
            not_3_list = [ self.lines[0].last_word[1],\
            self.lines[1].last_word[1],self.lines[3].last_word[1]]
            not_4_list = [ self.lines[0].last_word[1],\
            self.lines[1].last_word[1],self.lines[2].last_word[1]]

            #ABAC
            if self.lines[0].last_word[0] in self.lines[2].last_word[1] and\
            self.lines[0].last_word[1] not in self.lines[1].last_word[1] and\
            self.lines[0].last_word[0] not in self.lines[3].last_word[1]:
                return "ABAC"
            #ABBA
            elif self.lines[0].last_word[0] in self.lines[3].last_word[1] and\
            self.lines[1].last_word[1] in self.lines[2].last_word[1] and\
            self.lines[0].last_word[0] not in self.lines[1].last_word[1]:
                return "ABBA"
            #ABAB
            elif self.lines[0].last_word[0] in self.lines[2].last_word[1] and\
            self.lines[1].last_word[1] in self.lines[3].last_word[1] and\
            self.lines[0].last_word[0] not in self.lines[1].last_word[1]:
                return "ABAB"
           
            #ABCA
            elif self.lines[0].last_word[0] in self.lines[3].last_word[1] and\
            self.lines[1].last_word[1] not in self.lines[2].last_word[1] and\
            self.lines[0].last_word[0] not in self.lines[2].last_word[1] and\
            self.lines[1].last_word[0] not in self.lines[2].last_word[1]   :
                return "ABCA"
            #ABCB
            elif self.lines[1].last_word[0] in self.lines[3].last_word[1] and\
            self.lines[0].last_word[1] not in self.lines[2].last_word[1] and\
            self.lines[0].last_word[0] not in self.lines[1].last_word[1]:
                return "ABCB"
            #ABCD and #ABBC
            elif self.lines[0].last_word[0] not in not_1_list and \
            self.lines[1].last_word[0] not in not_2_list and \
            self.lines[2].last_word[0] not in not_3_list and \
            self.lines[3].last_word[0] not in not_4_list:
                if self.lines[1].last_word[0] in self.lines[2].last_word[1]:
                    return "ABBC"
                
                return "ABCD"
    
    def get_fitness(self, target):
        #maybe in future reward rhyming rhyme schemes 
        if not hasattr(self, 'fitness'):
            self.fitness = abs(self.sentiment - target)
        return abs(self.sentiment - target)
            
    def mutate_word(self):
        """
        Select a random line for mutation by word.
        """

        #pick which line we mutate
        line_index = random.randint(0, len(self.lines)-1)
        line = self.lines[line_index]
        #pick word from line (get word and POS tag)
        word_sel = line.get_random_word()
        if word_sel != None:
            word = word_sel[0]
            tag = word_sel[1]
        else:
            return
    
        word_syns = self.get_synonyms_antonyms(word)[0]
        word_syns = list(word_syns)
        len_word_syns = len(word_syns)
        word_syns = word_syns[0:len_word_syns//2]
        #get first half 
        # we want a synonym with same pos tag

        if len(word_syns) > 0:
            print(word_syns)
            syn = nltk.word_tokenize(random.choice(word_syns))
            print("syn", syn)
            #print(word,syn, word_syns, nltk.pos_tag(syn), tag)

            #print("sub ", syn[0], "for ", word)
            tok = line.tokens.index(word)
            line.tokens[tok] = syn[0]
            
            print("New line tokesn are",line.tokens)

            #if syllables different, update syllables
            word_syllables = pronouncing.phones_for_word(word)
            syn_syllables = pronouncing.phones_for_word(syn[0])
            try:
                old_syllables = pronouncing.syllable_count(word_syllables[0])
                new_syllables = pronouncing.syllable_count(syn_syllables[0])

                if ( old_syllables != new_syllables):
                    line.update_syllables(old_syllables, new_syllables)
            except IndexError:
                pass
    

            #update text of line 
            line.update_text(word, syn[0])
    
            #if word == line.last_word: 
                #print("last word")
                #we want rhymes

            #UPDATE THE LINE IN ThE POEM TOO THO
            self.lines[line_index] = line

            #fix poem text
            self.update_poem_text()
        
    def get_synonyms_antonyms(self, word):
        """
        https://www.holisticseo.digital/python-seo/nltk/wordnet
        """
        synonyms = []
        antonyms = []
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                synonyms.append(l.name())
                if l.antonyms():
                    antonyms.append(l.antonyms()[0].name())
        
        return [set(synonyms), set(antonyms)]

    def update_poem_text(self):
        self.text = ""
        for line in self.lines:
                self.text += line.input + "\n"


    def __str__(self):
        return"{0}".format(self.text)
        
            
    def __repr__(self):
        return "Poem({0})".format(self.lines)
        
def main():
    l = Line("Roses are terrible")
    l2 = Line("Violets are awful and blue")
    l3 = Line("Sugar is blown away")
    l4 = Line("And so are")

    p = Poem([l,l2,l3,l4])
    p.analyze_sentiment()
    #print(p.sentiment)
    #h1 = p.find_rhyme_scheme_half(0,1)
    #h2 = p.find_rhyme_scheme_half(2,3)
    #print(h1,h2)
    #print(p.final_rhyme_scheme(h1,h2))

    print(p)
    print(p.mutate_word())
    print(p)

#nltk.download('wordnet')
#nltk.download('omw-1.4')
#main()

"""
Roses are red
Violets are blue
Sugar is sweet
And so are you.
"""
        
        

