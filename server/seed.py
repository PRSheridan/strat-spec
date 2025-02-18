#!/usr/bin/env python3
# seed.py
from random import choice, randint
from faker import Faker

from app import app
from models import db, User, UserGuitar, Model, Body, Neck, Headstock, Fretboard, Nut, Frets, Inlays, Bridge, Saddles, Switch, Controls, TuningMachine, StringTree, NeckPlate, Pickguard

fake = Faker()

if __name__ == '__main__':
    with app.app_context():
        print("Starting database seeding...")

        # Clear existing data
        tables = [User, UserGuitar, Model, Body, Neck, Headstock, Fretboard, Nut, Frets, Inlays, Bridge, Saddles, Switch, Controls, TuningMachine, StringTree, NeckPlate, Pickguard]
        for table in tables:
            db.session.query(table).delete()
        db.session.commit()

        # Create Users
        users = [User(username=fake.user_name(), email=fake.email(), role="client") for _ in range(10)]
        db.session.add_all(users)
        db.session.commit()

        # Create Stratocaster components with more variety
        bodies = [
            Body(wood=choice(["Alder", "Ash", "Basswood", "Mahogany"]), contour=choice(["Standard", "Deep", "Slim"]),
                 routing=choice(["SSS", "HSS", "HH"]), finish=choice(["Gloss", "Matte", "Satin"]),
                 color=choice(["Sunburst", "Black", "Olympic White", "Candy Apple Red", "Natural"]))
            for _ in range(5)
        ]
        db.session.add_all(bodies)

        necks = [
            Neck(wood=choice(["Maple", "Mahogany", "Rosewood"]), finish=choice(["Satin", "Gloss"]), shape=choice(["C", "V", "D"]),
                 scale_length="25.5", truss_rod=choice(["Standard", "Dual-Action"]))
            for _ in range(3)
        ]
        db.session.add_all(necks)

        headstocks = [
            Headstock(shape=choice(["Standard", "Large", "Reverse"]), decal_style=choice(["Spaghetti Logo", "CBS Logo"]), reverse=choice([True, False]))
            for _ in range(3)
        ]
        db.session.add_all(headstocks)

        fretboards = [
            Fretboard(material=choice(["Maple", "Rosewood", "Ebony"]), radius=choice(["7.25", "9.5", "12"]))
            for _ in range(3)
        ]
        db.session.add_all(fretboards)

        nuts = [Nut(width=choice(["1.650", "1.685", "1.625"]), material=choice(["Bone", "Synthetic"]), locking=choice([True, False]))]
        db.session.add_all(nuts)

        frets = [Frets(count=choice([21, 22, 24]), material=choice(["Nickel", "Stainless Steel"]), size=choice(["Medium Jumbo", "Jumbo"]))]
        db.session.add_all(frets)

        inlays = [Inlays(shape=choice(["Dots", "Blocks", "None"]), material=choice(["Pearl", "Abalone", "Clay"]), spacing="Standard")]
        db.session.add_all(inlays)

        bridges = [
            Bridge(model=choice(["Vintage Synchronized Tremolo", "Two-Point Tremolo", "Hardtail"]), screws=choice([2, 6]), spacing=choice(["Standard", "Wide"]))
            for _ in range(3)
        ]
        db.session.add_all(bridges)

        saddles = [Saddles(style=choice(["Bent Steel", "Block"]), material=choice(["Nickel", "Brass"]))]
        db.session.add_all(saddles)

        switches = [Switch(positions=choice([3, 5]), color=choice(["White", "Black", "Cream"]))]
        db.session.add_all(switches)

        controls = [Controls(configuration=choice(["1 Volume, 2 Tone", "1 Volume, 1 Tone"]), color=choice(["Aged White", "Black"]))]
        db.session.add_all(controls)

        tuning_machines = [TuningMachine(model=choice(["Fender Standard", "Fender Locking"]), locking=choice([True, False]))]
        db.session.add_all(tuning_machines)

        string_trees = [StringTree(model=choice(["Butterfly", "Bar"]), count=randint(1, 2))]
        db.session.add_all(string_trees)

        neck_plates = [NeckPlate(style=choice(["Standard", "Engraved"]), bolts=4)]
        db.session.add_all(neck_plates)

        pickguards = [Pickguard(ply_count=choice([1, 3]), screws=choice([8, 11]), configuration=choice(["SSS", "HSS"]), color=choice(["White", "Black", "Tortoiseshell"]))]
        db.session.add_all(pickguards)

        db.session.commit()

        # Create at least 8 real-ish Stratocaster Models
        model_names = [
            "Stratocaster Standard", "Stratocaster Deluxe", "Stratocaster Hardtail", "Stratocaster Elite",
            "Stratocaster Plus", "Stratocaster American Vintage", "Stratocaster Player Series", "Stratocaster Ultra"
        ]
        models = [
            Model(
                model_name=name,
                year_range=f"{randint(1954, 2025)}-{randint(1955, 2025)}",
                country=choice(["USA", "Mexico", "Japan", "Indonesia"]),
                pickup_configuration=choice(["SSS", "HSS", "HH"]),
                other_controls=choice(["None", "Push-Pull Tone for Coil Split"]),
                hardware_finish=choice(["Chrome", "Nickel", "Gold"]),
                relic=choice(["NOS", "Light", "Heavy", "None"]),
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
                pickguard=choice(pickguards)
            ) for name in model_names
        ]
        db.session.add_all(models)
        db.session.commit()

                # Create UserGuitars
        user_guitars = []
        for i in range(200):
            model = choice(models) if randint(0, 1) else None
            user_guitar = UserGuitar(
                name=f"Stratocaster #{i+1}",
                serial_number=randint(100000, 999999),
                serial_number_location="Headstock",
                year=str(randint(1954, 2025)),
                country=choice(["USA", "Mexico", "Japan", "Indonesia"]),
                weight=randint(6, 10),
                pickup_configuration=choice(["SSS", "HSS", "HH"]),
                other_controls=choice(["None", "Push-Pull Tone for Coil Split"]),
                hardware_finish=choice(["Chrome", "Nickel", "Gold"]),
                modified=choice([True, False]),
                modifications=fake.sentence() if randint(0, 1) else "",
                relic=choice(["NOS", "Light", "Heavy", "None"]),
                owner=choice(users),
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
                model=model
            )
            user_guitars.append(user_guitar)

        db.session.add_all(user_guitars)
        db.session.commit()

        print("Database seeding complete!")

