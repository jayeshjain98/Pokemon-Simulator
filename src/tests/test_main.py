import unittest
from fastapi.testclient import TestClient
from src import app
from src.pokemon_simulator.utils import battle_simulator, normalize_name, find_most_relevant_name

client = TestClient(app)

class TestPokemonSimulator(unittest.TestCase):
    
    def test_normalize_name(self):
        self.assertEqual(normalize_name("Pikachu"), "pikachu")
        self.assertEqual(normalize_name("   CHARMANDER   "), "charmander")
        self.assertEqual(normalize_name("BuLbAsAuR"), "bulbasaur")
    
    def test_list_pokemons(self):
        response = client.get("/pokemons/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)
    
    def test_battle_simulator(self):
        # Mock Pokémon data
        pokemon_a = "Pikachu"
        pokemon_b = "Charmander"
        result = battle_simulator(pokemon_a, pokemon_b)
        self.assertIn(result["winnerName"], [pokemon_a, pokemon_b, "Draw"])
        self.assertIsInstance(result["wonByMargin"], (int, float))
    
    def test_start_battle(self):
        # Start a battle between Pikachu and Charmander
        response = client.post("/battle/", json={"pokemon_a": "Pikachu", "pokemon_b": "Charmander"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("battle_id", response.json())
    
    def test_get_battle_status(self):
        # Start a battle to get a valid battle_id
        response = client.post("/battle/", json={"pokemon_a": "Pikachu", "pokemon_b": "Charmander"})
        battle_id = response.json()["battle_id"]
        
        # Check the status of the battle
        response = client.get(f"/battle/{battle_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.json()["status"], ["BATTLE_INPROGRESS", "BATTLE_COMPLETED", "BATTLE_FAILED"])
    
    def test_battle_id_not_found(self):
        # Check a non-existent battle ID
        response = client.get("/battle/non_existent_id")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Battle ID not found", response.json()["detail"])

    def test_invalid_pokemon_name(self):
        # Test with an invalid Pokémon name
        response = client.post("/battle/", json={"pokemon_a": "InvalidPokemon", "pokemon_b": "Charmander"})
        print(response.json())
        self.assertEqual(response.status_code, 400)
        self.assertIn("Wrong name for pokemon_a entered", response.json()["detail"])

    def test_exact_match(self):
        name_list = ["Alice", "Alicia", "Aline", "Bob"]
        input_name = "Alice"
        result = find_most_relevant_name(input_name, name_list)
        self.assertEqual(result, "alice")

    def test_one_letter_difference(self):
        name_list = ["Alice", "Alicia", "Aline", "Bob"]
        input_name = "Alic"
        result = find_most_relevant_name(input_name, name_list)
        self.assertEqual(result, "alice")

    def test_multiple_close_matches(self):
        name_list = ["Alice", "Alicia", "Aline"]
        input_name = "Alici"
        result = find_most_relevant_name(input_name, name_list)
        self.assertEqual(result, "alicia")

    def test_no_relevant_match(self):
        name_list = ["Xavier", "Yvonne", "Zach"]
        input_name = "Alice"
        result = find_most_relevant_name(input_name, name_list)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()