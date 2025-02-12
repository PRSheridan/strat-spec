#models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from config import db, bcrypt

user_guitar_images = db.Table(
    'user_guitar_images',
    db.Column('user_guitar_id', db.Integer, db.ForeignKey('user_guitar.id'), primary_key=True),
    db.Column('image_id', db.Integer, db.ForeignKey('image.id'), primary_key=True)
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
    model_name = db.Column(db.String, nullable=False)
    year_range = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)

    pickup_configuration = db.Column(db.String, nullable=False)
    other_controls = db.Column(db.String, nullable=False)
    hardware_finish = db.Column(db.String, nullable=False)
    relic = db.Column(db.String, nullable=False)

    # Relationships to components
    body_id = db.Column(db.Integer, db.ForeignKey('body.id'), nullable=False)
    body = db.relationship('Body', back_populates='models')

    neck_id = db.Column(db.Integer, db.ForeignKey('neck.id'), nullable=False)
    neck = db.relationship('Neck', back_populates='models')

    headstock_id = db.Column(db.Integer, db.ForeignKey('headstock.id'), nullable=False)
    headstock = db.relationship('Headstock', back_populates='models')

    fretboard_id = db.Column(db.Integer, db.ForeignKey('fretboard.id'), nullable=False)
    fretboard = db.relationship('Fretboard', back_populates='models')

    nut_id = db.Column(db.Integer, db.ForeignKey('nut.id'), nullable=False)
    nut = db.relationship('Nut', back_populates='models')

    frets_id = db.Column(db.Integer, db.ForeignKey('frets.id'), nullable=False)
    frets = db.relationship('Frets', back_populates='models')

    inlays_id = db.Column(db.Integer, db.ForeignKey('inlays.id'), nullable=False)
    inlays = db.relationship('Inlays', back_populates='models')

    bridge_id = db.Column(db.Integer, db.ForeignKey('bridge.id'), nullable=False)
    bridge = db.relationship('Bridge', back_populates='models')

    saddles_id = db.Column(db.Integer, db.ForeignKey('saddles.id'), nullable=False)
    saddles = db.relationship('Saddles', back_populates='models')

    switch_id = db.Column(db.Integer, db.ForeignKey('switch.id'), nullable=False)
    switch = db.relationship('Switch', back_populates='models')

    controls_id = db.Column(db.Integer, db.ForeignKey('controls.id'), nullable=False)
    controls = db.relationship('Controls', back_populates='models')

    tuning_machine_id = db.Column(db.Integer, db.ForeignKey('tuning_machine.id'), nullable=False)
    tuning_machine = db.relationship('TuningMachine', back_populates='models')

    string_tree_id = db.Column(db.Integer, db.ForeignKey('string_tree.id'), nullable=False)
    string_tree = db.relationship('StringTree', back_populates='models')

    neck_plate_id = db.Column(db.Integer, db.ForeignKey('neck_plate.id'), nullable=False)
    neck_plate = db.relationship('NeckPlate', back_populates='models')

    pickguard_id = db.Column(db.Integer, db.ForeignKey('pickguard.id'), nullable=False)
    pickguard = db.relationship('Pickguard', back_populates='models')

    # One-to-Many Relationship: Model → UserGuitar
    user_guitars = db.relationship('UserGuitar', back_populates='model', lazy=True)

class UserGuitar(db.Model):
    __tablename__ = 'user_guitar'

    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.Integer, nullable=False)
    serial_number_location = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    weight = db.Column(db.Integer, nullable=False)

    pickup_configuration = db.Column(db.String, nullable=False)
    other_controls = db.Column(db.String, nullable=False)
    hardware_finish = db.Column(db.String, nullable=False)
    
    modified = db.Column(db.Boolean, default=False)
    modifications = db.Column(db.String, nullable=True)
    relic = db.Column(db.String, nullable=False)

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

    tuning_machine_id = db.Column(db.Integer, db.ForeignKey('tuning_machine.id'))
    tuning_machine = db.relationship('TuningMachine', back_populates='user_guitars')

    string_tree_id = db.Column(db.Integer, db.ForeignKey('string_tree.id'))
    string_tree = db.relationship('StringTree', back_populates='user_guitars')

    neck_plate_id = db.Column(db.Integer, db.ForeignKey('neck_plate.id'))
    neck_plate = db.relationship('NeckPlate', back_populates='user_guitars')

    pickguard_id = db.Column(db.Integer, db.ForeignKey('pickguard.id'))
    pickguard = db.relationship('Pickguard', back_populates='user_guitars')

    # Foreign Key linking UserGuitar to a single Model
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'), nullable=True)
    model = db.relationship('Model', back_populates='user_guitars')

    # Relationship to owner
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', back_populates='user_guitars')

    images = db.relationship('Image', secondary=user_guitar_images, back_populates='user_guitars')

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

    models = db.relationship('Model', back_populates='body')
    user_guitars = db.relationship('UserGuitar', back_populates='body')

# Neck Model
class Neck(db.Model):
    __tablename__ = 'neck'

    id = db.Column(db.Integer, primary_key=True)
    wood = db.Column(db.String, nullable=False)
    finish = db.Column(db.String, nullable=False)
    shape = db.Column(db.String, nullable=False)
    scale_length = db.Column(db.String, nullable=False)
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

# (Same structure applies to all other models below)

# Fretboard Model
class Fretboard(db.Model):
    __tablename__ = 'fretboard'

    id = db.Column(db.Integer, primary_key=True)
    material = db.Column(db.String, nullable=False)
    radius = db.Column(db.String, nullable=False)

    models = db.relationship('Model', back_populates='fretboard')
    user_guitars = db.relationship('UserGuitar', back_populates='fretboard')

# Nut Model
class Nut(db.Model):
    __tablename__ = 'nut'

    id = db.Column(db.Integer, primary_key=True)
    width = db.Column(db.String, nullable=False)
    material = db.Column(db.String, nullable=False)
    locking = db.Column(db.Boolean, default=False)

    models = db.relationship('Model', back_populates='nut')
    user_guitars = db.relationship('UserGuitar', back_populates='nut')

# Frets Model
class Frets(db.Model):
    __tablename__ = 'frets'

    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, nullable=False)
    material = db.Column(db.String, nullable=False)
    size = db.Column(db.String, nullable=False)

    models = db.relationship('Model', back_populates='frets')
    user_guitars = db.relationship('UserGuitar', back_populates='frets')

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

    models = db.relationship('Model', back_populates='switch')
    user_guitars = db.relationship('UserGuitar', back_populates='switch')

# Controls Model
class Controls(db.Model):
    __tablename__ = 'controls'

    id = db.Column(db.Integer, primary_key=True)
    configuration = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=False)

    models = db.relationship('Model', back_populates='controls')
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

    models = db.relationship('Model', back_populates='pickguard')
    user_guitars = db.relationship('UserGuitar', back_populates='pickguard')

# Image Model
class Image(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String, nullable=False)
    guitar_id = db.Column(db.Integer, db.ForeignKey('user_guitar.id'), nullable=False)

    # Relationships
    user_guitars = db.relationship('UserGuitar', back_populates='images')
    user_guitars = db.relationship('UserGuitar', secondary=user_guitar_images, back_populates='images')
