from sqlalchemy.orm import joinedload
from config import db
from models import Model, Body, Neck, Fretboard, Nut, TrussRod, Pickups, Bridge, TuningMachine, StringTree, Pickguard, ControlKnob, SwitchTip, NeckPlate

def get_models_by_attribute(attribute, column, value):
    if attribute not in ['body', 'neck', 'fretboard', 'nut', 'truss_rod', 'pickups', 'bridge', 'tuning_machine', 'string_tree', 'pickguard', 'control_knob', 'switch_tip', 'neck_plate']:
        raise ValueError("Invalid attribute name")

    attribute_class = globals()[attribute.capitalize()]
    return db.session.query(Model).join(attribute_class).filter(getattr(attribute_class, column) == value)

