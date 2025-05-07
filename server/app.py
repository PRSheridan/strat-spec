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
    
# --- Identification Form ---

class Brands(Resource):
    def get(self):
        brands = db.session.query(Model.brand).distinct().all()
        return [b[0] for b in brands if b[0]]

class SerialNumberLocations(Resource):
    def get(self):
        locations = db.session.query(Model.serial_number_location).distinct().all()
        return [l[0] for l in locations if l[0]]

class Countries(Resource):
    def get(self):
        countries = db.session.query(Model.country).distinct().all()
        return [c[0] for c in countries if c[0]]

# --- Body ---

class BodyWoods(Resource):
    def get(self):
        woods = db.session.query(Body.wood).join(Model.bodies).distinct().all()
        return [w[0] for w in woods if w[0]]

class BodyColors(Resource):
    def get(self):
        colors = db.session.query(Body.color).join(Model.bodies).distinct().all()
        return [c[0] for c in colors if c[0]]

# --- Bridge & Saddles ---

class BridgeModels(Resource):
    def get(self):
        models = db.session.query(Bridge.model).join(Model.bridge).distinct().all()
        return [m[0] for m in models if m[0]]

class SaddleStyles(Resource):
    def get(self):
        styles = db.session.query(Saddle.style).join(Model.saddles).distinct().all()
        return [s[0] for s in styles if s[0]]

class SaddleMaterials(Resource):
    def get(self):
        materials = db.session.query(Saddle.material).join(Model.saddles).distinct().all()
        return [m[0] for m in materials if m[0]]

# --- Neck & Headstock ---

class NeckWoods(Resource):
    def get(self):
        woods = db.session.query(Neck.wood).join(Model.neck).distinct().all()
        return [w[0] for w in woods if w[0]]

class NeckShapes(Resource):
    def get(self):
        shapes = db.session.query(Neck.shape).join(Model.neck).distinct().all()
        return [s[0] for s in shapes if s[0]]

class HeadstockShapes(Resource):
    def get(self):
        shapes = db.session.query(Headstock.shape).join(Model.headstock).distinct().all()
        return [s[0] for s in shapes if s[0]]

class HeadstockDecals(Resource):
    def get(self):
        decals = db.session.query(Headstock.decal_style).join(Model.headstock).distinct().all()
        return [d[0] for d in decals if d[0]]

# --- Fretboard / Frets / Nut ---

class FretboardMaterials(Resource):
    def get(self):
        materials = db.session.query(Fretboard.material).join(Model.fretboards).distinct().all()
        return [m[0] for m in materials if m[0]]

class NutMaterials(Resource):
    def get(self):
        materials = db.session.query(Nut.material).join(Model.nut).distinct().all()
        return [m[0] for m in materials if m[0]]

class InlayShapes(Resource):
    def get(self):
        shapes = db.session.query(Inlays.shape).join(Model.inlays).distinct().all()
        return [s[0] for s in shapes if s[0]]

class InlayMaterials(Resource):
    def get(self):
        materials = db.session.query(Inlays.material).join(Model.inlays).distinct().all()
        return [m[0] for m in materials if m[0]]

# --- Hardware ---

class TunerModels(Resource):
    def get(self):
        models = db.session.query(TuningMachine.model).join(Model.tuning_machine).distinct().all()
        return [m[0] for m in models if m[0]]

class StringTreeTypes(Resource):
    def get(self):
        types = db.session.query(StringTree.model).join(Model.string_tree).distinct().all()
        return [t[0] for t in types if t[0]]

class HardwareFinishes(Resource):
    def get(self):
        finishes = db.session.query(HardwareFinish.label).join(Model.hardware_finish).distinct().all()
        return [f[0] for f in finishes if f[0]]

class PlasticColors(Resource):
    def get(self):
        colors = db.session.query(PlasticColor.label).join(Model.plastic_color).distinct().all()
        return [c[0] for c in colors if c[0]]

# --- Electronics ---

class PickupTypes(Resource):
    def get(self):
        types = db.session.query(GuitarPickup.type).join(Model.pickups).distinct().all()
        return [t[0] for t in types if t[0]]

class PickupMagnets(Resource):
    def get(self):
        magnets = db.session.query(GuitarPickup.magnet).join(Model.pickups).distinct().all()
        return [m[0] for m in magnets if m[0]]

class PickupCovers(Resource):
    def get(self):
        covers = db.session.query(GuitarPickup.cover).join(Model.pickups).distinct().all()
        return [c[0] for c in covers if c[0]]

class ControlConfigurations(Resource):
    def get(self):
        configs = db.session.query(Controls.configuration).join(Model.controls).distinct().all()
        return [c[0] for c in configs if c[0]]

class IdentificationForm(Resource):
    def get(self):
      brand_list = Brands.get(self)
      location_list = SerialNumberLocations.get(self)
      country_list = Countries.get(self)

      print(country_list[0])

      return {
          "brands": brand_list[0],
          "serial_number_locations": location_list[0],
          "countries": country_list[0]
      }, 200


class PhysicalForm(Resource):
    def get(self):
        #plastic color
        #hardware color
        pass

class BodyForm(Resource):
    #body wood
    #body color
    #bridge model
    #saddle style
    #saddle material
    pass

class NeckForm(Resource):
    # neck wood
    # neck shape
    # headstock shape
    # headstock decal
    # fretboard material
    # nut material
    # inlay shape
    # inlay material
    # tuner model
    # string tree type
    pass

class ElectronicsForm(Resource):
    # pickup type
    # pickup magnet
    # pickup cover
    # control configuration
    pass


#specific guitar parts for GuitarForm to be replaced by form page specific requests
class Countries(Resource):
    def get(self):
        countries = db.session.query(UserGuitar.country).distinct().all()
        country_list = [country[0] for country in countries]  # Extract values from tuples
        return country_list, 200
    
class SerialNumberLocations(Resource):
    def get(self):
        locations = db.session.query(UserGuitar.serial_number_location).distinct().all()
        location_list = [location[0] for location in locations]  # Extract values from tuples
        return location_list, 200
    
class Brands(Resource):
    def get(self):
        brands = db.session.query(UserGuitar.brand).distinct().all()
        brand_list = [brand[0] for brand in brands]  # Extract values from tuples
        return brand_list, 200

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
api.add_resource(Countries, '/api/countries')
api.add_resource(SerialNumberLocations, '/api/serial-number-locations')
api.add_resource(Brands, '/api/brands')

api.add_resource(PickupCovers, '/api/pickup_covers')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

  #rework all resources. groups for specific form pages calling individual functions




