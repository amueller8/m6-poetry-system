
from weather_call import WeatherCall
from poem import Poem
from line import Line
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
            lines = self.process_poem_file(filename)
            while (len(lines) % 4 == 0 and len(lines) > 0):
                poem = Poem(lines[0:4])
                self.inspiring_set.append(poem)
                lines = lines[4:]


    
    def process_poem_file(self,file):
        lines = []
        with open(file, 'r') as f:
            my_line = f.readline()#may need to convert from one line to 
            while my_line:
                if my_line != "":
                    print(Line(my_line))
                    lines.append(Line(my_line))
                
                my_line = f.readline()

        return lines
    
    
def main():
    ga = GeneticAlgorithm(2, "Boston")
    print(ga.inspiring_set)
        
main()


