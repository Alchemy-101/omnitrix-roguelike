# Omnitrix Roguelike (CLI)

A small text-based roguelike inspired by the show Ben 10. The player completes short runs made of rooms (combat/event/rest), transforms using limited Omnitrix energy, earns DNA, and unlocks new alien forms between sessions.

## Requirements
- Python 3.10+ recommended

## How to Run
From the project folder:
- Windows:
  - `python main.py`
- macOS/Linux:
  - `python3 main.py`

A `save.json` file will be created automatically to store DNA and unlocks.

## How to Play
- Choose **Start Run** to begin a new run.
- In combat, choose:
  - Basic Attack
  - Special Ability
  - Transform (costs Omnitrix energy)
- Earn DNA when you win combats and from some events.
- Go to **DNA Lab** to unlock new forms using DNA.

## Data Persistence
Progress is stored in `save.json`:
- DNA total
- unlocked forms
- max Omnitrix energy

## Notes
This project is designed to focus on clean variable naming, data types, input validation, and best practices for modular logic in a simple command-line program.
