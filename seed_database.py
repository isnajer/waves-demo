"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb waves')
os.system('createdb waves')


model.connect_to_db(server.app)
model.db.create_all()