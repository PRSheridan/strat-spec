# Guitar Model
import db, SerializerMixin

class Guitar(db.Model, SerializerMixin):
    __tablename__ = 'guitars'

    serialize_rules = (
        '-model',  # Omit model to prevent recursion
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    serial_number = db.Column(db.String, nullable=True)
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'), nullable=False)

    # Relationships
    model = db.relationship('Model', back_populates='guitars')


# Model
class Model(db.Model, SerializerMixin):
    __tablename__ = 'models'

    serialize_rules = (
        '-guitars',  # Omit guitars to prevent recursion
    )

    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String, nullable=False)
    year_range = db.Column(db.String, nullable=True)
    body_id = db.Column(db.Integer, db.ForeignKey('bodies.id'), nullable=False)
    neck_shape_id = db.Column(db.Integer, db.ForeignKey('neck_shapes.id'), nullable=False)
    neck_wood = db.Column(db.String, nullable=False)
    neck_finish_id = db.Column(db.Integer, db.ForeignKey('finishes.id'), nullable=False)
    fretboard_material_id = db.Column(db.Integer, db.ForeignKey('fretboard_materials.id'), nullable=False)
    fretboard_radius = db.Column(db.Float, nullable=False)
    fret_size = db.Column(db.String, nullable=False)
    number_of_frets = db.Column(db.Integer, nullable=False)
    nut_material_id = db.Column(db.Integer, db.ForeignKey('nut_materials.id'), nullable=False)
    nut_width = db.Column(db.Float, nullable=False)
    truss_rod_type_id = db.Column(db.Integer, db.ForeignKey('truss_rods.id'), nullable=False)
    truss_rod_location = db.Column(db.String, nullable=False)
    pickup_configuration_id = db.Column(db.Integer, db.ForeignKey('configurations.id'), nullable=False)
    pickup_1_id = db.Column(db.Integer, db.ForeignKey('pickups.id'), nullable=False)
    pickup_2_id = db.Column(db.Integer, db.ForeignKey('pickups.id'), nullable=False)
    pickup_3_id = db.Column(db.Integer, db.ForeignKey('pickups.id'), nullable=True)
    bridge_type_id = db.Column(db.Integer, db.ForeignKey('bridges.id'), nullable=False)
    saddle_type_id = db.Column(db.Integer, db.ForeignKey('saddles.id'), nullable=False)
    tuning_machine_type_id = db.Column(db.Integer, db.ForeignKey('tuning_machines.id'), nullable=False)
    string_tree_type_id = db.Column(db.Integer, db.ForeignKey('string_trees.id'), nullable=False)
    pickguard_style_id = db.Column(db.Integer, db.ForeignKey('pickguards.id'), nullable=False)
    control_knob_style_id = db.Column(db.Integer, db.ForeignKey('control_knobs.id'), nullable=False)
    switch_tip_style_id = db.Column(db.Integer, db.ForeignKey('switch_tips.id'), nullable=False)
    neck_plate_design_id = db.Column(db.Integer, db.ForeignKey('neck_plates.id'), nullable=False)
    finish_id = db.Column(db.Integer, db.ForeignKey('finishes.id'), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('colors.id'), nullable=False)

    # Relationships
    body = db.relationship('Body', back_populates='models')
    neck_shape = db.relationship('NeckShape', back_populates='models')
    finish = db.relationship('Finish', back_populates='models')
    color = db.relationship('Color', back_populates='models')
    pickups = db.relationship('Pickup', back_populates='model')
    configurations = db.relationship('Configuration', back_populates='model')
    bridges = db.relationship('Bridge', back_populates='models')
    saddles = db.relationship('Saddle', back_populates='models')
    tuning_machines = db.relationship('TuningMachine', back_populates='models')
    string_trees = db.relationship('StringTree', back_populates='models')
    pickguards = db.relationship('Pickguard', back_populates='models')
    control_knobs = db.relationship('ControlKnob', back_populates='models')
    switch_tips = db.relationship('SwitchTip', back_populates='models')
    neck_plates = db.relationship('NeckPlate', back_populates='models')


# Body
class Body(db.Model, SerializerMixin):
    __tablename__ = 'bodies'

    serialize_rules = (
        '-models',  # Omit models to prevent recursion
    )

    id = db.Column(db.Integer, primary_key=True)
    body_type = db.Column(db.String, nullable=False)
    body_wood = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='body')


# NeckShape
class NeckShape(db.Model, SerializerMixin):
    __tablename__ = 'neck_shapes'

    serialize_rules = (
        '-models',  # Omit models to prevent recursion
    )

    id = db.Column(db.Integer, primary_key=True)
    shape_name = db.Column(db.String, nullable=False)
    neck_wood = db.Column(db.String, nullable=False)
    neck_finish_id = db.Column(db.Integer, db.ForeignKey('finishes.id'), nullable=False)

    # Relationships
    finish = db.relationship('Finish', back_populates='neck_shapes')
    models = db.relationship('Model', back_populates='neck_shape')


# FretboardMaterial
class FretboardMaterial(db.Model, SerializerMixin):
    __tablename__ = 'fretboard_materials'

    id = db.Column(db.Integer, primary_key=True)
    material_name = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='fretboard_material')


# NutMaterial
class NutMaterial(db.Model, SerializerMixin):
    __tablename__ = 'nut_materials'

    id = db.Column(db.Integer, primary_key=True)
    material_name = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='nut_material')


# TrussRod
class TrussRod(db.Model, SerializerMixin):
    __tablename__ = 'truss_rods'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='truss_rod')


# Pickup
class Pickup(db.Model, SerializerMixin):
    __tablename__ = 'pickups'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='pickups')


# Configuration
class Configuration(db.Model, SerializerMixin):
    __tablename__ = 'configurations'

    id = db.Column(db.Integer, primary_key=True)
    pickup_configuration = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='configurations')


# Bridge
class Bridge(db.Model, SerializerMixin):
    __tablename__ = 'bridges'

    id = db.Column(db.Integer, primary_key=True)
    bridge_type = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='bridges')


# Saddle
class Saddle(db.Model, SerializerMixin):
    __tablename__ = 'saddles'

    id = db.Column(db.Integer, primary_key=True)
    saddle_type = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='saddles')


# TuningMachine
class TuningMachine(db.Model, SerializerMixin):
    __tablename__ = 'tuning_machines'

    id = db.Column(db.Integer, primary_key=True)
    machine_type = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='tuning_machines')


# StringTree
class StringTree(db.Model, SerializerMixin):
    __tablename__ = 'string_trees'

    id = db.Column(db.Integer, primary_key=True)
    tree_type = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='string_trees')


# Pickguard
class Pickguard(db.Model, SerializerMixin):
    __tablename__ = 'pickguards'

    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='pickguards')


# ControlKnob
class ControlKnob(db.Model, SerializerMixin):
    __tablename__ = 'control_knobs'

    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='control_knobs')


# SwitchTip
class SwitchTip(db.Model, SerializerMixin):
    __tablename__ = 'switch_tips'

    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='switch_tips')


# NeckPlate
class NeckPlate(db.Model, SerializerMixin):
    __tablename__ = 'neck_plates'

    id = db.Column(db.Integer, primary_key=True)
    design = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='neck_plates')


# Finish
class Finish(db.Model, SerializerMixin):
    __tablename__ = 'finishes'

    id = db.Column(db.Integer, primary_key=True)
    finish_type = db.Column(db.String, nullable=False)

