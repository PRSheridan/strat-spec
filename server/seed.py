import json
from random import choice, randint, sample, uniform
from faker import Faker
from datetime import datetime, timedelta

from app import app
from models import (
    db, User, UserGuitar, Model, Body, Neck, Headstock, Fretboard, Nut, Frets, Inlays,
    Bridge, Saddles, Switch, Controls, TuningMachine, StringTree, NeckPlate, Pickguard, GuitarPickup
)

fake = Faker()

def seed_users():
    users = []
    admin = User(username="admin", email="admin@stratregistry.com", role="admin", is_active=True, last_login=datetime.now())
    admin.password_hash = "adminpassword"
    users.append(admin)
    for _ in range(9):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            role="client",
            is_active=True,
            last_login=fake.date_time_between(start_date="-30d", end_date="now")
        )
        user.password_hash = "password123"
        users.append(user)
    db.session.bulk_save_objects(users)
    db.session.commit()

def seed_components():
    bodies = [Body(wood=choice(["Alder", "Ash", "Basswood", "Mahogany"]), contour=choice(["Shallow", "Deep"]), routing=choice(["SSS", "HSS", "HH"]), finish=choice(["Nitrocellulose", "Polyurethane"]), color=choice(["Sunburst", "Black", "Olympic White"])) for _ in range(5)]
    necks = [Neck(wood=choice(["Maple", "Mahogany", "Roasted Maple"]), finish=choice(["Gloss", "Satin"]), shape=choice(["C", "V", "U"])) for _ in range(5)]
    headstocks = [Headstock(shape=choice(["Standard", "Large"]), decal_style=choice(["Vintage", "Modern"]), reverse=choice([True, False])) for _ in range(3)]
    fretboards = [Fretboard(material=choice(["Maple", "Rosewood"]), radius=choice(["7.25", "9.5", "12"]), fret_count=choice([21, 22, 24]), binding=choice([True, False]), scalloped=choice([True, False])) for _ in range(5)]
    nuts = [Nut(width=choice(["1.650", "1.685"]), material=choice(["Bone", "Plastic", "Graphite"]), locking=choice([True, False])) for _ in range(3)]
    frets = [Frets(material=choice(["Nickel Silver", "Stainless Steel"]), size=choice(["Vintage", "Jumbo"])) for _ in range(3)]
    inlays = [Inlays(shape=choice(["Dot", "Block"]), material=choice(["Pearloid", "Abalone"])) for _ in range(3)]
    bridges = [Bridge(model=choice(["Vintage", "2-Point Tremolo"]), screws=choice([2, 6]), spacing=choice([52, 54]), tremolo=choice([True, False])) for _ in range(3)]
    saddles = [Saddles(style=choice(["Vintage", "Modern"]), material=choice(["Steel", "Brass"])) for _ in range(3)]
    switches = [Switch(positions=choice([3, 5]), color=choice(["White", "Black"])) for _ in range(3)]
    controls = [Controls(configuration=choice(["1 Volume, 2 Tone"]), color=choice(["White", "Black"])) for _ in range(3)]
    tuning_machines = [TuningMachine(model=choice(["Vintage", "Locking"]), locking=choice([True, False])) for _ in range(3)]
    string_trees = [StringTree(model=choice(["Butterfly", "Disc"]), count=randint(0, 2)) for _ in range(3)]
    neck_plates = [NeckPlate(style=choice(["Vintage", "Contour"]), bolts=choice([3, 4])) for _ in range(3)]
    pickguards = [Pickguard(ply_count=choice([1, 3]), screws=choice([8, 11]), color=choice(["White", "Black", "Tortoise"])) for _ in range(3)]
    pickups = [GuitarPickup(brand=choice(["Fender", "Seymour Duncan"]), model=choice(["Custom '69", "Texas Special"]), position=[choice(["Neck", "Bridge"])], type=choice(["Single-coil", "Humbucker"])) for _ in range(5)]
    db.session.bulk_save_objects(bodies + necks + headstocks + fretboards + nuts + frets + inlays + bridges + saddles + switches + controls + tuning_machines + string_trees + neck_plates + pickguards + pickups)
    db.session.commit()

def seed_models():
    components = {k: v.query.all() for k, v in {
        "bodies": Body, "necks": Neck, "headstocks": Headstock, "fretboards": Fretboard,
        "nuts": Nut, "frets": Frets, "inlays": Inlays, "bridges": Bridge, "saddles": Saddles,
        "switches": Switch, "controls": Controls, "tuning_machines": TuningMachine, "string_trees": StringTree,
        "neck_plates": NeckPlate, "pickguards": Pickguard
    }.items()}
    models = [Model(brand="Fender", model_name=f"Model {i}", year_range="1990-present", country="USA", **{k: sample(v, randint(1, 3)) for k, v in components.items()}) for i in range(5)]
    db.session.bulk_save_objects(models)
    db.session.commit()

def seed_user_guitars():
    users = User.query.all()
    models = Model.query.all()
    user_guitars = [UserGuitar(brand="Fender", name=f"Guitar {i}", serial_number=f"SN{randint(10000,99999)}", model=choice(models) if randint(1, 10) <= 5 else None, owner=choice(users), body=choice(Body.query.all()), neck=choice(Neck.query.all()), fretboard=choice(Fretboard.query.all()), bridge=choice(Bridge.query.all())) for i in range(20)]
    db.session.bulk_save_objects(user_guitars)
    db.session.commit()

def seed_database():
    seed_users()
    seed_components()
    seed_models()
    seed_user_guitars()
    print("Database seeding complete!")

if __name__ == "__main__":
    with app.app_context():
        seed_database()
