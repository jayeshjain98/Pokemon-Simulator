# Pokemon Simulator
A rest app developed using FAST API framework in python.

# Local Setup
To locally setup project clone the git repo using
# set up environment
```bash
git clone git@github.com:jayeshjain98/Pokemon-Simulator.git
```

# Install Packages
To set up python libraries run the commands below

# Set up environment
```bash
pip3 install -r src/pokemon_simulator/requirements.txt
```

# Serve the api
This shell command will serve the api on your localhost over port 8000
```bash
fastapi dev src/
```
# Request url and format
The api takes request at 3 end points in below format
* GET -http://127.0.0.1:8000/pokemons
* POST -http://127.0.0.1:8000/battle/
* GET -http://127.0.0.1:8000/battle/{battleId}

Where {battleID} can be obtained from the battle API
and {battleId} is of type uuid only.

The format for POST api request to perform battle is as follows
* Request :
```json
{
    "pokemon_a": "Bulbasaur",
    "pokemon_b": "Ivysaur"
}
```
* Response:
```json
{
    "battle_id": "bc19d9f4-1875-4e13-9051-4169eb52133c"
}
```

# For running test cases on api first serve the api 
```bash
pytest src/tests/
```
# For checking the code coverage of the project run
```bash
coverage run --source=src -m pytest -v src/tests && coverage report -m
```
