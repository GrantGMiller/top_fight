import json
import os
import random


def GetStats(ID):
    path = f'stats\\{ID}.json'
    if not os.path.exists(path):
        d = {
            'attack': 0,
            'defense': 0,
            'spin': 0,
        }

        points = 66 * len(d)

        while points > 0:
            key = random.choice(list(d.keys()))
            if d[key] < 100:
                d[key] += 1
                points -= 1

        with open(path, mode='wt') as file:
            file.write(json.dumps(d, indent=2, sort_keys=True))
            return d
    else:
        with open(path, mode='rt') as file:
            return json.loads(file.read())
