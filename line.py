import nltk 
import pronouncing 

class Line:
    def __init__(self, input):
        self.tokens = nltk.tokenize(input)
        self.last_word = (self.tokens[-1], pronouncing.rhymes(self.tokens[-1]))
    
    def count_syllables_in_line(self):
        num_syllables = 0
        for word in self.tokens:
            pronunciation_list = pronouncing.phones_for_word(word)
            num_syllables += pronouncing.syllable_count(pronunciation_list[0])

