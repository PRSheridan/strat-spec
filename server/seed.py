#!/usr/bin/env python3
# seed.py
import json
from random import choice, randint, sample, uniform
from faker import Faker
from datetime import datetime, timedelta

from app import app
from models import (
    db, User, UserGuitar, Model, Body, Neck, Headstock, Fretboard, Nut, Frets, Inlays,
    Bridge, Saddles, Switch, Controls, TuningMachine, StringTree, NeckPlate, Pickguard, GuitarPickup,
    Image
)

fake = Faker()

if __name__ == '__main__':
    with app.app_context():
        print("Starting database seeding...")

        # Clear existing data
        tables = [User, UserGuitar, Model, Body, Neck, Headstock, Fretboard, Nut, Frets, Inlays,
                  Bridge, Saddles, Switch, Controls, TuningMachine, StringTree, NeckPlate, Pickguard, GuitarPickup,
                  Image]
        for table in tables:
            db.session.query(table).delete()
        db.session.commit()

        # Create Users
        users = []
        # Create one admin user
        admin = User(
            username="admin",
            email="admin@stratregistry.com",
            role="admin",
            is_active=True,
            last_login=datetime.now(),
            created_at=datetime.now() - timedelta(days=100),
            updated_at=datetime.now()
        )
        admin.password_hash = "adminpassword"
        users.append(admin)
        
        # Create regular users
        for i in range(9):
            user = User(
                username=fake.user_name(),
                email=fake.email(),
                role="client",
                is_active=True,
                last_login=fake.date_time_between(start_date="-30d", end_date="now"),
                created_at=fake.date_time_between(start_date="-365d", end_date="-30d"),
                updated_at=fake.date_time_between(start_date="-30d", end_date="now")
            )
            user.password_hash = "password123"
            users.append(user)
        
        db.session.add_all(users)
        db.session.commit()
        print("Created users")

        # Create guitar components
        print("Creating guitar components...")
        
        # Create pickups
        pickup_types = ["Single-coil", "Humbucker", "Hot Rails", "Noiseless", "Lace Sensor", 
                       "P90", "Mini-humbucker", "Active", "Lipstick", "Rail", "Vintage"]
        pickup_brands = ["Fender", "Seymour Duncan", "DiMarzio", "EMG", "Lace", "Gibson", "Bare Knuckle"]
        pickup_models = [
            "Custom Shop '69", "Texas Special", "Fat '50s", "Pure Vintage '59", "Noiseless Gen 4",
            "JB Jr", "Little '59", "Pearly Gates", "SSL-5", "SSL-1", "Area 67", "Area 61", 
            "Super Distortion", "Sensor Gold", "Sensor Blue", "Sensor Red", "SA", "Hot Rails"
        ]
        magnets = ["Alnico II", "Alnico III", "Alnico IV", "Alnico V", "Ceramic", "Neodymium"]
        
        pickups = []
        for _ in range(20):
            pickup_type = choice(pickup_types)
            position_options = ["Neck", "Middle", "Bridge"]
            position = [choice(position_options)]
            
            pickups.append(GuitarPickup(
                brand=choice(pickup_brands),
                model=choice(pickup_models),
                position=position,
                type=pickup_type,
                magnet=choice(magnets),
                active=pickup_type == "Active",
                noiseless=pickup_type == "Noiseless" or randint(0, 5) == 0,
                cover=choice(["None", "Chrome", "Nickel", "Black", "Cream"])
            ))
        
        db.session.add_all(pickups)
        
        # Create bodies
        woods = ["Alder", "Ash", "Basswood", "Mahogany", "Poplar"]
        finishes = ["Nitrocellulose", "Polyurethane"]
        colors = ["Sunburst", "Olympic White", "Black", "Fiesta Red", "Lake Placid Blue", 
                 "Candy Apple Red", "Natural", "Seafoam Green", "Sonic Blue", "Burgundy Mist"]
        
        bodies = []
        for _ in range(10):
            bodies.append(Body(
                wood=choice(woods),
                contour=choice(["Shallow", "Deep"]),
                routing=choice(["SSS", "HSS", "HH"]),
                chambering=choice([True, False]),
                binding=choice([True, False]),
                finish=choice(finishes),
                color=choice(colors)
            ))
        
        db.session.add_all(bodies)
        
        # Create necks
        neck_woods = ["Maple", "Mahogany", "Roasted Maple", "Flame Maple", "Birdseye Maple"]
        neck_shapes = ["C", "U", "V", "D", "Modern C", "Soft V"]
        
        necks = []
        for _ in range(8):
            necks.append(Neck(
                wood=choice(neck_woods),
                finish=choice(["Gloss", "Satin", "Natural"]),
                shape=choice(neck_shapes),
                truss_rod=choice(["Modern", "Vintage"])
            ))
        
        db.session.add_all(necks)
        
        # Create headstocks
        headstocks = []
        for _ in range(5):
            headstocks.append(Headstock(
                shape=choice(["Stratocaster Standard", "Stratocaster Large"]),
                decal_style=choice(["Spaghetti Logo", "CBS Logo", "Modern", "Block", "None"]),
                reverse=choice([True, False])
            ))
        
        db.session.add_all(headstocks)
        
        # Create fretboards
        fretboard_materials = ["Maple", "Rosewood", "Ebony", "Pau Ferro", "Richlite"]
        radiuses = ["7.25\"", "9.5\"", "10\"", "12\"", "Compound"]
        
        fretboards = []
        for _ in range(8):
            fretboards.append(Fretboard(
                material=choice(fretboard_materials),
                radius=choice(radiuses),
                fret_count=choice([21, 22, 24]),
                binding=choice([True, False]),
                scalloped=choice([True, False])
            ))
        
        db.session.add_all(fretboards)
        
        # Create other components briefly
        nuts = [Nut(width=choice(["1.650\"", "1.685\""]), material=choice(["Bone", "Plastic", "Graphite", "Tusq"]), locking=choice([True, False])) for _ in range(5)]
        db.session.add_all(nuts)
        
        frets = [Frets(material=choice(["Nickel Silver", "Stainless Steel", "Jescar EVO Gold"]), size=choice(["Vintage", "Medium", "Jumbo", "Medium Jumbo"])) for _ in range(5)]
        db.session.add_all(frets)
        
        inlays = [Inlays(shape=choice(["Dot", "Block", "None"]), material=choice(["Pearloid", "Abalone", "Plastic"]), spacing=choice(["Vintage", "Modern"])) for _ in range(5)]
        db.session.add_all(inlays)
        
        bridges = [Bridge(model=choice(["Vintage Tremolo", "2-Point Tremolo", "Hardtail"]), screws=choice([2, 6]), spacing=choice([52, 54]), tremolo=choice([True, False])) for _ in range(5)]
        db.session.add_all(bridges)
        
        saddles = [Saddles(style=choice(["Vintage", "Modern", "Block"]), material=choice(["Steel", "Brass", "Graphite"])) for _ in range(5)]
        db.session.add_all(saddles)
        
        switches = [Switch(positions=choice([3, 5]), color=choice(["White", "Black", "Mint Green", "Cream"])) for _ in range(5)]
        db.session.add_all(switches)
        
        controls = [Controls(configuration=choice(["1 Volume, 2 Tone", "1 Volume, 1 Tone"]), color=choice(["White", "Black", "Mint Green", "Cream"])) for _ in range(5)]
        db.session.add_all(controls)
        
        tuning_machines = [TuningMachine(model=choice(["Vintage", "Modern", "Locking"]), locking=choice([True, False])) for _ in range(5)]
        db.session.add_all(tuning_machines)
        
        string_trees = [StringTree(model=choice(["Vintage", "Modern", "Butterfly", "Disc", "None"]), count=randint(0, 2)) for _ in range(5)]
        db.session.add_all(string_trees)
        
        neck_plates = [NeckPlate(style=choice(["Vintage", "Contour"]), bolts=choice([3, 4]), details=choice(["F Logo", "Serial Number", "None"])) for _ in range(5)]
        db.session.add_all(neck_plates)
        
        pickguards = [Pickguard(ply_count=choice([1, 3]), screws=choice([8, 11]), color=choice(["White", "Black", "Mint Green", "Tortoise", "Parchment"])) for _ in range(5)]
        db.session.add_all(pickguards)
        
        db.session.commit()
        print("Created all guitar components")

        # Create Models
        print("Creating models...")
        models = [
            # 1. American Professional II
            Model(
                brand="Fender",
                model_name="American Professional II Stratocaster",
                year_range="2020-present",
                country="United States",
                description="The evolution of Fender's flagship model with V-Mod II pickups and push-push switching.",
                scale_length=25.5,
                pickup_configuration={"config": "SSS"},
                other_controls={"controls": ["Push-Push Switch"]},
                hardware_finish={"finish": "Nickel"},
                relic="None",
                neck=necks[0],
                headstock=headstocks[0],
                nut=nuts[0],
                frets=frets[0],
                inlays=inlays[0],
                bridge=bridges[0],
                saddles=saddles[0],
                tuning_machine=tuning_machines[0],
                string_tree=string_trees[0],
                neck_plate=neck_plates[0],
                created_at=datetime(2020, 10, 1),
                updated_at=datetime(2020, 10, 1)
            ),
            # 2. American Vintage II
            Model(
                brand="Fender",
                model_name="American Vintage II 1957 Stratocaster",
                year_range="2022-present",
                country="United States",
                description="Historically accurate recreation of the 1957 Stratocaster with period-correct details.",
                scale_length=25.5,
                pickup_configuration={"config": "SSS"},
                other_controls=None,
                hardware_finish={"finish": "Chrome"},
                relic="None",
                neck=necks[1],
                headstock=headstocks[1],
                nut=nuts[1],
                frets=frets[1],
                inlays=inlays[1],
                bridge=bridges[1],
                saddles=saddles[1],
                tuning_machine=tuning_machines[1],
                string_tree=string_trees[1],
                neck_plate=neck_plates[1],
                created_at=datetime(2022, 7, 1),
                updated_at=datetime(2022, 7, 1)
            ),
            # 3. Player Series
            Model(
                brand="Fender",
                model_name="Player Stratocaster",
                year_range="2018-present",
                country="Mexico",
                description="Mexican-made Stratocaster with modern features at an accessible price point.",
                scale_length=25.5,
                pickup_configuration={"config": "SSS"},
                other_controls=None,
                hardware_finish={"finish": "Chrome"},
                relic="None",
                neck=necks[2],
                headstock=headstocks[2],
                nut=nuts[2],
                frets=frets[2],
                inlays=inlays[2],
                bridge=bridges[2],
                saddles=saddles[2],
                tuning_machine=tuning_machines[2],
                string_tree=string_trees[2],
                neck_plate=neck_plates[2],
                created_at=datetime(2018, 6, 1),
                updated_at=datetime(2018, 6, 1)
            ),
            # 4. Custom Shop
            Model(
                brand="Fender",
                model_name="Custom Shop 1969 Stratocaster Relic",
                year_range="2015-present",
                country="United States",
                description="Master-built recreation with authentic aging and hand-wound pickups.",
                scale_length=25.5,
                pickup_configuration={"config": "SSS"},
                other_controls=None,
                hardware_finish={"finish": "Nickel"},
                relic="Medium",
                neck=necks[3],
                headstock=headstocks[3],
                nut=nuts[3],
                frets=frets[3],
                inlays=inlays[3],
                bridge=bridges[3],
                saddles=saddles[3],
                tuning_machine=tuning_machines[3],
                string_tree=string_trees[3],
                neck_plate=neck_plates[3],
                created_at=datetime(2015, 1, 1),
                updated_at=datetime(2015, 1, 1)
            ),
            # 5. Eric Clapton Signature
            Model(
                brand="Fender",
                model_name="Eric Clapton Signature Stratocaster",
                year_range="1988-present",
                country="United States",
                description="Signature model featuring Noiseless pickups and active mid-boost circuit.",
                scale_length=25.5,
                pickup_configuration={"config": "SSS"},
                other_controls={"controls": ["Mid Boost"]},
                hardware_finish={"finish": "Chrome"},
                relic="None",
                neck=necks[4],
                headstock=headstocks[0],
                nut=nuts[0],
                frets=frets[0],
                inlays=inlays[0],
                bridge=bridges[0],
                saddles=saddles[0],
                tuning_machine=tuning_machines[0],
                string_tree=string_trees[0],
                neck_plate=neck_plates[0],
                created_at=datetime(2010, 1, 1),
                updated_at=datetime(2010, 1, 1)
            ),
            # 6. Vintera
            Model(
                brand="Fender",
                model_name="Vintera '50s Stratocaster",
                year_range="2019-present",
                country="Mexico",
                description="Vintage-style Stratocaster with '50s features and period-correct pickups.",
                scale_length=25.5,
                pickup_configuration={"config": "SSS"},
                other_controls=None,
                hardware_finish={"finish": "Chrome"},
                relic="None",
                neck=necks[5],
                headstock=headstocks[1],
                nut=nuts[1],
                frets=frets[1],
                inlays=inlays[1],
                bridge=bridges[1],
                saddles=saddles[1],
                tuning_machine=tuning_machines[1],
                string_tree=string_trees[1],
                neck_plate=neck_plates[1],
                created_at=datetime(2019, 1, 1),
                updated_at=datetime(2019, 1, 1)
            ),
            # 7. American Ultra
            Model(
                brand="Fender",
                model_name="American Ultra Stratocaster",
                year_range="2019-present",
                country="United States",
                description="Modern features with Ultra Noiseless pickups and compound radius fingerboard.",
                scale_length=25.5,
                pickup_configuration={"config": "SSS"},
                other_controls={"controls": ["S-1 Switch"]},
                hardware_finish={"finish": "Chrome"},
                relic="None",
                neck=necks[6],
                headstock=headstocks[2],
                nut=nuts[2],
                frets=frets[2],
                inlays=inlays[2],
                bridge=bridges[2],
                saddles=saddles[2],
                tuning_machine=tuning_machines[2],
                string_tree=string_trees[2],
                neck_plate=neck_plates[2],
                created_at=datetime(2019, 11, 1),
                updated_at=datetime(2019, 11, 1)
            ),
            # 8. Classic Vibe
            Model(
                brand="Squier",
                model_name="Classic Vibe '60s Stratocaster",
                year_range="2019-present",
                country="Indonesia",
                description="Vintage-inspired Stratocaster with Alnico pickups and period-correct details.",
                scale_length=25.5,
                pickup_configuration={"config": "SSS"},
                other_controls=None,
                hardware_finish={"finish": "Chrome"},
                relic="None",
                neck=necks[7],
                headstock=headstocks[3],
                nut=nuts[3],
                frets=frets[3],
                inlays=inlays[3],
                bridge=bridges[3],
                saddles=saddles[3],
                tuning_machine=tuning_machines[3],
                string_tree=string_trees[3],
                neck_plate=neck_plates[3],
                created_at=datetime(2019, 1, 1),
                updated_at=datetime(2019, 1, 1)
            )
        ]
        
        # Add components to the models
        for model in models:
            # Add random bodies, pickups, etc.
            model.bodies.extend(sample(bodies, randint(1, 2)))
            model.pickups.extend(sample(pickups, randint(2, 3)))
            model.fretboards.extend([choice(fretboards)])
            model.pickguards.extend(sample(pickguards, randint(1, 2)))
            model.switches.extend([choice(switches)])
            model.controls.extend([choice(controls)])
        
        db.session.add_all(models)
        db.session.commit()
        print(f"Created {len(models)} guitar models")

        # Create User Guitars
        print("Creating user guitars...")
        user_guitars = []
        
        for i in range(55):  # Create 55 user guitars
            # 70% chance of having a model
            use_model = randint(1, 10) <= 7
            model = choice(models) if use_model else None
            is_modified = choice([True, False]) if use_model else True
            
            # Basic details
            name = model.model_name if model and not is_modified else f"Custom Strat #{i+1}"
            brand = model.brand if model else choice(["Fender", "Squier", "Partscaster"])
            country = model.country if model else choice(["USA", "Mexico", "Japan", "Indonesia"])
            
            # Generate a random serial number
            year = randint(1954, 2023)
            serial_number = f"{choice(['Z', 'US', 'MX', 'JD', 'IC'])}{randint(10000, 999999)}"
            
            # Create the user guitar
            user_guitar = UserGuitar(
                brand=brand,
                name=name,
                serial_number=serial_number,
                serial_number_location=choice(["Headstock", "Neck Plate"]),
                year=year,
                country=country,
                description=fake.paragraph() if randint(1, 4) > 1 else None,
                scale_length=25.5,
                weight=f"{uniform(7.2, 8.9):.1f} lbs",
                relic=model.relic if model else choice(["None", "Light", "Medium", "Heavy"]),
                other_controls=model.other_controls["controls"][0] if model and model.other_controls else choice(["None", "S-1 Switch", "Push-Pull"]),
                hardware_finish=model.hardware_finish["finish"] if model else choice(["Chrome", "Nickel", "Gold"]),
                modified=is_modified,
                modifications=fake.sentence() if is_modified else None,
                pickup_configuration=model.pickup_configuration["config"] if model else choice(["SSS", "HSS", "HH"]),
                owner=choice(users),
                model=model,
                # Component assignments - use model's if available, otherwise random
                body=choice(bodies),
                neck=model.neck if model else choice(necks),
                headstock=model.headstock if model else choice(headstocks),
                fretboard=choice(list(model.fretboards)) if model and model.fretboards else choice(fretboards),
                nut=model.nut if model else choice(nuts),
                frets=model.frets if model else choice(frets),
                inlays=model.inlays if model else choice(inlays),
                bridge=model.bridge if model else choice(bridges),
                saddles=model.saddles if model else choice(saddles),
                switch=choice(list(model.switches)) if model and model.switches else choice(switches),
                controls=choice(list(model.controls)) if model and model.controls else choice(controls),
                tuning_machine=model.tuning_machine if model else choice(tuning_machines),
                string_tree=model.string_tree if model else choice(string_trees),
                neck_plate=model.neck_plate if model else choice(neck_plates),
                pickguard=choice(list(model.pickguards)) if model and model.pickguards else choice(pickguards),
                created_at=fake.date_time_between(start_date="-1y", end_date="now"),
                updated_at=fake.date_time_between(start_date="-1m", end_date="now")
            )
            
            # Add pickups
            if model and model.pickups:
                user_guitar.pickups.extend(sample(list(model.pickups), min(3, len(list(model.pickups)))))
            else:
                user_guitar.pickups.extend(sample(pickups, randint(2, 3)))
                
            user_guitars.append(user_guitar)

        db.session.add_all(user_guitars)
        db.session.commit()
        print(f"Created {len(user_guitars)} user guitars")

        print("Database seeding complete!")