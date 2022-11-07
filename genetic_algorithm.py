
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
    
    def selection(self):
        selected_poems = []
        total = 0
        for p in range(len(self.inspiring_set)):
            total += self.inspiring_set[p].get_fitness(self.target_mood)

        self.inspiring_set.sort(key=lambda x: x.fitness)
        count = 0
        
        for i in range(2 * len(self.inspiring_set)):
            count = 0
            random_number = random.SystemRandom().uniform(0,total)
            for z in range(len(self.inspiring_set)):
                count += self.inspiring_set[z].get_fitness(self.target_mood)
                if random_number <= count:
                    selected_poems.append(self.inspiring_set[z])
                    break
        return selected_poems

    
    
def main():
    ga = GeneticAlgorithm(2, "Boston")
    print(len(ga.inspiring_set))
    for i in range(10):
        ga.inspiring_set[i].analyze_sentiment()
        print("fitness",ga.inspiring_set[i].get_fitness(ga.target_mood))
        print("fitness assigned",ga.inspiring_set[i].fitness)
    #for poem in ga.inspiring_set:
        #print("x",poem.lines)
    print(ga.selection())
main()


