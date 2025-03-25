import json
from random import choice, randint, sample, uniform
from faker import Faker
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

from flask_migrate import upgrade
from flask_migrate import init, migrate
import os

from app import app
from models import (
    db, User, GuitarPickup, Body, Neck, Headstock, Fretboard, Frets, Nut,
    Inlays, Bridge, Saddles, Switch, Controls, TuningMachine, StringTree, 
    NeckPlate, Pickguard, Model, UserGuitar
)

fake = Faker()

user_guitar_amt = 40
user_amt = 10

def create_users(num_users=user_amt):
    """Generate users with all required attributes."""
    users = []
    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        password = generate_password_hash("password")  # Default password for all users
        role = choice(["client", "admin"]) if randint(0, 9) == 0 else "client"  # ~10% chance of admin
        is_active = choice([True, False])  # Randomly assign active/inactive status
        last_login = fake.date_time_between(start_date="-1y", end_date="now") if randint(0, 1) else None
        created_at = fake.date_time_between(start_date="-2y", end_date="-1y")
        updated_at = fake.date_time_between(start_date=created_at, end_date="now")

        user = User(
            username=username,
            email=email,
            _password_hash=password,
            role=role,
            is_active=is_active,
            last_login=last_login,
            created_at=created_at,
            updated_at=updated_at
        )
        users.append(user)

    db.session.bulk_save_objects(users)
    db.session.commit()
    return users

def create_guitar_pickups(num_pickups=15):
    """Generate guitar pickups with valid attributes and relationships."""
    valid_types = [
        'Single-coil', 'Humbucker', 'Hot Rails', 'Noiseless', 'Lace Sensor',
        'P90', 'Mini-humbucker', 'Active', 'Lipstick', 'Rail', 'Vintage', 
        'Texas Special', 'Custom Shop', 'Other'
    ]
    
    valid_magnets = ['Alnico II', 'Alnico III', 'Alnico IV', 'Alnico V', 
                     'Ceramic', 'Neodymium', 'Samarium Cobalt', 'Other', None]

    valid_covers = ['None', 'Chrome', 'Nickel', 'Gold', 'Black', 'Cream', 'Zebra', 'Other', None]

    valid_pickup_models = ["Texas Special", "Vintage Noiseless", "Fat 50s", "Lace Sensor Gold"]

    pickups = []
    for _ in range(num_pickups):
        pickup = GuitarPickup(
            brand=fake.company() if randint(0, 1) else None,
            model=choice(valid_pickup_models) if randint(0, 1) else None,
            position=sample(["Neck", "Middle", "Bridge"], randint(1, 3)),
            type=choice(valid_types),
            magnet=choice(valid_magnets),
            active=choice([True, False, None]),
            noiseless=choice([True, False]),
            cover=choice(valid_covers)
        )
        pickups.append(pickup)

    db.session.bulk_save_objects(pickups)
    db.session.commit()
    return pickups

def create_bodies(num_bodies=15):
    """Generate guitar bodies with valid attributes and relationships."""
    valid_woods = ['Alder', 'Ash', 'Basswood', 'Mahogany', 'Poplar', 'Pine', 
                   'Maple', 'Korina', 'Walnut', 'Paulownia', 'Other', None]

    valid_contours = ['Shallow', 'Deep', None]

    valid_routings = ['Standard', 'HH', 'HSH', 'HSS', 'SSS', 'HS', 'S', 'H', 'Other', None]

    valid_finishes = ['Nitrocellulose', 'Polyurethane', 'Other']

    colors = ['Sunburst', 'Black', 'White', 'Red', 'Blue', 'Green', 'Natural', 'Gold', 'Silver', 'Other']

    bodies = []
    for _ in range(num_bodies):
        body = Body(
            wood=choice(valid_woods),
            contour=choice(valid_contours),
            routing=choice(valid_routings),
            chambering=choice([True, False, None]),
            binding=choice([True, False]),
            finish=choice(valid_finishes),
            color=choice(colors)
        )
        bodies.append(body)

    db.session.bulk_save_objects(bodies)
    db.session.commit()
    return bodies

def create_necks(num_necks=15):
    """Generate guitar necks with valid attributes and relationships."""
    valid_woods = ['Maple', 'Mahogany', 'Roasted Maple', 'Flame Maple', 'Birdseye Maple', 'Other', None]

    valid_finishes = ['Gloss', 'Satin', 'Natural']

    valid_truss_rods = ['Modern', 'Vintage']

    necks = []
    for _ in range(num_necks):
        neck = Neck(
            wood=choice(valid_woods),
            finish=choice(valid_finishes),
            shape=fake.word().capitalize() if randint(0, 1) else None,
            truss_rod=choice(valid_truss_rods)
        )
        necks.append(neck)

    db.session.bulk_save_objects(necks)
    db.session.commit()
    return necks

def create_headstocks(num_headstocks=10):
    """Generate headstocks with valid attributes and relationships."""
    valid_decal_styles = ['Vintage', 'Modern', 'Spaghetti Logo', 'CBS Logo', 'Block', 'None', 'Other', None]

    headstocks = []
    for _ in range(num_headstocks):
        headstock = Headstock(
            shape=fake.word().capitalize() if randint(0, 1) else None,
            decal_style=choice(valid_decal_styles),
            reverse=choice([True, False])
        )
        headstocks.append(headstock)

    db.session.bulk_save_objects(headstocks)
    db.session.commit()
    return headstocks

def create_fretboards(num_fretboards=10):
    """Generate fretboards with valid attributes and relationships."""
    valid_materials = ['Maple', 'Rosewood', 'Ebony', 'Pau Ferro', 'Richlite', 'Walnut', 'Laurel', 'Wenge', 'Other']
    
    fretboards = []
    for _ in range(num_fretboards):
        radius_value = round(uniform(5.0, 25.0), 1) if randint(0, 1) else "Compound"
        fret_count = randint(19, 36)

        fretboard = Fretboard(
            material=choice(valid_materials),
            radius=str(radius_value) if isinstance(radius_value, float) else radius_value,
            fret_count=fret_count,
            binding=choice([True, False]),
            scalloped=choice([True, False])
        )
        fretboards.append(fretboard)

    db.session.bulk_save_objects(fretboards)
    db.session.commit()
    return fretboards

def create_frets(num_frets=10):
    """Generate frets with valid attributes and relationships."""
    valid_materials = ['Nickel Silver', 'Stainless Steel', 'Jescar EVO Gold', 'Vintage', 'Other', None]
    valid_sizes = ['Vintage', 'Medium', 'Jumbo', 'Medium Jumbo', 'Narrow Tall', 'Other', None]

    frets = []
    for _ in range(num_frets):
        fret = Frets(
            material=choice(valid_materials),
            size=choice(valid_sizes)
        )
        frets.append(fret)

    db.session.bulk_save_objects(frets)
    db.session.commit()
    return frets

def create_nuts(num_nuts=10):
    """Generate nuts with valid attributes and relationships."""
    valid_materials = ['Bone', 'Plastic', 'Graphite', 'Corian', 'Brass', 'Tusq', 'Other', None]

    nuts = []
    for _ in range(num_nuts):
        width_value = round(uniform(1.5, 2.0), 2) if randint(0, 1) else None
        nut = Nut(
            width=str(width_value) if width_value else None,
            material=choice(valid_materials),
            locking=choice([True, False])
        )
        nuts.append(nut)

    db.session.bulk_save_objects(nuts)
    db.session.commit()
    return nuts

def create_inlays(num_inlays=10):
    """Generate inlays with valid attributes and relationships."""
    valid_shapes = ['Dot', 'Block', 'Shark Fin', 'Trapezoid', 'Bird', 'None', 'Other', None]
    valid_materials = ['Pearloid', 'Mother of Pearl', 'Abalone', 'Acrylic', 'Stone', 'Plastic', 'None', 'Other', None]
    valid_spacings = ['Modern', 'Vintage', None]

    inlays = []
    for _ in range(num_inlays):
        shape = choice(valid_shapes)
        spacing = choice(valid_spacings) if shape == 'Dot' else None
        inlay = Inlays(
            shape=shape,
            material=choice(valid_materials),
            spacing=spacing
        )
        inlays.append(inlay)

    db.session.bulk_save_objects(inlays)
    db.session.commit()
    return inlays

def create_bridges(num_bridges=10):
    """Generate bridges with valid attributes and relationships."""
    bridges = []
    for _ in range(num_bridges):
        bridge = Bridge(
            model=fake.word().capitalize() if randint(0, 1) else None,  # 50% chance of having a model
            screws=randint(2, 6),
            spacing=randint(50, 56) if randint(0, 1) else None,  # Random spacing within typical range
            tremolo=choice([True, False])  # Required boolean
        )
        bridges.append(bridge)

    db.session.bulk_save_objects(bridges)
    db.session.commit()
    return bridges

def create_saddles(num_saddles=10):
    """Generate saddles with valid attributes and relationships."""
    valid_styles = ['Vintage', 'Modern', 'Block', 'Roller', 'Compensated', 'Graphtech', 'Other']
    valid_materials = ['Steel', 'Brass', 'Graphite', 'Titanium', 'Chrome', 'Nickel', 'Other', None]

    saddles = []
    for _ in range(num_saddles):
        saddle = Saddles(
            style=choice(valid_styles),
            material=choice(valid_materials)
        )
        saddles.append(saddle)

    db.session.bulk_save_objects(saddles)
    db.session.commit()
    return saddles

def create_switches(num_switches=10):
    """Generate switches with valid attributes and relationships."""
    valid_colors = ['White', 'Black', 'Cream', 'Mint Green', 'Aged White', 'Parchment', 'Other']

    switches = []
    for _ in range(num_switches):
        switch = Switch(
            positions=randint(2, 7),
            color=choice(valid_colors)
        )
        switches.append(switch)

    db.session.bulk_save_objects(switches)
    db.session.commit()
    return switches

def create_controls(num_controls=10):
    """Generate controls with valid attributes and relationships."""
    valid_colors = ['White', 'Black', 'Cream', 'Mint Green', 'Aged White', 'Parchment', 'Other']

    controls = []
    for _ in range(num_controls):
        control = Controls(
            configuration=fake.sentence(nb_words=3).rstrip('.'),
            color=choice(valid_colors)
        )
        controls.append(control)

    db.session.bulk_save_objects(controls)
    db.session.commit()
    return controls

def create_tuning_machines(num_tuners=10):
    """Generate tuning machines with valid attributes and relationships."""
    valid_models = ['Vintage', 'Modern', 'Locking', 'Kluson', 'Gotoh', 'Grover', 
                    'Sperzel', 'Hipshot', 'Schaller', 'Other', None]

    tuners = []
    for _ in range(num_tuners):
        tuner = TuningMachine(
            model=choice(valid_models),
            locking=choice([True, False])  # Required boolean
        )
        tuners.append(tuner)

    db.session.bulk_save_objects(tuners)
    db.session.commit()
    return tuners

def create_string_trees(num_trees=10):
    """Generate string trees with valid attributes and relationships."""
    valid_models = ['Vintage', 'Modern', 'Butterfly', 'Disc', 'None', 'Other', None]

    string_trees = []
    for _ in range(num_trees):
        string_tree = StringTree(
            model=choice(valid_models),
            count=randint(0, 4)  # Count must be between 0 and 4
        )
        string_trees.append(string_tree)

    db.session.bulk_save_objects(string_trees)
    db.session.commit()
    return string_trees

def create_neck_plates(num_plates=10):
    """Generate neck plates with valid attributes and relationships."""
    valid_styles = ['Vintage', 'Contour']
    valid_details = ['Serial Number', 'F Logo', 'Anniversary', 'Other', None]

    neck_plates = []
    for _ in range(num_plates):
        neck_plate = NeckPlate(
            style=choice(valid_styles),
            bolts=choice([3, 4, 5, 6]),  # Bolts must be 3, 4, 5, or 6
            details=choice(valid_details)
        )
        neck_plates.append(neck_plate)

    db.session.bulk_save_objects(neck_plates)
    db.session.commit()
    return neck_plates

def create_pickguards(num_pickguards=10):
    """Generate pickguards with valid attributes and relationships."""
    valid_ply_counts = [1, 2, 3, 4, 5, None]
    valid_colors = [
        'White', 'Black', 'Cream', 'Mint Green', 'Parchment', 'Aged White', 
        'Tortoise', 'Red Tortoise', 'Pearloid', 'Anodized', 'Mirror', 'Other'
    ]

    pickguards = []
    for _ in range(num_pickguards):
        pickguard = Pickguard(
            ply_count=choice(valid_ply_counts),
            screws=randint(6, 13),  # Screws must be between 6 and 13
            color=choice(valid_colors)
        )
        pickguards.append(pickguard)

    db.session.bulk_save_objects(pickguards)
    db.session.commit()
    return pickguards

def create_models(num_models=10):
    """Generate guitar models with valid attributes and relationships."""
    valid_countries = [
        'United States', 'Mexico', 'Japan', 'China', 'South Korea', 'Indonesia',
        'India', 'Vietnam', 'Malaysia'
    ]
    valid_relics = ['None', 'Light', 'Medium', 'Heavy', 'Custom']
    valid_hardware_finishes = ['Chrome', 'Nickel', 'Gold', 'Black', 'Other']
    valid_pickup_configurations = ['SSS', 'HSS', 'HH', 'HSH', 'HS', 'Other']
    valid_model_names = [
        "Stratocaster",
        "American Standard",
        "Deluxe",
        "Player Series",
        "Custom Shop '62",
        "American Vintage '59",
        "American Vintage '62",
        "American Vintage '65",
        "American Professional",
        "American Ultra",
        "American Performer",
        "Vintera '50s Stratocaster",
        "Vintera '60s Stratocaster",
        "Vintera '70s Stratocaster",
        "Eric Clapton Signature",
        "Jimi Hendrix Signature",
        "David Gilmour Signature",
        "Jeff Beck Signature",
        "SRV Signature",
        "American Special",
        "Highway One",
        "American Original '50s",
        "American Original '60s",
        "American Original '70s",
        "Custom Shop '50s",
        "Custom Shop '60s",
        "Custom Shop '70s",
    ]

    models = []
    for _ in range(num_models):
        model = Model(
            brand="Fender",
            model_name = choice(valid_model_names),
            year_range=f"{randint(1950, 2020)}-{choice([str(randint(1951, 2023)), 'present'])}",
            country=choice(valid_countries),
            description=fake.sentence(),
            scale_length=round(uniform(20.0, 30.0), 1),
            relic=choice(valid_relics),
            other_controls=sample(["Blend Knob", "Kill Switch", "Mid Boost"], randint(0, 2)),
            hardware_finish=sample(valid_hardware_finishes, randint(1, 3)),
            pickup_configuration=sample(valid_pickup_configurations, randint(1, 3)),
            neck=choice(Neck.query.all()),
            headstock=choice(Headstock.query.all()),
            nut=choice(Nut.query.all()),
            frets=choice(Frets.query.all()),
            inlays=choice(Inlays.query.all()),
            bridge=choice(Bridge.query.all()),
            saddles=choice(Saddles.query.all()),
            tuning_machine=choice(TuningMachine.query.all()),
            string_tree=choice(StringTree.query.all()),
            neck_plate=choice(NeckPlate.query.all())
        )

        db.session.add(model)
        db.session.flush()

        # Many-to-Many Relationships (Variations)
        model.pickups = sample(GuitarPickup.query.all(), randint(1, 3))
        model.bodies = sample(Body.query.all(), randint(1, 2))
        model.fretboards = sample(Fretboard.query.all(), randint(1, 2))
        model.pickguards = sample(Pickguard.query.all(), randint(1, 2))
        model.switches = sample(Switch.query.all(), randint(1, 2))
        model.controls = sample(Controls.query.all(), randint(1, 2))

        models.append(model)

    db.session.bulk_save_objects(models)
    db.session.commit()
    return models

def create_user_guitars(num_guitars=user_guitar_amt):
    """Generate user-created guitars with valid attributes and relationships."""
    valid_countries = ['USA', 'Mexico', 'Japan', 'China', 'Indonesia', 'Korea', 'Custom']
    valid_relics = ['None', 'Light', 'Medium', 'Heavy', 'Custom']
    valid_serial_number_locations = ['Headstock', 'Neck Plate', 'Body Cavity', 'Other']
    valid_prefixes = ["MX", "US", "CN", "J", "I", "A", "B", "C", "D", "E", "F"]
    valid_pickup_configurations = ['SSS', 'HSS', 'HH', 'HSH', 'HS', 'Other']

    user_guitars = []
    users = User.query.all()
    models = Model.query.all()

    # Ensure valid relationships
    bodies = Body.query.all()
    necks = Neck.query.all()
    headstocks = Headstock.query.all()
    fretboards = Fretboard.query.all()
    nuts = Nut.query.all()
    frets = Frets.query.all()
    inlays = Inlays.query.all()
    bridges = Bridge.query.all()
    saddles = Saddles.query.all()
    switches = Switch.query.all()
    controls = Controls.query.all()
    tuning_machines = TuningMachine.query.all()
    string_trees = StringTree.query.all()
    neck_plates = NeckPlate.query.all()
    pickguards = Pickguard.query.all()

    for _ in range(num_guitars):
        owner = choice(users)
        assigned_model = choice(models) if models and randint(0, 1) else None

        modified = choice([True, False])
        modifications = fake.sentence() if modified else None

        user_guitar = UserGuitar(
            brand="Fender",
            name=fake.word().capitalize(),
            serial_number = f"{choice(valid_prefixes)}{randint(10, 23)}{fake.bothify('#####')}",
            serial_number_location=choice(valid_serial_number_locations),
            year=randint(1930, datetime.utcnow().year) if randint(0, 1) else None,
            country=choice(valid_countries),
            description=fake.sentence() if randint(0, 1) else None,
            scale_length=round(uniform(20.0, 30.0), 1) if randint(0, 1) else None,
            weight=f"{round(uniform(6.0, 10.0), 1)} lbs" if randint(0, 1) else None,
            relic=choice(valid_relics),
            other_controls=fake.sentence() if randint(0, 1) else None,
            hardware_finish=choice(['Chrome', 'Nickel', 'Gold', 'Black', 'Other']) if randint(0, 1) else None,
            pickup_configuration=choice(valid_pickup_configurations),
            modified=modified,
            modifications=modifications,
            owner=owner,
            model=assigned_model,
        )

        db.session.add(user_guitar)  # Add to session first
        db.session.flush()  # Force SQLAlchemy to assign an ID

        # Assign relationships AFTER adding but BEFORE flush
        user_guitar.body = choice(bodies) if bodies else None
        user_guitar.neck = choice(necks) if necks else None
        user_guitar.headstock = choice(headstocks) if headstocks else None
        user_guitar.fretboard = choice(fretboards) if fretboards else None
        user_guitar.nut = choice(nuts) if nuts else None
        user_guitar.frets = choice(frets) if frets else None
        user_guitar.inlays = choice(inlays) if inlays else None
        user_guitar.bridge = choice(bridges) if bridges else None
        user_guitar.saddles = choice(saddles) if saddles else None
        user_guitar.switch = choice(switches) if switches else None
        user_guitar.controls = choice(controls) if controls else None
        user_guitar.tuning_machine = choice(tuning_machines) if tuning_machines else None
        user_guitar.string_tree = choice(string_trees) if string_trees else None
        user_guitar.neck_plate = choice(neck_plates) if neck_plates else None
        user_guitar.pickguard = choice(pickguards) if pickguards else None

        # Many-to-Many Relationships
        user_guitar.pickups = sample(GuitarPickup.query.all(), randint(1, 3))

        db.session.add(user_guitar)
        db.session.flush()

        user_guitars.append(user_guitar)

    db.session.commit()
    return user_guitars


if __name__ == "__main__":
    with app.app_context():
        print("Seeding database...")

        
        # Check if the migrations folder exists before initializing
        if not os.path.exists("migrations"):
            print("Running 'flask db init'...")
            init()

        # Run migrations
        print("Running 'flask db migrate'...")
        migrate()

        # Apply migrations
        print("Running 'flask db upgrade'...")
        upgrade()

        print("Seeding database...")

        create_users()
        create_guitar_pickups()
        create_bodies()
        create_necks()
        create_headstocks()
        create_fretboards()
        create_frets()
        create_nuts()
        create_inlays()
        create_bridges()
        create_saddles()
        create_switches()
        create_controls()
        create_tuning_machines()
        create_string_trees()
        create_neck_plates()
        create_pickguards()
        create_models()
        create_user_guitars()

        print("Database seeding complete!")
