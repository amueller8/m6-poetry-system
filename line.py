import nltk
import pronouncing
import random

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
            if pronunciation_list:
                num_syllables += pronouncing.syllable_count(pronunciation_list[0])
            else:
                num_syllables += 0
        
        return num_syllables
    
    def update_text(self, old_word, new_word):
        #if new word has _, change it
        start = self.input.find(old_word)
        new_word = new_word.split("_")
        new_w_str = ""
        if len(new_word) > 1:
            for w in new_word:
                new_w_str += w + " "
        else:
             new_w_str = new_word[0] + " "

        self.input = self.input[0:start] + new_w_str + self.input[start+len(old_word):]
        

    def update_syllables(self, old_word_syll, new_word_syll):
        self.syllables -= old_word_syll
        self.syllables += new_word_syll
        

    def get_input(self):
        return self.input
    
    def get_tokens(self):
        return self.tokens

    def get_tags(self):
        return self.tags
        
    def __str__(self):
        x = self.input
        return f'{self.input}'
    
    def __repr__(self):
        return "Line({0})".format(self.get_input())
    
    def get_random_word(self):
        """
        Well, not quite random, in a specified category.
        Return selection and POS tag.
        """
        #https://stackoverflow.com/questions/15388831/what-are-all-possible-pos-tags-of-nltk 
        #select a VB* type, JJ* (adjective or ordinal), JJS superlative
        # NN or NNS (common noun singular or plural)
        
        tags = ["VB", "VBD", "VBG", "VBZ", "VBP", "JJ", "JJS", "JJR", "NN", "NNS"]
        
        #select a random type 
        matches = []
        type = random.choice(tags)
        iterations = 0
        while(len(matches) == 0):
            type = random.choice(tags)
            for t in range(len(self.tags)):
                #print(self.tags[t], "is ", type, "?\n")
                if self.tags[t] == type or type in self.tags[t]:
                    matches.append(t)
            iterations += 1
            if iterations > 10:
                return None
       # print("\nMATCHES",matches)

        if len(matches) > 1:
            return [self.tokens[random.choice(matches)] ,type]
        else:
            return [self.tokens[matches[0]], type]


def m():
    print("hi")
    l = Line("hello there")
    l2 = Line("Shall I compare thee to a summer's day? Thou art more temperate\
         and more glorious. And the harsh wind bites the lovely month of May,\
             summer leaves at all too short a date")

    print(pronouncing.syllable_count("HH AH0 L OW1"))

    print(l2.get_tokens(), l2.get_tags(), l2.get_random_word())
    print(l.get_tokens(), l.get_tags())

#m()


