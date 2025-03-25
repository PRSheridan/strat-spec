import json
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from models import (
    User, UserGuitar, Model, Image, Body, Neck, Headstock, Fretboard, Nut, Frets, Inlays,
    Bridge, Saddles, Switch, Controls, TuningMachine, StringTree, NeckPlate, Pickguard,
    GuitarPickup
)

class ImageSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Image
        load_instance = True
        ordered = True

    id = fields.Integer()
    file_name = fields.String()
    caption = fields.String(allow_none=True)
    file_path = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        ordered = True

    id = fields.Integer()
    username = fields.String()
    email = fields.String()
    role = fields.String()
    is_active = fields.Boolean()
    last_login = fields.DateTime(allow_none=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=['owner'])))


class ModelSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Model
        load_instance = True
        ordered = True

    def get_other_controls(self, obj):
        if isinstance(obj.other_controls, str):
            try:
                return json.loads(obj.other_controls)
            except json.JSONDecodeError:
                return {}
        return obj.other_controls or {}

    def get_hardware_finish(self, obj):
        if isinstance(obj.hardware_finish, str):
            try:
                return json.loads(obj.hardware_finish)
            except json.JSONDecodeError:
                return {}
        return obj.hardware_finish or {}

    def get_pickup_configuration(self, obj):
        if isinstance(obj.pickup_configuration, str):
            try:
                return json.loads(obj.pickup_configuration)
            except json.JSONDecodeError:
                return {}
        return obj.pickup_configuration or {}

    id = fields.Integer()
    brand = fields.String()
    model_name = fields.String()
    year_range = fields.String()
    country = fields.String()
    description = fields.String(allow_none=True)
    scale_length = fields.Float()
    relic = fields.String()
    other_controls = fields.Method("get_other_controls")
    hardware_finish = fields.Method("get_hardware_finish")
    pickup_configuration = fields.Method("get_pickup_configuration")
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    pickups = fields.List(fields.Nested(lambda: GuitarPickupSchema(exclude=["models"])))
    bodies = fields.List(fields.Nested(lambda: BodySchema(exclude=["models", "user_guitars"])))
    fretboards = fields.List(fields.Nested(lambda: FretboardSchema(exclude=["models", "user_guitars"])))
    pickguards = fields.List(fields.Nested(lambda: PickguardSchema(exclude=["models", "user_guitars"])))
    switches = fields.List(fields.Nested(lambda: SwitchSchema(exclude=["models", "user_guitars"])))
    controls = fields.List(fields.Nested(lambda: ControlsSchema(exclude=["models", "user_guitars"])))

    neck = fields.Nested(lambda: NeckSchema(exclude=["models", "user_guitars"]))
    headstock = fields.Nested(lambda: HeadstockSchema(exclude=["models", "user_guitars"]))
    nut = fields.Nested(lambda: NutSchema(exclude=["models", "user_guitars"]))
    frets = fields.Nested(lambda: FretsSchema(exclude=["models", "user_guitars"]))
    inlays = fields.Nested(lambda: InlaysSchema(exclude=["models", "user_guitars"]))
    bridge = fields.Nested(lambda: BridgeSchema(exclude=["models", "user_guitars"]))
    saddles = fields.Nested(lambda: SaddlesSchema(exclude=["models", "user_guitars"]))
    tuning_machine = fields.Nested(lambda: TuningMachineSchema(exclude=["models", "user_guitars"]))
    string_tree = fields.Nested(lambda: StringTreeSchema(exclude=["models", "user_guitars"]))
    neck_plate = fields.Nested(lambda: NeckPlateSchema(exclude=["models", "user_guitars"]))

    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(only=["id", "name", "year"])))


class UserGuitarSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserGuitar
        load_instance = True
        ordered = True

    id = fields.Integer()
    brand = fields.String()
    name = fields.String()
    serial_number = fields.String()
    serial_number_location = fields.String()
    year = fields.Integer(allow_none=True)
    country = fields.String(allow_none=True)
    description = fields.String(allow_none=True)
    scale_length = fields.Float(allow_none=True)
    weight = fields.String(allow_none=True)
    relic = fields.String()
    other_controls = fields.String(allow_none=True)
    hardware_finish = fields.String(allow_none=True)  # Changed to String
    modified = fields.Boolean(allow_none=True)
    modifications = fields.String(allow_none=True)
    pickup_configuration = fields.String()  # Changed to String
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    pickups = fields.List(fields.Nested(lambda: GuitarPickupSchema(exclude=["user_guitars"])))
    owner = fields.Nested(lambda: UserSchema(exclude=["user_guitars"]))
    model = fields.Nested(lambda: ModelSchema(only=["id", "model_name", "year_range"]))
    images = fields.List(fields.Nested(lambda: ImageSchema()))

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


class GuitarPickupSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = GuitarPickup
        load_instance = True
        ordered = True

    def get_positions(self, obj):
        if isinstance(obj.position, str):
            try:
                return json.loads(obj.position)
            except json.JSONDecodeError:
                return {}
        return obj.position or {}

    id = fields.Integer()
    brand = fields.String(allow_none=True)
    model = fields.String(allow_none=True)
    position = fields.Method("get_positions")    
    type = fields.String()
    magnet = fields.String(allow_none=True)
    active = fields.Boolean(allow_none=True)  # Removed resistance, inductance, etc.
    noiseless = fields.Boolean(allow_none=True)
    cover = fields.String(allow_none=True)

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["pickups"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["pickups"])))


class BodySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Body
        load_instance = True
        ordered = True

    id = fields.Integer()
    wood = fields.String(allow_none=True)
    contour = fields.String(allow_none=True)
    routing = fields.String(allow_none=True)
    chambering = fields.Boolean(allow_none=True)
    binding = fields.Boolean()
    finish = fields.String()
    color = fields.String()

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["bodies"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["body"])))


class NeckSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Neck
        load_instance = True
        ordered = True

    id = fields.Integer()
    wood = fields.String(allow_none=True)
    finish = fields.String()
    shape = fields.String(allow_none=True)
    truss_rod = fields.String()

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["neck"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["neck"])))


class HeadstockSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Headstock
        load_instance = True
        ordered = True

    id = fields.Integer()
    shape = fields.String(allow_none=True)
    decal_style = fields.String(allow_none=True)
    reverse = fields.Boolean()

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["headstock"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["headstock"])))


class FretboardSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Fretboard
        load_instance = True
        ordered = True

    id = fields.Integer()
    material = fields.String(allow_none=True)
    radius = fields.String(allow_none=True)
    fret_count = fields.Integer()
    binding = fields.Boolean()
    scalloped = fields.Boolean()

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["fretboards"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["fretboard"])))


class NutSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Nut
        load_instance = True
        ordered = True

    id = fields.Integer()
    width = fields.String(allow_none=True)
    material = fields.String(allow_none=True)
    locking = fields.Boolean()

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["nut"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["nut"])))


class FretsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Frets
        load_instance = True
        ordered = True

    id = fields.Integer()
    material = fields.String(allow_none=True)
    size = fields.String(allow_none=True)

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["frets"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["frets"])))


class InlaysSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Inlays
        load_instance = True
        ordered = True

    id = fields.Integer()
    shape = fields.String(allow_none=True)
    material = fields.String(allow_none=True)
    spacing = fields.String(allow_none=True)  # Changed from Integer to String

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["inlays"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["inlays"])))


class BridgeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Bridge
        load_instance = True
        ordered = True

    id = fields.Integer()
    model = fields.String(allow_none=True)
    screws = fields.Integer()
    spacing = fields.Integer(allow_none=True)
    tremolo = fields.Boolean()

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["bridge"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["bridge"])))


class SaddlesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Saddles
        load_instance = True
        ordered = True

    id = fields.Integer()
    style = fields.String(allow_none=True)
    material = fields.String(allow_none=True)

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

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["switches"])))
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
    model = fields.String(allow_none=True)
    locking = fields.Boolean()

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["tuning_machine"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["tuning_machine"])))


class StringTreeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = StringTree
        load_instance = True
        ordered = True

    id = fields.Integer()
    model = fields.String(allow_none=True)
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
    details = fields.String(allow_none=True)

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["neck_plate"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["neck_plate"])))


class PickguardSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pickguard
        load_instance = True
        ordered = True

    id = fields.Integer()
    ply_count = fields.Integer(allow_none=True)
    screws = fields.Integer()
    color = fields.String()

    models = fields.List(fields.Nested(lambda: ModelSchema(exclude=["pickguards"])))
    user_guitars = fields.List(fields.Nested(lambda: UserGuitarSchema(exclude=["pickguard"])))