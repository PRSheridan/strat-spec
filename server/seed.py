#!/usr/bin/env python3
#seed.py
from random import sample, choice
from faker import Faker

from app import app
from models import db, User, Guitar, Model, Body, Neck, Fretboard, Nut, TrussRod, Pickups, Bridge, TuningMachine, StringTree, Pickguard, ControlKnob, SwitchTip, NeckPlate

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting guitar seeding...")

        # Create example users with roles
        users = [
            User(username="client1", email="client1@example.com", role="client"),
            User(username="client2", email="client2@example.com", role="client"),
            User(username="client3", email="client3@example.com", role="client"),
            User(username="sheridan", email="sheridan@example.com", role="admin")  # Example of an admin
        ]
        db.session.add_all(users)
        db.session.commit()

        # Create example Stratocaster parts with specific attributes

        # Body Model Data
        bodies = [
            Body(body_type="Solid", body_wood="Alder", color="Sunburst", finish_type="Gloss"),
            Body(body_type="Solid", body_wood="Ash", color="Black", finish_type="Satin"),
            Body(body_type="Solid", body_wood="Poplar", color="Red", finish_type="Matte")
        ]
        db.session.add_all(bodies)

        # Neck Model Data
        necks = [
            Neck(shape="C Shape", wood="Maple", finish="Satin"),
            Neck(shape="V Shape", wood="Rosewood", finish="Gloss"),
            Neck(shape="U Shape", wood="Mahogany", finish="Oil")
        ]
        db.session.add_all(necks)

        # Fretboard Model Data
        fretboards = [
            Fretboard(material="Maple", radius="9.5", frets="22"),
            Fretboard(material="Rosewood", radius="12", frets="24"),
            Fretboard(material="Ebony", radius="10", frets="21")
        ]
        db.session.add_all(fretboards)

        # Nut Model Data
        nuts = [
            Nut(material="Bone"),
            Nut(material="Plastic"),
            Nut(material="Synthetic")
        ]
        db.session.add_all(nuts)

        # TrussRod Model Data
        truss_rods = [
            TrussRod(type="Vintage", location="Headstock"),
            TrussRod(type="Modern", location="Heel"),
            TrussRod(type="Dual-Action", location="Headstock")
        ]
        db.session.add_all(truss_rods)

        # Pickups Model Data
        pickups = [
            Pickups(pickup_configuration="Single-Coil"),
            Pickups(pickup_configuration="Humbucker"),
            Pickups(pickup_configuration="P90")
        ]
        db.session.add_all(pickups)

        # Bridge Model Data
        bridges = [
            Bridge(bridge_type="Vintage Synchronized Tremolo"),
            Bridge(bridge_type="Hardtail"),
            Bridge(bridge_type="Floating Tremolo")
        ]
        db.session.add_all(bridges)

        # TuningMachine Model Data
        tuning_machines = [
            TuningMachine(machine_type="Standard"),
            TuningMachine(machine_type="Locking"),
            TuningMachine(machine_type="Vintage Style")
        ]
        db.session.add_all(tuning_machines)

        # StringTree Model Data
        string_trees = [
            StringTree(tree_type="Fender"),
            StringTree(tree_type="Planet Waves"),
            StringTree(tree_type="Schaller")
        ]
        db.session.add_all(string_trees)

        # Pickguard Model Data
        pickguards = [
            Pickguard(layers="3-Ply", color="White"),
            Pickguard(layers="1-Ply", color="Black"),
            Pickguard(layers="5-Ply", color="Tortoise Shell")
        ]
        db.session.add_all(pickguards)

        # ControlKnob Model Data
        control_knobs = [
            ControlKnob(style="Plastic"),
            ControlKnob(style="Metal"),
            ControlKnob(style="Vintage")
        ]
        db.session.add_all(control_knobs)

        # SwitchTip Model Data
        switch_tips = [
            SwitchTip(style="Standard White"),
            SwitchTip(style="Standard Black"),
            SwitchTip(style="Vintage Cream")
        ]
        db.session.add_all(switch_tips)

        # NeckPlate Model Data
        neck_plates = [
            NeckPlate(style="Fender"),
            NeckPlate(style="Aftermarket"),
            NeckPlate(style="Custom")
        ]
        db.session.add_all(neck_plates)

        # Commit all part data to the database
        db.session.commit()

        # Create guitar models linking parts

        models = [
            Model(name="Stratocaster Standard", years="1954-1959", body_id=1, neck_id=1, fretboard_id=1, nut_id=1, truss_rod_id=1, pickups_id=1, bridge_id=1, tuning_machine_id=1, string_tree_id=1, pickguard_id=1, control_knob_id=1, switch_tip_id=1, neck_plate_id=1),
            Model(name="Stratocaster Deluxe", years="1960-1965", body_id=2, neck_id=2, fretboard_id=2, nut_id=2, truss_rod_id=2, pickups_id=2, bridge_id=2, tuning_machine_id=2, string_tree_id=2, pickguard_id=2, control_knob_id=2, switch_tip_id=2, neck_plate_id=2),
            Model(name="Stratocaster American Professional", years="2017-present", body_id=1, neck_id=1, fretboard_id=1, nut_id=1, truss_rod_id=1, pickups_id=1, bridge_id=1, tuning_machine_id=1, string_tree_id=1, pickguard_id=1, control_knob_id=1, switch_tip_id=1, neck_plate_id=1),
            Model(name="Stratocaster Player", years="2018-present", body_id=3, neck_id=3, fretboard_id=3, nut_id=3, truss_rod_id=3, pickups_id=3, bridge_id=3, tuning_machine_id=3, string_tree_id=3, pickguard_id=3, control_knob_id=3, switch_tip_id=3, neck_plate_id=3)
        ]
        db.session.add_all(models)
        db.session.commit()

        # Create guitars based on models
        guitars = []
        for _ in range(5):  # Create 5 guitars
            model = choice(models)  # Randomly choose a model

            guitar = Guitar(
                name=fake.word().capitalize() + " Stratocaster",  # Random name based on fake word
                description=fake.text(),
                serial_number=fake.uuid4(),
                user_id=choice(users).id,  # Random user
                model_id=model.id  # Link to the chosen model
            )

            guitars.append(guitar)

        # Add guitars to the session
        db.session.add_all(guitars)
        db.session.commit()

        print("Guitar seeding complete!")

