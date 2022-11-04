"""CRUD functions."""

from model import db, User, User_Records, Brain_Wave, connect_to_db


# Functions for USER class:
def create_user(email, password):
    """Create and return a new user.
    Email= string, Password= string"""
    

    user = User(email=email, password=password)

    return user
    # ^ passed test


def get_users():
    """"Return all users"""

    return User.query.all()
    # ^ passed test


def get_user_by_id(user_id):
    """Returns the user with that ID"""

    return User.query.get(user_id)
    # ^ passed test


def get_user_by_email(email):
    """Returns user by email"""

    return User.query.filter(User.email == email).first()
    # ASK ABOUT THIS WHY FILTER INSTEAD OF GET?
    # ^ passed test


# Functions for USER RECORDS class:
def create_user_record(user_id, created_on, brain_wave_id):
    """Create and return a new favorite"""

    record = User_Records(
        user_id=user_id,
        created_on=created_on,
        brain_wave_id=brain_wave_id)

    return record


def get_user_record():
    """Return all favorites."""

    return User_Records.query.all()


def get_user_record_id(user_record_id):
    """Return all Brin Waves by id."""

    return User_Records.query.get(user_record_id)


# Functions for BRAIN WAVE class:
def create_brain_wave(brain_wave_id, brain_wave_name, description, playlist):
    """Create and return a new frequency."""

    brain_wave = Brain_Wave(
        brain_wave_id=brain_wave_id, 
        brain_wave_name=brain_wave_name,
        description=description,
        playlist=playlist)

    return brain_wave


def get_brain_waves():
    """Return all Brain Waves."""

    return Brain_Wave.query.all()
    # ^ passed test


def get_brain_wave_id(brain_wave_id):
    """Return all Brin Waves by id."""

    return Brain_Wave.query.get(brain_wave_id)
    # ^ passed test


def get_brain_wave_name(brain_wave_name):
    """Return all Brain Waves by name."""

    return Brain_Wave.query.filter(Brain_Wave.brain_wave_name == brain_wave_name).first()
    # ^ AttributeError: type object 'Brain_Wave' has no attribute 'name'
    # Should it be `return Brain_Wave.query.get(brain_wave_name)`




if __name__ == '__main__':
    from server import app
    connect_to_db(app)