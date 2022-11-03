from re import X
import nltk
import pronouncing

#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')

class Line:
    def __init__(self, input):
        self.input = input
        self.tokens = nltk.word_tokenize(input)
        self.tags = nltk.pos_tag(self.tokens)
        self.last_word = (self.tokens[-1], pronouncing.rhymes(self.tokens[-1]))
        self.syllables = self.count_syllables_in_line()
    
    def count_syllables_in_line(self):
        num_syllables = 0
        for word in self.tokens:
            pronunciation_list = pronouncing.phones_for_word(word)
            #for now just picking first of list 
            num_syllables += pronouncing.syllable_count(pronunciation_list[0])
        
        return num_syllables
        
    def __str__(self):
        x = self.input
        return f'{self.input}'
    
    def __repr__(self):
        return "Line({input})".format(self.input)


def m():
    print("hi")
    l = Line("hello there")
   
    print(pronouncing.syllable_count("HH AH0 L OW1"))


