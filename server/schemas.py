from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from models import (
    User, UserGuitar, Model, Image, Body, Neck, Headstock, Fretboard, Nut, Frets, Inlays,
    Bridge, Saddles, Switch, Controls, TuningMachine, StringTree, NeckPlate, Pickguard
)

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        ordered = True

    id = fields.Integer()
    username = fields.String()
    email = fields.String()
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=['owner'])))

class UserGuitarSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserGuitar
        load_instance = True
        ordered = True

    id = fields.Integer()
    name = fields.String()
    serial_number = fields.Integer()
    serial_number_location = fields.String()
    year = fields.String()
    country = fields.String()
    weight = fields.Integer()
    pickup_configuration = fields.String()
    other_controls = fields.String()
    hardware_finish = fields.String()
    modified = fields.Boolean()
    modifications = fields.String()
    relic = fields.String()

    owner = fields.Nested(lambda: UserSchema(exclude=["user_guitars"]))
    model = fields.Nested(lambda: ModelSchema(exclude=["user_guitars"]))

    body = fields.Nested(lambda: BodySchema(exclude=["models", "user_guitars"]))
    neck = fields.Nested(lambda: NeckSchema(exclude=["models", "user_guitars"]))
    headstock = fields.Nested(lambda: HeadstockSchema(exclude=["models", "user_guitars"]))
    fretboard = fields.Nested(lambda: FretboardSchema(exclude=["models", "user_guitars"]))
    nut = fields.Nested(lambda: NutSchema(exclude=["models", "user_guitars"]))
    frets = fields.Nested(lambda: FretsSchema(exclude=["models", "user_guitars"]))
    inlays = fields.Nested(lambda: InlaysSchema(exclude=["models", "user_guitars"]))
    bridge = fields.Nested(lambda: BridgeSchema(exclude=["models", "user_guitars"]))
    saddles = fields.Nested(lambda: SaddlesSchema(exclude=["models", "user_guitars"]))
    switch = fields.Nested(lambda: SwitchSchema(exclude=["models", "user_guitars"]))
    controls = fields.Nested(lambda: ControlsSchema(exclude=["models", "user_guitars"]))
    tuning_machine = fields.Nested(lambda: TuningMachineSchema(exclude=["models", "user_guitars"]))
    string_tree = fields.Nested(lambda: StringTreeSchema(exclude=["models", "user_guitars"]))
    neck_plate = fields.Nested(lambda: NeckPlateSchema(exclude=["models", "user_guitars"]))
    pickguard = fields.Nested(lambda: PickguardSchema(exclude=["models", "user_guitars"]))

class ModelSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Model
        load_instance = True
        ordered = True

    id = fields.Integer()
    model_name = fields.String()
    year_range = fields.String()
    country = fields.String()
    pickup_configuration = fields.String()
    other_controls = fields.String()
    hardware_finish = fields.String()
    relic = fields.String()

    body = fields.Nested(lambda: BodySchema(exclude=["models", "user_guitars"]))
    neck = fields.Nested(lambda: NeckSchema(exclude=["models", "user_guitars"]))
    headstock = fields.Nested(lambda: HeadstockSchema(exclude=["models", "user_guitars"]))
    fretboard = fields.Nested(lambda: FretboardSchema(exclude=["models", "user_guitars"]))
    nut = fields.Nested(lambda: NutSchema(exclude=["models", "user_guitars"]))
    frets = fields.Nested(lambda: FretsSchema(exclude=["models", "user_guitars"]))
    inlays = fields.Nested(lambda: InlaysSchema(exclude=["models", "user_guitars"]))
    bridge = fields.Nested(lambda: BridgeSchema(exclude=["models", "user_guitars"]))
    saddles = fields.Nested(lambda: SaddlesSchema(exclude=["models", "user_guitars"]))
    switch = fields.Nested(lambda: SwitchSchema(exclude=["models", "user_guitars"]))
    controls = fields.Nested(lambda: ControlsSchema(exclude=["models", "user_guitars"]))
    tuning_machine = fields.Nested(lambda: TuningMachineSchema(exclude=["models", "user_guitars"]))
    string_tree = fields.Nested(lambda: StringTreeSchema(exclude=["models", "user_guitars"]))
    neck_plate = fields.Nested(lambda: NeckPlateSchema(exclude=["models", "user_guitars"]))
    pickguard = fields.Nested(lambda: PickguardSchema(exclude=["models", "user_guitars"]))

    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["model"])))


class ImageSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Image
        load_instance = True
        ordered = True

    id = fields.Integer()
    file_path = fields.String()
    guitar = fields.Nested(lambda: UserGuitarSchema(exclude=["images"]))

class BodySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Body
        load_instance = True
        ordered = True

    id = fields.Integer()
    wood = fields.String()
    contour = fields.String()
    routing = fields.String()
    finish = fields.String()
    color = fields.String()

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["body"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["body"])))


class NeckSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Neck
        load_instance = True
        ordered = True

    id = fields.Integer()
    wood = fields.String()
    finish = fields.String()
    shape = fields.String()
    scale_length = fields.String()
    truss_rod = fields.String()

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["neck"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["neck"])))


class HeadstockSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Headstock
        load_instance = True
        ordered = True

    id = fields.Integer()
    shape = fields.String()
    decal_style = fields.String()
    reverse = fields.Boolean()

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["headstock"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["headstock"])))


class FretboardSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Fretboard
        load_instance = True
        ordered = True

    id = fields.Integer()
    material = fields.String()
    radius = fields.String()

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["fretboard"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["fretboard"])))


class NutSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Nut
        load_instance = True
        ordered = True

    id = fields.Integer()
    width = fields.String()
    material = fields.String()
    locking = fields.Boolean()

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["nut"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["nut"])))


class FretsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Frets
        load_instance = True
        ordered = True

    id = fields.Integer()
    count = fields.Integer()
    material = fields.String()
    size = fields.String()

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["frets"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["frets"])))


class InlaysSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Inlays
        load_instance = True
        ordered = True

    id = fields.Integer()
    shape = fields.String()
    material = fields.String()
    spacing = fields.String()

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["inlays"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["inlays"])))


class BridgeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Bridge
        load_instance = True
        ordered = True

    id = fields.Integer()
    model = fields.String()
    screws = fields.Integer()
    spacing = fields.String()

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["bridge"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["bridge"])))


class SaddlesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Saddles
        load_instance = True
        ordered = True

    id = fields.Integer()
    style = fields.String()
    material = fields.String()

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["saddles"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["saddles"])))


class SwitchSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Switch
        load_instance = True
        ordered = True

    id = fields.Integer()
    positions = fields.Integer()
    color = fields.String()

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["switch"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["switch"])))


class ControlsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Controls
        load_instance = True
        ordered = True

    id = fields.Integer()
    configuration = fields.String()
    color = fields.String()

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["controls"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["controls"])))


class TuningMachineSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TuningMachine
        load_instance = True
        ordered = True

    id = fields.Integer()
    model = fields.String()
    locking = fields.Boolean()

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["tuning_machine"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["tuning_machine"])))


class StringTreeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = StringTree
        load_instance = True
        ordered = True

    id = fields.Integer()
    model = fields.String()
    count = fields.Integer()

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["string_tree"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["string_tree"])))


class NeckPlateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = NeckPlate
        load_instance = True
        ordered = True

    id = fields.Integer()
    style = fields.String()
    bolts = fields.Integer()

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["neck_plate"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["neck_plate"])))


class PickguardSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pickguard
        load_instance = True
        ordered = True

    id = fields.Integer()
    ply_count = fields.Integer()
    screws = fields.Integer()
    configuration = fields.String()
    color = fields.String()

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["pickguard"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["pickguard"])))




