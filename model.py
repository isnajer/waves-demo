"""Models & Database Functions"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Users."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, 
                        autoincrement=True,
                        primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    records = db.relationship("User_Records", back_populates="user")

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'


class User_Records(db.Model):
    """User Records."""

    __tablename__ = 'records'

    user_records_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    created_on = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    brain_wave_id = db.Column(db.Integer, db.ForeignKey("brain_waves.brain_wave_id"))

    user = db.relationship("User", back_populates="records")
    brain_wave = db.relationship("Brain_Wave", back_populates="records")
    
    def __repr__(self):
        return f'<Record user_records_id={self.user_records_id} created_on={self.created_on} user_id={self.user_id} brain_wave_id={self.brain_wave_id}>'


class Brain_Wave(db.Model):
    """Brain Wave States."""

    __tablename__ = 'brain_waves'

    brain_wave_id = db.Column(db.Integer,
                                autoincrement=False,
                                primary_key=True)
    brain_wave_name = db.Column(db.String(50))
    description = db.Column(db.String(200))
    playlist = db.Column(db.String)
    
    records = db.relationship("User_Records", back_populates="brain_wave")

    def __repr__(self):
        return f'<Brain_Wave brain_wave_id={self.brain_wave_id} user_records_id={self.user_records_id}>' 


   



# #####################################################################
# # Helper functions;

def connect_to_db(flask_app, db_uri="postgresql:///waves", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = False
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = flask_app
    db.init_app(flask_app)



if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
    print("Connected to the db!")
    db.create_all()