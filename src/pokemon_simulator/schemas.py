from pydantic import BaseModel

class Pokemons(BaseModel):
    pokemon_a: str
    pokemon_b: str