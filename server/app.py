#!/usr/bin/env python3
# app.py
from flask import request, session, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.sql.expression import func

from config import app, db, api
from models import User, Image, UserGuitar, Model, Body, Bridge, Saddles, Neck, Headstock, \
    Fretboard, Nut, Inlays, TuningMachine, StringTree, GuitarPickup, Controls, HardwareFinish, PlasticColor

from schemas import UserSchema, UserGuitarSchema, ModelSchema

# Instantiate schema objects
user_schema = UserSchema()
guitar_schema = UserGuitarSchema()
model_schema = ModelSchema()

@app.route('/')
def index():
    return {'message': 'Strat-spec API'}

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        user = User.query.get(user_id) if user_id else None
        return (user_schema.dump(user), 200) if user else ({'error': 'Unauthorized'}, 401)

class Signup(Resource):
    def post(self):
        data = request.get_json()
        try:
            user_data = user_schema.load(data)
            if user_data['password'] != user_data['passwordConfirm']:
                return {'error': 'Passwords do not match'}, 400

            new_user = User(username=user_data['username'], email=user_data['email'], role='client')
            new_user.password_hash = user_data['password']

            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            return user_schema.dump(new_user), 201
        except ValidationError as err:
            return {'error': err.messages}, 400
        except Exception as e:
            return {'error': str(e)}, 402

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data.get('username')).first()
        if not user or not user.authenticate(data.get('password')):
            return {'error': 'Unauthorized login'}, 401
        session['user_id'] = user.id
        return user_schema.dump(user), 200

class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {}, 204

class Users(Resource):
    def get(self):    
        return user_schema.dump(User.query.all(), many=True), 200

class UserByID(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        return (user_schema.dump(user), 200) if user else ({'error': 'User not found'}, 404)

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        db.session.delete(user)
        db.session.commit()
        return {}, 204

class Guitars(Resource):
    def get(self):
        return guitar_schema.dump(UserGuitar.query.all(), many=True), 200
    
    def post(self):
        data = request.get_json()
        try:
            guitar_data = guitar_schema.load(data)
            if UserGuitar.query.filter_by(serial_number=guitar_data['serial_number']).first():
                return {'error': 'Serial number already exists'}, 400
            
            user = User.query.get(guitar_data['user_id'])
            if not user:
                return {'error': 'User not found'}, 404

            model = Model.query.get(guitar_data['model_id'])
            if not model:
                return {'error': 'Model not found'}, 404
            
            new_guitar = UserGuitar(**guitar_data)
            db.session.add(new_guitar)
            db.session.commit()
            return guitar_schema.dump(new_guitar), 201
        except ValidationError as err:
            return {'error': err.messages}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

class GuitarBySN(Resource):
    def get(self, serial_number):
        guitar = UserGuitar.query.filter_by(serial_number=serial_number).first()
        return (guitar_schema.dump(guitar), 200) if guitar else ({'error': 'Guitar not found'}, 404)

    def put(self, serial_number):
        data = request.get_json()
        guitar = UserGuitar.query.filter_by(serial_number=serial_number).first()
        if not guitar:
            return {'error': 'Guitar not found'}, 404
        try:
            guitar_data = guitar_schema.load(data, partial=True)
            for key, value in guitar_data.items():
                setattr(guitar, key, value)
            db.session.commit()
            return guitar_schema.dump(guitar), 200
        except ValidationError as err:
            return {'error': err.messages}, 400
        except Exception as e:
            return {'error': str(e)}, 400

    def delete(self, serial_number):
        guitar = UserGuitar.query.filter_by(serial_number=serial_number).first()
        if not guitar:
            return {'error': 'Guitar not found'}, 404
        db.session.delete(guitar)
        db.session.commit()
        return {}, 204

class Models(Resource):
    def get(self):    
        return model_schema.dump(Model.query.all(), many=True), 200
    
    def post(self):
        data = request.get_json()
        try:
            model_data = model_schema.load(data)
            new_model = Model(**model_data)
            db.session.add(new_model)
            db.session.commit()
            return model_schema.dump(new_model), 201
        except ValidationError as err:
            return {'error': err.messages}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

class ModelByName(Resource):
    def get(self, model_name):
        model_name = model_name.replace("_", " ")
        model = Model.query.filter_by(model_name=model_name).first()
        return (model_schema.dump(model), 200) if model else ({'error': 'Model not found'}, 404)

    def put(self, model_name):
        model_name = model_name.replace("_", " ")
        data = request.get_json()
        model = Model.query.filter_by(model_name=model_name).first()
        if not model:
            return {'error': 'Model not found'}, 404
        try:
            model_data = model_schema.load(data, partial=True)
            for key, value in model_data.items():
                setattr(model, key, value)
            db.session.commit()
            return model_schema.dump(model), 200
        except ValidationError as err:
            return {'error': err.messages}, 400
        except Exception as e:
            return {'error': str(e)}, 400

    def delete(self, model_name):
        model_name = model_name.replace("_", " ")
        model = Model.query.filter_by(model_name=model_name).first()
        if not model:
            return {'error': 'Model not found'}, 404
        db.session.delete(model)
        db.session.commit()
        return {}, 204

class IdentificationForm(Resource):
    def get(self):
        return {
            "brands": Model.get_model_brands(),
            "serial_number_locations": Model.get_model_serial_number_locations(),
            "countries": Model.get_model_countries()
        }, 200

class PhysicalForm(Resource):
    def get(self):
        return {
            "plastic_colors": PlasticColor.get_model_labels(),
            "hardware_finishes": HardwareFinish.get_model_labels()
        }, 200

class BodyForm(Resource):
    def get(self):
        return {
            "body_woods": Body.get_model_woods(),
            "body_colors": Body.get_model_colors(),
            "bridge_models": Bridge.get_model_models(),
            "saddle_styles": Saddles.get_model_styles(),
            "saddle_materials": Saddles.get_model_materials()
        }, 200

class NeckForm(Resource):
    def get(self):
        return {
            "neck_woods": Neck.get_model_woods(),
            "neck_shapes": Neck.get_model_shapes(),
            "headstock_shapes": Headstock.get_model_shapes(),
            "headstock_decals": Headstock.get_model_decals(),
            "fretboard_materials": Fretboard.get_model_materials(),
            "nut_materials": Nut.get_model_materials(),
            "inlay_shapes": Inlays.get_model_shapes(),
            "inlay_materials": Inlays.get_model_materials(),
            "tuner_models": TuningMachine.get_model_models(),
            "string_tree_types": StringTree.get_model_types()
        }, 200

class ElectronicsForm(Resource):
    def get(self):
        return {
            "pickup_types": GuitarPickup.get_model_types(),
            "pickup_magnets": GuitarPickup.get_model_magnets(),
            "pickup_covers": GuitarPickup.get_model_covers(),
            "control_configurations": Controls.get_model_configurations()
        }, 200

api.add_resource(CheckSession, '/api/check_session')
api.add_resource(Signup, '/api/signup')
api.add_resource(Login, '/api/login')
api.add_resource(Logout, '/api/logout')
api.add_resource(Users, '/api/users')
api.add_resource(UserByID, '/api/user/<int:user_id>')
api.add_resource(Guitars, '/api/guitars')
api.add_resource(GuitarBySN, '/api/guitar/<string:serial_number>')
api.add_resource(Models, '/api/models')
api.add_resource(ModelByName, '/api/model/<string:model_name>')

api.add_resource(IdentificationForm, '/api/identification-form')
api.add_resource(PhysicalForm, '/api/physical-form')
api.add_resource(BodyForm, '/api/body-form')
api.add_resource(NeckForm, '/api/neck-form')
api.add_resource(ElectronicsForm, '/api/electronics-form')

if __name__ == '__main__':
    app.run(port=5555, debug=True)