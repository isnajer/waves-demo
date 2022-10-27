"""CRUD functions."""

from model import db, User, Favorite, Brain_Wave, Focus, Sound, connect_to_db


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


# Functions for FAVORITE class:
def create_favorite(favorite_id):
    """Create and return a new favorite"""

    favorite = Favorite(
        favorite_id=favorite_id)

    return favorite


def get_favorites():
    """Return all favorites."""

    return Favorite.query.get()


# Functions for BRAIN WAVE class:
def create_brain_wave(brain_wave_id, brain_wave_name, description):
    """Create and return a new frequency."""

    brain_wave = Brain_Wave(
        brain_wave_id=brain_wave_id, 
        brain_wave_name=brain_wave_name,
        description=description)

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


# Functions for FOCUS class:
def create_focus(focus_id, focus_name):
    """Create and return a new focus
    User=user object, Focus=focus object"""

    focus = Focus(
        focus_id=focus_id,
        focus_name=focus_name)

    return focus
    # ^ TypeError: 'user' is an invalid keyword argument for Focus 

def get_focus():
    """Return all focuses."""

    return Focus.query.get()


def get_focus_id(focus_id):
    """Return all focuses by id."""

    return Focus.query.get(focus_id)


def get_focus(focus_name):
    """Return all focuses by name."""

    return Focus.query.get(focus_name)


# Functions for SOUND class:
def create_sound(sound_id, sound_name, description):
    """Create and return a new sound"""

    sound = Sound(
        sound_id=sound_id,
        sound_name=sound_name,
        description=description)

    return sound
     

def get_sounds():
    """Return all sounds."""

    return Sound.query.get()


def get_sound_id(sound_id):
    """Return all sounds by id."""

    return Sound.query.get(sound_id)


def get_sound_name(sound_name):
    """Return all sounds by name."""

    return Sound.query.get(sound_name)




if __name__ == '__main__':
    from server import app
    connect_to_db(app)