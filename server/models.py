from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from config import db, bcrypt


# User Model
class User(db.Model, SerializerMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), nullable=False)
    #_password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), nullable=False)

    # Relationships
    guitars = db.relationship('Guitar', backref='owner', cascade='all, delete-orphan')

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


# Image Model
class Image(db.Model, SerializerMixin):
    __tablename__ = 'image'

    serialize_rules = ('-ticket',)  # Omit ticket to prevent recursion

    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String, nullable=False)
    guitar_id = db.Column(db.Integer, db.ForeignKey('guitar.id'), nullable=False)

    # Relationships
    guitar = db.relationship('Guitar', back_populates='images')


# Guitar Model
class Guitar(db.Model, SerializerMixin):
    __tablename__ = 'guitar'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    serial_number = db.Column(db.String, unique=True, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'), nullable=False) 

    # Relationships
    user = db.relationship('User', back_populates='guitars')
    model = db.relationship('Model', back_populates='guitars')
    images = db.relationship('Image', back_populates='guitar', cascade='all, delete-orphan')


# Model Model
class Model(db.Model, SerializerMixin):
    __tablename__ = 'model'

    serialize_rules = ('-body.model', '-neck_shape.model', '-fretboard.model', '-nut.model',
                       '-truss_rod.model', '-pickups.model', '-bridge.model', '-tuning_machine.model',
                       '-string_tree.model', '-pickguard.model', '-control_knob.model', '-switch_tip.model',
                       '-neck_plate.model')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    years = db.Column(db.String, nullable=True)

    body_id = db.Column(db.Integer, db.ForeignKey('body.id'), nullable=False)
    neck_id = db.Column(db.Integer, db.ForeignKey('neck.id'), nullable=False)
    fretboard_id = db.Column(db.Integer, db.ForeignKey('fretboard.id'), nullable=False)
    nut_id = db.Column(db.Integer, db.ForeignKey('nut.id'), nullable=False)
    truss_rod_id = db.Column(db.Integer, db.ForeignKey('truss_rod.id'), nullable=False)
    pickups_id = db.Column(db.Integer, db.ForeignKey('pickups.id'), nullable=False)
    bridge_id = db.Column(db.Integer, db.ForeignKey('bridge.id'), nullable=False)
    tuning_machine_id = db.Column(db.Integer, db.ForeignKey('tuning_machine.id'), nullable=False)
    string_tree_id = db.Column(db.Integer, db.ForeignKey('string_tree.id'), nullable=False)
    pickguard_id = db.Column(db.Integer, db.ForeignKey('pickguard.id'), nullable=False)
    control_knob_id = db.Column(db.Integer, db.ForeignKey('control_knob.id'), nullable=False)
    switch_tip_id = db.Column(db.Integer, db.ForeignKey('switch_tip.id'), nullable=False)
    neck_plate_id = db.Column(db.Integer, db.ForeignKey('neck_plate.id'), nullable=False)

    # Relationships
    body = db.relationship('Body', back_populates='models')
    neck = db.relationship('Neck', back_populates='models')
    fretboard = db.relationship('Fretboard', back_populates='models')
    nut = db.relationship('Nut', back_populates='models')
    truss_rod = db.relationship('TrussRod', back_populates='models')
    pickups = db.relationship('Pickups', back_populates='models')
    bridges = db.relationship('Bridge', back_populates='models')
    tuning_machines = db.relationship('TuningMachine', back_populates='models')
    string_trees = db.relationship('StringTree', back_populates='models')
    pickguards = db.relationship('Pickguard', back_populates='models')
    control_knobs = db.relationship('ControlKnob', back_populates='models')
    switch_tips = db.relationship('SwitchTip', back_populates='models')
    neck_plates = db.relationship('NeckPlate', back_populates='models')

    guitars = db.relationship('Guitar', back_populates='model')  # One-to-many relationship (Model -> Guitars)

#Guitar Attributes (no specific methods to search yet)

# Body Model
class Body(db.Model, SerializerMixin):
    __tablename__ = 'body'

    serialize_rules = ('-models',)

    id = db.Column(db.Integer, primary_key=True)
    body_type = db.Column(db.String, nullable=False)
    body_wood = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=False)
    finish_type = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='body')


# Neck Model
class Neck(db.Model, SerializerMixin):
    __tablename__ = 'neck'

    serialize_rules = ('-models',)

    id = db.Column(db.Integer, primary_key=True)
    shape = db.Column(db.String, nullable=False)
    wood = db.Column(db.String, nullable=False)
    finish = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='neck')


# Fretboard Model
class Fretboard(db.Model, SerializerMixin):
    __tablename__ = 'fretboard'

    id = db.Column(db.Integer, primary_key=True)
    material = db.Column(db.String, nullable=False)
    radius = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='fretboard')


# Nut Model
class Nut(db.Model, SerializerMixin):
    __tablename__ = 'nut'

    id = db.Column(db.Integer, primary_key=True)
    material = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='nut')


# TrussRod Model
class TrussRod(db.Model, SerializerMixin):
    __tablename__ = 'truss_rod'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='truss_rod')


# Pickups Model
class Pickups(db.Model, SerializerMixin):
    __tablename__ = 'pickups'

    id = db.Column(db.Integer, primary_key=True)
    pickup_configuration = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='pickups')


# Bridge Model
class Bridge(db.Model, SerializerMixin):
    __tablename__ = 'bridge'

    id = db.Column(db.Integer, primary_key=True)
    bridge_type = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='bridges')


# TuningMachine Model
class TuningMachine(db.Model, SerializerMixin):
    __tablename__ = 'tuning_machine'

    id = db.Column(db.Integer, primary_key=True)
    machine_type = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='tuning_machines')


# StringTree Model
class StringTree(db.Model, SerializerMixin):
    __tablename__ = 'string_tree'

    id = db.Column(db.Integer, primary_key=True)
    tree_type = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='string_trees')


# Pickguard Model
class Pickguard(db.Model, SerializerMixin):
    __tablename__ = 'pickguard'

    id = db.Column(db.Integer, primary_key=True)
    layers = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='pickguards')


# ControlKnob Model
class ControlKnob(db.Model, SerializerMixin):
    __tablename__ = 'control_knob'

    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='control_knobs')


# SwitchTip Model
class SwitchTip(db.Model, SerializerMixin):
    __tablename__ = 'switch_tip'

    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='switch_tips')


# NeckPlate Model
class NeckPlate(db.Model, SerializerMixin):
    __tablename__ = 'neck_plate'

    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='neck_plates')