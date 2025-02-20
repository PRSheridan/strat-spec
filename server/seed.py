#!/usr/bin/env python3
# seed.py
import json
from random import choice, randint, sample
from faker import Faker

from app import app
from models import (
    db, User, UserGuitar, Model, Body, Neck, Headstock, Fretboard, Nut, Frets, Inlays,
    Bridge, Saddles, Switch, Controls, TuningMachine, StringTree, NeckPlate, Pickguard, GuitarPickup
)

fake = Faker()

if __name__ == '__main__':
    with app.app_context():
        print("Starting database seeding...")

        # Clear existing data
        tables = [User, UserGuitar, Model, Body, Neck, Headstock, Fretboard, Nut, Frets, Inlays,
                  Bridge, Saddles, Switch, Controls, TuningMachine, StringTree, NeckPlate, Pickguard, GuitarPickup]
        for table in tables:
            db.session.query(table).delete()
        db.session.commit()

        # Create Users
        users = [User(username=fake.user_name(), email=fake.email(), role="client") for _ in range(10)]
        db.session.add_all(users)
        db.session.commit()

        # Create GuitarPickups
        pickups = [
            GuitarPickup(
                brand=choice(["Fender", "Seymour Duncan", "DiMarzio", "Gibson"]),
                model=choice(["Texas Special", "Custom '69", "Noiseless Gen 4", "Fat '50s"]),
                position=json.dumps(sample(["Neck", "Middle", "Bridge"], randint(1, 3))),  # Store JSON
                type=choice(["Single-Coil", "Humbucker", "P-90"]),
                magnet=choice(["Alnico V", "Ceramic", "Alnico II"]),
                resistance=round(randint(5, 15) + fake.random.random(), 1),
                inductance=round(randint(1, 10) + fake.random.random(), 2),
                active=choice([True, False]),
                noiseless=choice([True, False]),
                staggered_poles=choice([True, False]),
                wax_potted=choice([True, False]),
                cover=choice(["White", "Black", "None"])
            ) for _ in range(10)
        ]
        db.session.add_all(pickups)

        # Create Stratocaster Components
        bodies = [Body(wood=choice(["Alder", "Ash", "Mahogany"]), contour=choice(["Standard", "Deep"]),
                       routing=choice(["SSS", "HSS", "HH"]), chambering=choice([True, False]),
                       binding=choice([True, False]), finish=choice(["Gloss", "Satin"]),
                       color=choice(["Sunburst", "Black", "Olympic White", "Red", "Natural"])) for _ in range(5)]
        db.session.add_all(bodies)

        necks = [Neck(wood=choice(["Maple", "Mahogany"]), finish=choice(["Satin", "Gloss"]), shape=choice(["C", "V"]),
                      truss_rod=choice(["Standard", "Dual-Action"])) for _ in range(3)]
        db.session.add_all(necks)

        headstocks = [Headstock(shape=choice(["Standard", "Large", "Reverse"]), decal_style=choice(["Spaghetti", "CBS"]),
                                reverse=choice([True, False])) for _ in range(3)]
        db.session.add_all(headstocks)

        fretboards = [Fretboard(material=choice(["Maple", "Rosewood", "Ebony"]), radius=choice(["7.25", "9.5", "12"]),
                                fret_count=choice([21, 22, 24]), binding=choice([True, False]),
                                scalloped=choice([True, False])) for _ in range(3)]
        db.session.add_all(fretboards)

        nuts = [Nut(width=choice(["1.650", "1.685"]), material=choice(["Bone", "Synthetic"]), locking=choice([True, False]))]
        db.session.add_all(nuts)

        frets = [Frets(material=choice(["Nickel", "Stainless Steel"]), size=choice(["Medium Jumbo", "Jumbo"]))]
        db.session.add_all(frets)

        inlays = [Inlays(shape=choice(["Dots", "Blocks", "None"]), material=choice(["Pearl", "Abalone"]), spacing="Standard")]
        db.session.add_all(inlays)

        bridges = [Bridge(model=choice(["Vintage Tremolo", "Hardtail"]), screws=choice([2, 6]), spacing=choice([52.5, 56]))]
        db.session.add_all(bridges)

        saddles = [Saddles(style=choice(["Bent Steel", "Block"]), material=choice(["Nickel", "Brass"]))]        
        db.session.add_all(saddles)

        switches = [Switch(positions=choice([3, 5]), color=choice(["White", "Black"]))]        
        db.session.add_all(switches)

        controls = [Controls(configuration=choice(["1 Volume, 2 Tone", "1 Volume, 1 Tone"]), color=choice(["White", "Black"]))]        
        db.session.add_all(controls)

        tuning_machines = [TuningMachine(model=choice(["Fender Standard", "Fender Locking"]), locking=choice([True, False]))]        
        db.session.add_all(tuning_machines)

        string_trees = [StringTree(model=choice(["Butterfly", "Bar"]), count=randint(1, 2))]        
        db.session.add_all(string_trees)

        neck_plates = [NeckPlate(style=choice(["Standard", "Engraved"]), bolts=4)]
        db.session.add_all(neck_plates)

        pickguards = [Pickguard(ply_count=choice([1, 3]), screws=choice([8, 11]), configuration=choice(["SSS", "HSS"]),
                                color=choice(["White", "Black", "Tortoiseshell"]))]        
        db.session.add_all(pickguards)

        db.session.commit()

        # Create Models
        model_names = ["Strat Standard", "Strat Deluxe", "Strat Hardtail", "Strat Elite",
                       "Strat Plus", "Strat Vintage", "Strat Player", "Strat Ultra"]
        models = []
        for name in model_names:
            model = Model(
                brand=choice(["Fender", "Squier"]),
                model_name=name,
                year_range=f"{randint(1954, 2025)}-{randint(1955, 2025)}",
                country=choice(["USA", "Mexico", "Japan"]),
                scale_length=25.5,
                pickup_configuration=json.dumps([choice(["SSS", "HSS", "HH"])]),
                other_controls=choice(["None", "Push-Pull Tone"]),
                hardware_finish=json.dumps([choice(["Chrome", "Nickel", "Gold"])]),
                relic=choice(["NOS", "Light", "Heavy", "None"]),
                neck=choice(necks),
                headstock=choice(headstocks),
                nut=choice(nuts),
                frets=choice(frets),
                inlays=choice(inlays),
                bridge=choice(bridges),
                saddles=choice(saddles),
                tuning_machine=choice(tuning_machines),
                string_tree=choice(string_trees),
                neck_plate=choice(neck_plates),
            )

            model.bodies.extend(sample(bodies, randint(1, 2)))  
            model.pickguards.extend(sample(pickguards, randint(1, 2)))
            model.pickups.extend(sample(pickups, randint(1, 3)))

            models.append(model)

        db.session.add_all(models)
        db.session.commit()

        # Create User Guitars
        user_guitars = []
        for i in range(50):  # 50 User-created guitars
            model = choice(models) if randint(1, 10) <= 6 else None  # 60% chance of having a model
            is_modified = choice([True, False]) if model else True  # If it has a model, 50% chance of being modified

            user_guitar = UserGuitar(
                brand=choice(["Fender", "Squier"]),
                name=model.model_name if model else f"Custom Strat #{i+1}",
                serial_number=str(randint(100000, 999999)),
                serial_number_location="Headstock",
                year=randint(1954, 2025),
                country=choice(["USA", "Mexico", "Japan", "Indonesia"]),
                scale_length=25.5,
                weight=str(randint(6, 10)),  # Keeping weight as string per model
                pickup_configuration=json.dumps([choice(["SSS", "HSS", "HH"])]),  # JSON array (list)
                other_controls=choice(["None", "Push-Pull Tone", "Mid Boost", "Treble Bleed"]),
                hardware_finish=json.dumps([choice(["Chrome", "Nickel", "Gold"])]),  # JSON array (list)
                modified=is_modified,
                modifications=fake.sentence() if is_modified else None,
                relic=choice(["NOS", "Light", "Heavy", "None"]),
                owner=choice(users),
                model=model,  # Links to a model (or None)
                body=choice(bodies),
                neck=choice(necks),
                headstock=choice(headstocks),
                fretboard=choice(fretboards),
                nut=choice(nuts),
                frets=choice(frets),
                inlays=choice(inlays),
                bridge=choice(bridges),
                saddles=choice(saddles),
                switch=choice(switches),
                controls=choice(controls),
                tuning_machine=choice(tuning_machines),
                string_tree=choice(string_trees),
                neck_plate=choice(neck_plates),
                pickguard=choice(pickguards),
                pickups=sample(pickups, randint(1, 3))  # Assign random pickups
            )
            user_guitars.append(user_guitar)

        db.session.add_all(user_guitars)
        db.session.commit()

        print("Database seeding complete!")
