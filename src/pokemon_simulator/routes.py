import uuid
from src.pokemon_simulator.utils import *
from src.pokemon_simulator.schemas import Pokemons
from fastapi import BackgroundTasks, HTTPException, APIRouter

router = APIRouter()

# API 1: Listing API with pagination
@router.get("/pokemons/")
def list_pokemons(skip: int = 0, limit: int = 10):
    data = get_paginated_data(skip, limit)
    return data

# API 2: Battle API
@router.post("/battle/")
async def start_battle(pokemons: Pokemons , background_tasks: BackgroundTasks):
    pokemon_a = find_most_relevant_name(pokemons.pokemon_a,df['name'].to_list())
    pokemon_b = find_most_relevant_name(pokemons.pokemon_b,df['name'].to_list())
    if not pokemon_a:
        raise HTTPException(status_code=400, detail="Wrong name for pokemon_a entered")
    elif not pokemon_b:
        raise HTTPException(status_code=400, detail="Wrong name for pokemon_b entered")
    
    battle_id = str(uuid.uuid4())
    battle_status[battle_id] = {"status": "BATTLE_INPROGRESS", "result": None}
    run_battle(battle_id, pokemon_a, pokemon_b)
    background_tasks.add_task(run_battle, battle_id, pokemon_a, pokemon_b)
    
    return {"battle_id": battle_id}

# API 3: Check battle status
@router.get("/battle/{battle_id}")
def get_battle_status(battle_id: str):
    if battle_id not in battle_status:
        raise HTTPException(status_code=404, detail="Battle ID not found")
    
    return battle_status[battle_id]