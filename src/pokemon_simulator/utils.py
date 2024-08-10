import pandas as pd
from difflib import SequenceMatcher

# Dictionary to hold battle statuses
battle_status = {}

# Load the dataset
df = pd.read_csv('src/pokemon_simulator/pokemon.csv')

def get_paginated_data(skip: int, limit: int):
    return df.iloc[skip: skip + limit][["name"]].to_dict(orient="records")

def similarity_score(name1, name2):
    return SequenceMatcher(None, name1, name2).ratio()

def find_most_relevant_name(input_name, name_list):
    """
    Finds the most relevant name from a list of names based on the highest similarity score.
    Returns the name with the highest score.
    """
    input_name = input_name.lower()
    highest_score = (len(input_name)-1)/len(input_name)
    most_relevant_name = None
    
    for name in name_list:
        name = name.lower()
        score = similarity_score(input_name, name)
        
        if score >= highest_score:
            highest_score = score
            most_relevant_name = name
    
    return most_relevant_name

def run_battle(battle_id, pokemon_a, pokemon_b):
    try:
        result = battle_simulator(pokemon_a, pokemon_b)
        battle_status[battle_id]["status"] = "BATTLE_COMPLETED"
        battle_status[battle_id]["result"] = result
    except Exception as e:
        battle_status[battle_id]["status"] = "BATTLE_FAILED"
        battle_status[battle_id]["result"] = None


# Function to normalize and correct spelling mistakes
def normalize_name(name):
    return name.lower().strip()

# Function to calculate damage
def calculate_damage(attacker, defender):
    # Extract the needed fields from the dataset for attacker and defender
    # Calculate damage based on the logic
    type1 = attacker["type1"]
    type2 = attacker["type2"]

    defence_type2 = ((defender["against_"+type2]/4)*100) if type2 else 0
    damage = (attacker["attack"]/200)*100 - (((defender["against_"+type1]/4)*100) + defence_type2)
    return damage

# Battle simulator function
def battle_simulator(pokemon_a, pokemon_b):
    pokemon_a = normalize_name(pokemon_a)
    pokemon_b = normalize_name(pokemon_b)

    #replace nan
    df["type2"].fillna("",inplace=True)
    
    # Fetch Pokemon data from dataframe
    poke_a_data = df[df['name'].str.lower() == pokemon_a].iloc[0]
    poke_b_data = df[df['name'].str.lower() == pokemon_b].iloc[0]
    
    # Battle round 1
    damage_a_to_b = calculate_damage(poke_a_data, poke_b_data)
    # Battle round 2
    damage_b_to_a = calculate_damage(poke_b_data, poke_a_data)
    
    if damage_a_to_b > damage_b_to_a:
        winner = poke_a_data["name"]
        margin = damage_a_to_b
    elif damage_b_to_a > damage_a_to_b:
        winner = poke_b_data["name"]
        margin = damage_b_to_a
    else:
        winner = "Draw"
        margin = 0
    
    return {"winnerName": winner, "wonByMargin": margin}