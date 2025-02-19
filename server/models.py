#models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from config import db, bcrypt

user_guitar_images = db.Table(
    'user_guitar_images',
    db.Column('user_guitar_id', db.Integer, db.ForeignKey('user_guitar.id'), primary_key=True),
    db.Column('image_id', db.Integer, db.ForeignKey('image.id'), primary_key=True)
)

model_pickups = db.Table(
    'model_pickups',
    db.Column('model_id', db.Integer, db.ForeignKey('model.id'), primary_key=True),
    db.Column('pickup_id', db.Integer, db.ForeignKey('guitar_pickup.id'), primary_key=True)
)

user_guitar_pickups = db.Table(
    'user_guitar_pickups',
    db.Column('user_guitar_id', db.Integer, db.ForeignKey('user_guitar.id'), primary_key=True),
    db.Column('pickup_id', db.Integer, db.ForeignKey('guitar_pickup.id'), primary_key=True)
)

model_body = db.Table(
    'model_body',
    db.Column('model_id', db.Integer, db.ForeignKey('model.id'), primary_key=True),
    db.Column('body_id', db.Integer, db.ForeignKey('body.id'), primary_key=True)
)

model_fretboard = db.Table(
    'model_fretboard',
    db.Column('model_id', db.Integer, db.ForeignKey('model.id'), primary_key=True),
    db.Column('fretboard_id', db.Integer, db.ForeignKey('fretboard.id'), primary_key=True)
)

model_pickguard = db.Table(
    'model_pickguard',
    db.Column('model_id', db.Integer, db.ForeignKey('model.id'), primary_key=True),
    db.Column('pickguard_id', db.Integer, db.ForeignKey('pickguard.id'), primary_key=True)
)

model_switch = db.Table(
    'model_switch',
    db.Column('model_id', db.Integer, db.ForeignKey('model.id'), primary_key=True),
    db.Column('switch_id', db.Integer, db.ForeignKey('switch.id'), primary_key=True)
)

model_controls = db.Table(
    'model_controls',
    db.Column('model_id', db.Integer, db.ForeignKey('model.id'), primary_key=True),
    db.Column('controls_id', db.Integer, db.ForeignKey('controls.id'), primary_key=True)
)

# User Model
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), nullable=False)
    #_password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), nullable=False)

    # Relationship to guitars
    user_guitars = db.relationship('UserGuitar', back_populates='owner')


    @validates('role')
    def validate_role(self, key, role):
        if role not in ['client', 'admin']:
            raise ValueError("Role must be either 'client' or 'admin'.")
        return role

    #@hybrid_property
    #def password_hash(self):
    #    raise AttributeError('Password hashes cannot be viewed.')

    #@password_hash.setter
    #def password_hash(self, password):
    #    password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
    #    self._password_hash = password_hash.decode('utf-8')

    #def authenticate(self, password):
    #    return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    def __repr__(self):
        return f'<User {self.id}, {self.username}>'
    

class Model(db.Model):
    __tablename__ = 'model'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String, nullable=False)
    model_name = db.Column(db.String, nullable=False)
    year_range = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    scale_length = db.Column(db.Float, nullable=False)
    relic = db.Column(db.String, nullable=False)
    other_controls = db.Column(db.String, nullable=False)
    hardware_finish = db.Column(db.ARRAY, nullable=False)
    pickup_configuration = db.Column(db.ARRAY, nullable=False)

    # Many-to-Many Relationships (Variations)
    pickups = db.relationship('GuitarPickup', secondary='model_pickups', back_populates='model')
    bodies = db.relationship('Body', secondary='model_body', back_populates='models')
    fretboards = db.relationship('Fretboard', secondary='model_fretboard', back_populates='models')
    pickguards = db.relationship('Pickguard', secondary='model_pickguard', back_populates='models')
    switches = db.relationship('Switch', secondary='model_switch', back_populates='models')
    controls = db.relationship('Controls', secondary='model_controls', back_populates='models')

    # Many-to-One Relationships (Fixed parts of the model)
    neck_id = db.Column(db.Integer, db.ForeignKey('neck.id'), nullable=False)
    neck = db.relationship('Neck', back_populates='model')

    headstock_id = db.Column(db.Integer, db.ForeignKey('headstock.id'), nullable=False)
    headstock = db.relationship('Headstock', back_populates='model')

    nut_id = db.Column(db.Integer, db.ForeignKey('nut.id'), nullable=False)
    nut = db.relationship('Nut', back_populates='model')

    frets_id = db.Column(db.Integer, db.ForeignKey('frets.id'), nullable=False)
    frets = db.relationship('Frets', back_populates='model')

    inlays_id = db.Column(db.Integer, db.ForeignKey('inlays.id'), nullable=False)
    inlays = db.relationship('Inlays', back_populates='model')

    bridge_id = db.Column(db.Integer, db.ForeignKey('bridge.id'), nullable=False)
    bridge = db.relationship('Bridge', back_populates='model')

    saddles_id = db.Column(db.Integer, db.ForeignKey('saddles.id'), nullable=False)
    saddles = db.relationship('Saddles', back_populates='model')

    tuning_machine_id = db.Column(db.Integer, db.ForeignKey('tuning_machine.id'), nullable=False)
    tuning_machine = db.relationship('TuningMachine', back_populates='model')

    string_tree_id = db.Column(db.Integer, db.ForeignKey('string_tree.id'), nullable=False)
    string_tree = db.relationship('StringTree', back_populates='model')

    neck_plate_id = db.Column(db.Integer, db.ForeignKey('neck_plate.id'), nullable=False)
    neck_plate = db.relationship('NeckPlate', back_populates='model')

    # One-to-Many: Model → UserGuitar
    user_guitars = db.relationship('UserGuitar', back_populates='model', lazy=True)



class UserGuitar(db.Model):
    __tablename__ = 'user_guitar'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    serial_number = db.Column(db.String, nullable=False)
    serial_number_location = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String, nullable=False)
    scale_length = db.Column(db.Float, nullable=False)
    weight = db.Column(db.String, nullable=False)
    relic = db.Column(db.String, nullable=False)
    other_controls = db.Column(db.String, nullable=False)
    hardware_finish = db.Column(db.String, nullable=False)
    modified = db.Column(db.Boolean, default=False)
    modifications = db.Column(db.String, nullable=True)
    pickup_configuration = db.Column(db.String, nullable=False)

    pickups = db.relationship('GuitarPickup', secondary=user_guitar_pickups, back_populates='user_guitars')
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'), nullable=True)
    model = db.relationship('Model', back_populates='user_guitars')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', back_populates='user_guitars')

    # Relationships to components
    body_id = db.Column(db.Integer, db.ForeignKey('body.id'))
    body = db.relationship('Body', back_populates='user_guitars')

    neck_id = db.Column(db.Integer, db.ForeignKey('neck.id'))
    neck = db.relationship('Neck', back_populates='user_guitars')

    headstock_id = db.Column(db.Integer, db.ForeignKey('headstock.id'))
    headstock = db.relationship('Headstock', back_populates='user_guitars')

    fretboard_id = db.Column(db.Integer, db.ForeignKey('fretboard.id'))
    fretboard = db.relationship('Fretboard', back_populates='user_guitars')

    nut_id = db.Column(db.Integer, db.ForeignKey('nut.id'))
    nut = db.relationship('Nut', back_populates='user_guitars')

    frets_id = db.Column(db.Integer, db.ForeignKey('frets.id'))
    frets = db.relationship('Frets', back_populates='user_guitars')

    inlays_id = db.Column(db.Integer, db.ForeignKey('inlays.id'))
    inlays = db.relationship('Inlays', back_populates='user_guitars')

    bridge_id = db.Column(db.Integer, db.ForeignKey('bridge.id'))
    bridge = db.relationship('Bridge', back_populates='user_guitars')

    saddles_id = db.Column(db.Integer, db.ForeignKey('saddles.id'))
    saddles = db.relationship('Saddles', back_populates='user_guitars')

    switch_id = db.Column(db.Integer, db.ForeignKey('switch.id'))
    switch = db.relationship('Switch', back_populates='user_guitars')

    controls_id = db.Column(db.Integer, db.ForeignKey('controls.id'))
    controls = db.relationship('Controls', back_populates='user_guitars')

    other_controls = db.Column(db.String, nullable=True)

    tuning_machine_id = db.Column(db.Integer, db.ForeignKey('tuning_machine.id'))
    tuning_machine = db.relationship('TuningMachine', back_populates='user_guitars')

    string_tree_id = db.Column(db.Integer, db.ForeignKey('string_tree.id'))
    string_tree = db.relationship('StringTree', back_populates='user_guitars')

    neck_plate_id = db.Column(db.Integer, db.ForeignKey('neck_plate.id'))
    neck_plate = db.relationship('NeckPlate', back_populates='user_guitars')

    pickguard_id = db.Column(db.Integer, db.ForeignKey('pickguard.id'))
    pickguard = db.relationship('Pickguard', back_populates='user_guitars')

    images = db.relationship('Image', secondary=user_guitar_images, back_populates='user_guitars')

    def __init__(self, *args, **kwargs):
        """Set name to model name if unmodified and model exists upon creation."""
        super().__init__(*args, **kwargs)
        self.sync_name_with_model()

    def sync_name_with_model(self):
        """Update the name to the model's name if it hasn't been modified."""
        if not self.modified and self.model and self.name != self.model.model_name:
            self.name = self.model.model_name
            db.session.add(self)
            db.session.commit()

    @property
    def display_name(self):
        """Returns the model's name if unmodified, otherwise the guitar's name."""
        return self.model.model_name if not self.modified and self.model else self.name or "Unnamed Guitar"


# Guitar Attributes

# Body Model
class Body(db.Model):
    __tablename__ = 'body'

    id = db.Column(db.Integer, primary_key=True)
    wood = db.Column(db.String, nullable=False)
    contour = db.Column(db.String, nullable=False)
    routing = db.Column(db.String, nullable=False)
    finish = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=False)

    # Many-to-Many with Model
    models = db.relationship('Model', secondary='model_body', back_populates='bodies')

    # One-to-Many with UserGuitar
    user_guitars = db.relationship('UserGuitar', back_populates='body')


# Neck Model
class Neck(db.Model):
    __tablename__ = 'neck'

    id = db.Column(db.Integer, primary_key=True)
    wood = db.Column(db.String, nullable=False)
    finish = db.Column(db.String, nullable=False)
    shape = db.Column(db.String, nullable=False)
    truss_rod = db.Column(db.String, nullable=False)

    models = db.relationship('Model', back_populates='neck')
    user_guitars = db.relationship('UserGuitar', back_populates='neck')


# Headstock Model
class Headstock(db.Model):
    __tablename__ = 'headstock'

    id = db.Column(db.Integer, primary_key=True)
    shape = db.Column(db.String, nullable=False)
    decal_style = db.Column(db.String, nullable=False)
    reverse = db.Column(db.Boolean, default=False)

    models = db.relationship('Model', back_populates='headstock')
    user_guitars = db.relationship('UserGuitar', back_populates='headstock')


# Fretboard Model
class Fretboard(db.Model):
    __tablename__ = 'fretboard'

    id = db.Column(db.Integer, primary_key=True)
    material = db.Column(db.String, nullable=False)
    radius = db.Column(db.String, nullable=False)
    fret_count = db.Column(db.Integer, nullable=False)
    binding = db.Column(db.Boolean, default=False)
    scalloped = db.Column(db.Boolean, default=False)

    # Many-to-Many with Model
    models = db.relationship('Model', secondary='model_fretboard', back_populates='fretboards')

    # One-to-Many with UserGuitar
    user_guitars = db.relationship('UserGuitar', back_populates='fretboard')


# Frets Model
class Frets(db.Model):
    __tablename__ = 'frets'

    id = db.Column(db.Integer, primary_key=True)
    material = db.Column(db.String, nullable=False)
    size = db.Column(db.String, nullable=False)

    models = db.relationship('Model', back_populates='frets')
    user_guitars = db.relationship('UserGuitar', back_populates='frets')


# Nut Model
class Nut(db.Model):
    __tablename__ = 'nut'

    id = db.Column(db.Integer, primary_key=True)
    width = db.Column(db.String, nullable=False)
    material = db.Column(db.String, nullable=False)
    locking = db.Column(db.Boolean, default=False)

    models = db.relationship('Model', back_populates='nut')
    user_guitars = db.relationship('UserGuitar', back_populates='nut')


# Inlays Model
class Inlays(db.Model):
    __tablename__ = 'inlays'

    id = db.Column(db.Integer, primary_key=True)
    shape = db.Column(db.String, nullable=False)
    material = db.Column(db.String, nullable=False)
    spacing = db.Column(db.String, nullable=False)

    models = db.relationship('Model', back_populates='inlays')
    user_guitars = db.relationship('UserGuitar', back_populates='inlays')


# Bridge Model
class Bridge(db.Model):
    __tablename__ = 'bridge'

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String, nullable=False)
    screws = db.Column(db.Integer, nullable=False)
    spacing = db.Column(db.Integer, nullable=False)
    tremolo = db.Column(db.Boolean, default=True)

    models = db.relationship('Model', back_populates='bridge')
    user_guitars = db.relationship('UserGuitar', back_populates='bridge')


# Saddles Model
class Saddles(db.Model):
    __tablename__ = 'saddles'

    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String, nullable=False)
    material = db.Column(db.String, nullable=False)

    models = db.relationship('Model', back_populates='saddles')
    user_guitars = db.relationship('UserGuitar', back_populates='saddles')


# Switch Model
class Switch(db.Model):
    __tablename__ = 'switch'

    id = db.Column(db.Integer, primary_key=True)
    positions = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String, nullable=False)

    # Many-to-Many with Model
    models = db.relationship('Model', secondary='model_switch', back_populates='switches')

    # One-to-Many with UserGuitar
    user_guitars = db.relationship('UserGuitar', back_populates='switch')


# Controls Model
class Controls(db.Model):
    __tablename__ = 'controls'

    id = db.Column(db.Integer, primary_key=True)
    configuration = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=False)

    # Many-to-Many with Model
    models = db.relationship('Model', secondary='model_controls', back_populates='controls')

    # One-to-Many with UserGuitar
    user_guitars = db.relationship('UserGuitar', back_populates='controls')


# Tuning Machine Model
class TuningMachine(db.Model):
    __tablename__ = 'tuning_machine'

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String, nullable=False)
    locking = db.Column(db.Boolean, default=False)

    models = db.relationship('Model', back_populates='tuning_machine')
    user_guitars = db.relationship('UserGuitar', back_populates='tuning_machine')


# String Tree Model
class StringTree(db.Model):
    __tablename__ = 'string_tree'

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String, nullable=False)
    count = db.Column(db.Integer, nullable=False)

    models = db.relationship('Model', back_populates='string_tree')
    user_guitars = db.relationship('UserGuitar', back_populates='string_tree')


# Neck Plate Model
class NeckPlate(db.Model):
    __tablename__ = 'neck_plate'

    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String, nullable=False)
    bolts = db.Column(db.Integer, nullable=False)

    models = db.relationship('Model', back_populates='neck_plate')
    user_guitars = db.relationship('UserGuitar', back_populates='neck_plate')


# Pickguard Model
class Pickguard(db.Model):
    __tablename__ = 'pickguard'

    id = db.Column(db.Integer, primary_key=True)
    ply_count = db.Column(db.Integer, nullable=False)
    screws = db.Column(db.Integer, nullable=False)
    configuration = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=False)

    # Many-to-Many with Model
    models = db.relationship('Model', secondary='model_pickguard', back_populates='pickguards')

    # One-to-Many with UserGuitar
    user_guitars = db.relationship('UserGuitar', back_populates='pickguard')

# Image Model
class Image(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String, nullable=False)
    guitar_id = db.Column(db.Integer, db.ForeignKey('user_guitar.id'), nullable=False)

    # Relationships
    user_guitars = db.relationship('UserGuitar', secondary=user_guitar_images, back_populates='images')
