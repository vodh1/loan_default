import json
from django.shortcuts import render
import pickle
import pandas as pd
import numpy as np

pokemon = pd.read_csv('pokemon.csv')
cln_pokemon = pd.read_csv('cleaned_pokemon.csv')

POKEMON_NAMES = pokemon['Name'].tolist()

def home(request):
    return render(request, 'index.html', {'pokemon_names': POKEMON_NAMES})

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

    # Get the data of the pokemons from cleaned pokemon CSV
    first_pokemon_data = getPokemonValues(first_pokemon).values[:, 3:][0] # get the values from the 4th column
    second_pokemon_data = getPokemonValues(second_pokemon).values[:, 3:][0]
    result = getPredictions(first_pokemon_data, second_pokemon_data)

    stats = ['Name', 'HP','Attack','Defense','Sp. Atk','Sp. Def','Speed']

    # convert array to dictionary
    pokemon1 = dict(zip(stats, getPokemonValues(first_pokemon).values[:, 2:][0]))
    pokemon2 = dict(zip(stats, getPokemonValues(second_pokemon).values[:, 2:][0]))
    labels = ['HP','Attack','Defense','Sp. Atk','Sp. Def','Speed']
    data1 = [pokemon1[s] for s in labels] # get only all the values
    data2 = [pokemon2[s] for s in labels] # get only all the values

    return render(request, 'result.html', {
      'result':      result,
      'pokemon1':    pokemon1,
      'pokemon2':    pokemon2,
      'labels_json': json.dumps(labels),
      'data1_json':  json.dumps(data1),
      'data2_json':  json.dumps(data2),
    })


def getPokemonValues(pokemon_name):
    # Get the data of the pokemons from cleaned pokemon CSV
    first_pokemon_data = cln_pokemon.loc[cln_pokemon['Name'] == pokemon_name]
    return first_pokemon_data