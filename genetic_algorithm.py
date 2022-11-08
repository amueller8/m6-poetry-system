
from weather_call import WeatherCall
from poem import Poem
from line import Line
import random
import glob

class GeneticAlgorithm:

    def __init__(self, iterations, city_name, state_name=""):
        
        self.iterations = iterations
        self.inspiring_set = []
        
        weather_call = WeatherCall()
        if state_name != "":
            weather = weather_call.query_city_for_weather(city_name,\
                state_name)
        else:
            weather = weather_call.query_city_for_weather(city=city_name)
        
        self.weather = weather
        self.target_mood = weather_call.determine_weather_sentiment(weather)
        for filename in glob.glob("quatrains/*.txt"):
            try:
                lines = self.process_poem_file(filename)
                while (len(lines) % 4 == 0 and len(lines) > 0):
                    poem = Poem(lines[0:4])
                    self.inspiring_set.append(poem)
                    lines = lines[4:]
            except IndexError:
                continue


    
    def process_poem_file(self,file):
        lines = []
        with open(file, 'r') as f:
            my_line = f.readline()#may need to convert from one line to 
            while my_line:
                if my_line != "" and my_line != "\n":
                    #print(Line(my_line))
                    lines.append(Line(my_line))
                
                my_line = f.readline()

        return lines
    
    def pre_selection(self):
        for i in self.inspiring_set:
            i.analyze_sentiment()
            
    
    def selection(self):
        """
        Does selection.
        Attempt to normalize to ints by * fitness by 50 and casting to int.
        
        """
        selected_poems = []
        total = 0
        for p in range(len(self.inspiring_set)):
            total += int(self.inspiring_set[p].get_fitness(self.target_mood)*50) 

        self.inspiring_set.sort(key=lambda x: (x.fitness*50))
        count = 0
        
        for i in range(2 * len(self.inspiring_set)):
            count = 0
            random_number = random.randint(0,total)
            #random_number = random.SystemRandom().uniform(0,total)
            for z in range(len(self.inspiring_set)):
                count += int(self.inspiring_set[z].get_fitness(self.target_mood) * 50)
                if random_number <= count:
                    selected_poems.append(self.inspiring_set[z])
                    break
        return selected_poems
    
    def selection_2(self):
        
        self.pre_selection()
        print(self.target_mood, " is mood. Weather is ", self.weather)
        minDiff = 1 #sentiment between -1 and 1
        poem = self.inspiring_set[1]
        
        for i in self.inspiring_set:
            if abs(i.get_fitness(self.target_mood) - self.target_mood) <= minDiff:
                minDiff = abs(i.get_fitness(self.target_mood) - self.target_mood)
                poem = i
               
        
        return poem, minDiff
        

    
    def recombination(self, selected_poems):
        """
        The selected poems are recombined through crossover.
        Try to match rhyme pattern at crossover point?

        Args:
            selected_poems (Poem[]): A list of the poems produced by
            selection, which is double the size of the initial population.
        """
        new_poems = []
        for i in range(0, len(selected_poems), 2):
            if selected_poems[i].get_fitness() < \
                    selected_poems[i + 1].get_fitness():
                random_index = random.randint(0, int(
                    selected_poems[i].get_fitness() * 50))
            else:
                random_index = random.randint(0, int(
                    selected_poems[i + 1].get_fitness() * 50))
            #hard code halfway split ??
            #random_index = 2 
            first_half = selected_poems[i].lines[0:random_index]
            second_half = selected_poems[i + 1].lines[random_index:]
            combined_list = self.check_fix_duplicates_recombination(first_half,
                                                                    second_half
                                                                    )
            new_poem = Poem(combined_list)
                    
            new_poems.append(new_poem)
        self.inspiring_set = new_poems

    
    
def main():
    ga = GeneticAlgorithm(2, "Boston")
    print(len(ga.inspiring_set))
    #ga.pre_selection()
    #for poem in ga.inspiring_set:
        #print("x",poem.lines)
    #print(len(ga.selection()))
    poem, diff = ga.selection_2()
    print("Poem that best fits mood, with a score of ", diff,  "is ", poem)
    ga2 = GeneticAlgorithm(2, "Dubai")
    poem, diff = ga2.selection_2()
    print("Poem that best fits mood, with a score of ", diff,  "is ", poem)
   

main()


