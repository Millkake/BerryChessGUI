import json

with open(r'saves/pvs_games/pvs_save_1.json', 'r') as f:
    print(json.load(f))