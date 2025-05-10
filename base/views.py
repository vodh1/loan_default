import json
from django.shortcuts import render
import pickle
import pandas as pd
import numpy as np

# pokemon = pd.read_csv('pokemon.csv')
# cln_pokemon = pd.read_csv('cleaned_pokemon.csv')

# POKEMON_NAMES = pokemon['Name'].tolist()

def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')   

def getPredictions(first_pokemon, second_pokemon):
    model = pickle.load(open('model.pkl', 'rb'))

    X_sample = np.concatenate((first_pokemon, second_pokemon))

    prediction = model.predict([X_sample])
    
    # result 0 = first_pokemon wins
    # result 1 = second_pokemon wins
    return prediction[0]

def result(request):
    first_pokemon = request.GET['first_pokemon']
    second_pokemon = request.GET['second_pokemon']

    

    return render(request, 'result.html')


