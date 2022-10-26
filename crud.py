"""CRUD functions."""

from model import db, User, Favorite, Brain_Wave, Focus, connect_to_db


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
    # ^ passed test


# Functions for FAVORITE class:
def create_favorite(user, brain_wave):
    """Create and return a new favorite
    User=user object, Frequency=frequency object"""

    favorite = Favorite(
        user=user, brain_wave=brain_wave)

    return favorite


# Functions for BRAIN WAVE class:
def create_brain_wave(brain_wave_id, brain_wave_name):
    """Create and return a new frequency."""

    brain_wave = Brain_Wave(
        brain_wave_id=brain_wave_id, 
        brain_wave_name=brain_wave_name)

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

    return Brain_Wave.query.filter(Brain_Wave.name == brain_wave_name).first()
    # ^ AttributeError: type object 'Brain_Wave' has no attribute 'name'


# Functions for FOCUS class:
def create_focus(user, focus):
    """Create and return a new focus
    User=user object, Focus=focus object"""

    focus = Focus(
        user=user, focus=focus)

    return focus
    # ^ TypeError: 'user' is an invalid keyword argument for Focus 


def get_focus_id(focus_id):

    return Focus.query.get(focus_id)


def get_focus(focus_name):

    return Focus.query.get(focus_name)




if __name__ == '__main__':
    from server import app
    connect_to_db(app)