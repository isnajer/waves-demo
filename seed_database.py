"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

# os.system('dropdb waves')
# os.system('createdb waves')


model.connect_to_db(server.app)
# model.db.create_all()

# Load brain wave data from JSON file
with open("data/brain_waves.json") as f:
    brain_wave_data = json.loads(f.read())

# Create brain waves, store them in list so we can use them
brain_wave_in_db = []
for brain_wave in brain_wave_data:
    brain_wave_id, brain_wave_name, description, playlist = (
        brain_wave["brain_wave_id"],
        brain_wave["brain_wave_name"],
        brain_wave["description"],
        brain_wave["playlist"],
    )

    db_brain_wave = crud.create_brain_wave(brain_wave_id, brain_wave_name, description, playlist)
    brain_wave_in_db.append(db_brain_wave)

model.db.session.add_all(brain_wave_in_db)
model.db.session.commit()