from line import Line
from api_keys import API_Key
import requests, json 
import os


def main():
    
    print(query_city_for_weather("Boston"))
main()