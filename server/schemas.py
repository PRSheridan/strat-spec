from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from models import (
    User, Guitar, Model, Image, Body, Neck, Fretboard, Nut, TrussRod, Pickups, 
    Bridge, TuningMachine, StringTree, Pickguard, ControlKnob, SwitchTip, NeckPlate
)

# User Schema
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        ordered = True

    id = fields.Integer()
    username = fields.String()
    email = fields.String()
    role = fields.String()
    guitars = fields.List(fields.Nested(lambda: GuitarSchema(exclude=['user'])))

# Guitar Schema
class GuitarSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Guitar
        load_instance = True
        ordered = True

    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    serial_number = fields.String()
    user = fields.Nested(lambda: UserSchema(exclude=["guitars"]))
    model = fields.Nested(lambda: ModelSchema(exclude=["guitars"]))
    images = fields.List(fields.Nested(lambda: ImageSchema()))

# Model Schema
class ModelSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Model
        load_instance = True
        ordered = True

    id = fields.Integer()
    name = fields.String()
    years = fields.String()
    body = fields.Nested(lambda: BodySchema(exclude=["models"]))
    neck = fields.Nested(lambda: NeckSchema(exclude=["models"]))
    fretboard = fields.Nested(lambda: FretboardSchema(exclude=["models"]))
    nut = fields.Nested(lambda: NutSchema(exclude=["models"]))
    truss_rod = fields.Nested(lambda: TrussRodSchema(exclude=["models"]))
    pickups = fields.Nested(lambda: PickupsSchema(exclude=["models"]))
    bridge = fields.Nested(lambda: BridgeSchema(exclude=["models"]))
    tuning_machine = fields.Nested(lambda: TuningMachineSchema(exclude=["models"]))
    string_tree = fields.Nested(lambda: StringTreeSchema(exclude=["models"]))
    pickguard = fields.Nested(lambda: PickguardSchema(exclude=["models"]))
    control_knob = fields.Nested(lambda: ControlKnobSchema(exclude=["models"]))
    switch_tip = fields.Nested(lambda: SwitchTipSchema(exclude=["models"]))
    neck_plate = fields.Nested(lambda: NeckPlateSchema(exclude=["models"]))
    guitars = fields.List(fields.Nested(lambda: GuitarSchema(exclude=["model"])))

# Image Schema
class ImageSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Image
        load_instance = True
        ordered = True

    id = fields.Integer()
    file_path = fields.String()
    guitar = fields.Nested(lambda: GuitarSchema(exclude=["images"]))

# Component Schemas
class BodySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Body
        load_instance = True
        ordered = True

    id = fields.Integer()
    body_type = fields.String()
    body_wood = fields.String()
    color = fields.String()
    finish_type = fields.String()
    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["body"])))

class NeckSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Neck
        load_instance = True
        ordered = True

    id = fields.Integer()
    shape = fields.String()
    wood = fields.String()
    finish = fields.String()
    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["neck"])))

class FretboardSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Fretboard
        load_instance = True
        ordered = True

    id = fields.Integer()
    material = fields.String()
    radius = fields.String()
    frets = fields.String()
    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["fretboard"])))

class NutSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Nut
        load_instance = True
        ordered = True

    id = fields.Integer()
    material = fields.String()
    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["nut"])))

class TrussRodSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TrussRod
        load_instance = True
        ordered = True

    id = fields.Integer()
    type = fields.String()
    location = fields.String()
    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["truss_rod"])))

class PickupsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pickups
        load_instance = True
        ordered = True

    id = fields.Integer()
    pickup_configuration = fields.String()
    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["pickups"])))

class BridgeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Bridge
        load_instance = True
        ordered = True

    id = fields.Integer()
    bridge_type = fields.String()
    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["bridge"])))

class TuningMachineSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TuningMachine
        load_instance = True
        ordered = True

    id = fields.Integer()
    machine_type = fields.String()
    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["tuning_machine"])))

class StringTreeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = StringTree
        load_instance = True
        ordered = True

    id = fields.Integer()
    tree_type = fields.String()
    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["string_tree"])))

class PickguardSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pickguard
        load_instance = True
        ordered = True

    id = fields.Integer()
    layers = fields.String()
    color = fields.String()
    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["pickguard"])))

class ControlKnobSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ControlKnob
        load_instance = True
        ordered = True

    id = fields.Integer()
    style = fields.String()
    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["control_knob"])))

class SwitchTipSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SwitchTip
        load_instance = True
        ordered = True

    id = fields.Integer()
    style = fields.String()
    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["switch_tip"])))

class NeckPlateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = NeckPlate
        load_instance = True
        ordered = True

    id = fields.Integer()
    style = fields.String()
    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["neck_plate"])))

