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
        db.session.query(User).delete()
        db.session.query(UserGuitar).delete()
        db.session.query(Model).delete()
        db.session.query(Body).delete()
        db.session.query(Neck).delete()
        db.session.query(Headstock).delete()
        db.session.query(Fretboard).delete()
        db.session.query(Nut).delete()
        db.session.query(Frets).delete()
        db.session.query(Inlays).delete()
        db.session.query(Bridge).delete()
        db.session.query(Saddles).delete()
        db.session.query(Switch).delete()
        db.session.query(Controls).delete()
        db.session.query(TuningMachine).delete()
        db.session.query(StringTree).delete()
        db.session.query(NeckPlate).delete()
        db.session.query(Pickguard).delete()
        db.session.commit()

        # Create Users
        users = [User(username=fake.user_name(), email=fake.email(), role="client") for _ in range(10)]
        db.session.add_all(users)
        db.session.commit()

        # Create Stratocaster components
        bodies = [
            Body(wood="Alder", contour="Standard", routing="SSS", finish="Gloss", color="Sunburst"),
            Body(wood="Ash", contour="Deep", routing="HSS", finish="Satin", color="Black"),
            Body(wood="Basswood", contour="Standard", routing="SSS", finish="Matte", color="Olympic White")
        ]
        db.session.add_all(bodies)

        necks = [
            Neck(wood="Maple", finish="Satin", shape="C", scale_length="25.5", truss_rod="Standard"),
            Neck(wood="Mahogany", finish="Gloss", shape="V", scale_length="25.5", truss_rod="Dual-Action")
        ]
        db.session.add_all(necks)

        headstocks = [
            Headstock(shape="Standard", decal_style="Spaghetti Logo", reverse=False),
            Headstock(shape="Large", decal_style="CBS Logo", reverse=False)
        ]
        db.session.add_all(headstocks)

        fretboards = [
            Fretboard(material="Maple", radius="9.5"),
            Fretboard(material="Rosewood", radius="12")
        ]
        db.session.add_all(fretboards)

        nuts = [Nut(width="1.650", material="Bone", locking=False)]
        db.session.add_all(nuts)

        frets = [Frets(count=21, material="Nickel", size="Medium Jumbo")]
        db.session.add_all(frets)

        inlays = [Inlays(shape="Dots", material="Pearl", spacing="Standard")]
        db.session.add_all(inlays)

        bridges = [
            Bridge(model="Vintage Synchronized Tremolo", screws=6, spacing="Standard"),
            Bridge(model="Two-Point Tremolo", screws=2, spacing="Modern")
        ]
        db.session.add_all(bridges)

        saddles = [Saddles(style="Bent Steel", material="Nickel")]
        db.session.add_all(saddles)

        switches = [Switch(positions=5, color="White")]
        db.session.add_all(switches)

        controls = [Controls(configuration="1 Volume, 2 Tone", color="Aged White")]
        db.session.add_all(controls)

        tuning_machines = [
            TuningMachine(model="Fender Standard", locking=False),
            TuningMachine(model="Fender Locking", locking=True)
        ]
        db.session.add_all(tuning_machines)

        string_trees = [StringTree(model="Butterfly", count=1)]
        db.session.add_all(string_trees)

        neck_plates = [NeckPlate(style="Standard", bolts=4)]
        db.session.add_all(neck_plates)

        pickguards = [
            Pickguard(ply_count=3, screws=11, configuration="SSS", color="White"),
            Pickguard(ply_count=1, screws=8, configuration="HSS", color="Black")
        ]
        db.session.add_all(pickguards)

        db.session.commit()

        # Create Models
        models = [
            Model(
                model_name="Stratocaster Standard",
                year_range="1954-1959",
                country="USA",
                pickup_configuration="SSS",
                other_controls="None",
                hardware_finish="Nickel",
                relic="NOS",
                body=bodies[0],
                neck=necks[0],
                headstock=headstocks[0],
                fretboard=fretboards[0],
                nut=nuts[0],
                frets=frets[0],
                inlays=inlays[0],
                bridge=bridges[0],
                saddles=saddles[0],
                switch=switches[0],
                controls=controls[0],
                tuning_machine=tuning_machines[0],
                string_tree=string_trees[0],
                neck_plate=neck_plates[0],
                pickguard=pickguards[0]
            ),
            Model(
                model_name="Stratocaster Deluxe",
                year_range="1960-1965",
                country="USA",
                pickup_configuration="SSS",
                other_controls="None",
                hardware_finish="Nickel",
                relic="Light",
                body=bodies[1],
                neck=necks[1],
                headstock=headstocks[1],
                fretboard=fretboards[1],
                nut=nuts[0],
                frets=frets[0],
                inlays=inlays[0],
                bridge=bridges[1],
                saddles=saddles[0],
                switch=switches[0],
                controls=controls[0],
                tuning_machine=tuning_machines[1],
                string_tree=string_trees[0],
                neck_plate=neck_plates[0],
                pickguard=pickguards[1]
            ),
            Model(
                model_name="Stratocaster Hardtail",
                year_range="1970-1975",
                country="USA",
                pickup_configuration="SSS",
                other_controls="None",
                hardware_finish="Chrome",
                relic="NOS",
                body=bodies[2],
                neck=necks[0],
                headstock=headstocks[1],
                fretboard=fretboards[0],
                nut=nuts[0],
                frets=frets[0],
                inlays=inlays[0],
                bridge=bridges[1],  # Hardtail bridge
                saddles=saddles[0],
                switch=switches[0],
                controls=controls[0],
                tuning_machine=tuning_machines[1],
                string_tree=string_trees[0],
                neck_plate=neck_plates[0],
                pickguard=pickguards[0]
            ),
            Model(
                model_name="Stratocaster CBS Era",
                year_range="1965-1981",
                country="USA",
                pickup_configuration="SSS",
                other_controls="None",
                hardware_finish="Nickel",
                relic="Heavy",
                body=bodies[1],
                neck=necks[1],
                headstock=headstocks[1],
                fretboard=fretboards[1],
                nut=nuts[0],
                frets=frets[0],
                inlays=inlays[0],
                bridge=bridges[0],
                saddles=saddles[0],
                switch=switches[0],
                controls=controls[0],
                tuning_machine=tuning_machines[0],
                string_tree=string_trees[0],
                neck_plate=neck_plates[0],
                pickguard=pickguards[1]
            ),
            Model(
                model_name="Stratocaster American Vintage",
                year_range="1982-1998",
                country="USA",
                pickup_configuration="SSS",
                other_controls="5-way switch",
                hardware_finish="Nickel",
                relic="Light",
                body=bodies[0],
                neck=necks[0],
                headstock=headstocks[0],
                fretboard=fretboards[1],
                nut=nuts[0],
                frets=frets[0],
                inlays=inlays[0],
                bridge=bridges[0],
                saddles=saddles[0],
                switch=switches[0],
                controls=controls[0],
                tuning_machine=tuning_machines[1],
                string_tree=string_trees[0],
                neck_plate=neck_plates[0],
                pickguard=pickguards[0]
            ),
            Model(
                model_name="Stratocaster American Professional",
                year_range="2017-Present",
                country="USA",
                pickup_configuration="HSS",
                other_controls="Push-Pull Tone for Coil Split",
                hardware_finish="Nickel",
                relic="None",
                body=bodies[1],
                neck=necks[1],
                headstock=headstocks[0],
                fretboard=fretboards[1],
                nut=nuts[0],
                frets=frets[0],
                inlays=inlays[0],
                bridge=bridges[1],
                saddles=saddles[0],
                switch=switches[0],
                controls=controls[0],
                tuning_machine=tuning_machines[1],
                string_tree=string_trees[0],
                neck_plate=neck_plates[0],
                pickguard=pickguards[1]
            ),
            Model(
                model_name="Stratocaster Player Series",
                year_range="2018-Present",
                country="Mexico",
                pickup_configuration="HSS",
                other_controls="None",
                hardware_finish="Chrome",
                relic="None",
                body=bodies[2],
                neck=necks[1],
                headstock=headstocks[0],
                fretboard=fretboards[1],
                nut=nuts[0],
                frets=frets[0],
                inlays=inlays[0],
                bridge=bridges[1],
                saddles=saddles[0],
                switch=switches[0],
                controls=controls[0],
                tuning_machine=tuning_machines[1],
                string_tree=string_trees[0],
                neck_plate=neck_plates[0],
                pickguard=pickguards[1]
            ),
            Model(
                model_name="Stratocaster Japanese Reissue",
                year_range="1985-Present",
                country="Japan",
                pickup_configuration="SSS",
                other_controls="None",
                hardware_finish="Nickel",
                relic="Light",
                body=bodies[0],
                neck=necks[0],
                headstock=headstocks[0],
                fretboard=fretboards[1],
                nut=nuts[0],
                frets=frets[0],
                inlays=inlays[0],
                bridge=bridges[0],
                saddles=saddles[0],
                switch=switches[0],
                controls=controls[0],
                tuning_machine=tuning_machines[0],
                string_tree=string_trees[0],
                neck_plate=neck_plates[0],
                pickguard=pickguards[0]
            ),
        ]

        db.session.add_all(models)
        db.session.commit()


        # Create UserGuitars
        user_guitars = []
        for _ in range(200):
            user_guitar = UserGuitar(
                serial_number=randint(100000, 999999),
                serial_number_location="Headstock",
                year=str(randint(1954, 2025)),
                country=choice(["USA", "Mexico", "Japan"]),
                weight=randint(6, 9),
                pickup_configuration=choice(["SSS", "HSS"]),
                other_controls="None",
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
                model=choice(models) if randint(0, 1) else None  # Some guitars are not linked to a model
            )
            user_guitars.append(user_guitar)

        db.session.add_all(user_guitars)
        db.session.commit()

        print("Database seeding complete!")


