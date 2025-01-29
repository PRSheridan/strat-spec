#!/usr/bin/env python3
from flask import request, session, make_response, send_file
from flask_restful import Resource
from sqlalchemy import or_

from config import app, db, api
from models import User, Image, Guitar, Model

@app.route('/')
def index():
    return '<h1>service-tracker-server</h1>'

#outline of needed classes and methods. Will make many many methods for the search model. 
#last project used frontend for filtering... not good.

class CheckSession(Resource):
    def get(self):
        if session['user_id']:
            user = User.query.filter(User.id == session['user_id']).first().to_dict()
            return user, 200
        
        return {'error': '401 Unauthorized Request'}, 401

class Signup(Resource):
    def post(self):
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        role = "client"
        passwordConfirm = data.get('passwordConfirm')

        if password != passwordConfirm:
            return {'error': '400 Passwords do not match'}, 400

        try:
            user = User(
                username = username,
                email = email,
                role=role
            )

            user.password_hash = password

            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return user.to_dict(), 201
        
        except Exception as e:
            return {'error': str(e)}, 402
        
class Login(Resource):
    def post(self):
        json = request.get_json()
        username = json.get('username')
        password = json.get('password')
        user = User.query.filter(User.username == username).first()

        if user and user.authenticate(password):
            session['user_id'] = user.id
            return make_response(user.to_dict(), 200)
        
        return {'error': '401 Unauthorized login'}, 401
    
class Logout(Resource):
    def delete(self):
        if session['user_id']:
            session['user_id'] = ''
            return {}, 204
        
        return {'error':'401 Unable to process request'}, 401

#Users: list of all users
class Users(Resource):
    def get(self):    
        return [user.to_dict() for user in User.query.all()], 200
    
#UserByID: User dict matching an ID (by ID)
class UserByID(Resource):
    def get(self, user_id):
        if not (user := User.query.filter_by(id=user_id).one_or_none()):
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    def delete(self, user_id):
        if not (user := User.query.filter_by(id=user_id).one_or_none()):
            return {'error': 'User not found'}, 404
        db.session.delete(user)
        db.session.commit()
        return '', 204

#guitars (all)
class Guitars(Resource):
    def get(self):    
        return [guitar.to_dict() for guitar in Guitar.query.all()], 200
    
    def post(self):
        data = request.get_json()

        # Validate attributes: user_id and model_id and ensures unique serial number (serial number WIP)
        user = User.query.filter_by(id=data.get('user_id')).one_or_none()
        if not user:
            return {'error': 'User not found'}, 404

        model = Model.query.filter_by(id=data.get('model_id')).one_or_none()
        if not model:
            return {'error': 'Model not found'}, 404
        
        serial_number = Guitar.query.filter_by(id=data.get('serial_number')).one_or_none()
        if serial_number:
            return {'error': 'Serial number already exists'}, 404

        try:
            new_guitar = Guitar(
                name=data.get('name'),
                description=data.get('description'),
                serial_number=data.get('serial_number'),
                user_id=user.id,
                model_id=model.id
            )

            db.session.add(new_guitar)
            db.session.commit()

            return new_guitar.to_dict(), 201
        
        #look into rollback function
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400


# TicketByID : get, post, delete
class GuitarByID(Resource):
    def get(self, guitar_id):
        if not (guitar := Guitar.query.filter_by(id=guitar_id).one_or_none()):
            return {'error': 'Guitar not found'}, 404
        return guitar.to_dict(), 200

    def put(self, guitar_id):
        if not (guitar := Guitar.query.filter_by(id=guitar_id).one_or_none()):
            return {'error': 'Guitar not found'}, 404
        
        user = User.query.filter_by(id=data.get('user_id')).one_or_none()
        if not user:
            return {'error': 'User not found'}, 404

        model = Model.query.filter_by(id=data.get('model_id')).one_or_none()
        if not model:
            return {'error': 'Model not found'}, 404
        
        serial_number = Guitar.query.filter_by(id=data.get('serial_number')).one_or_none()
        if serial_number:
            return {'error': 'Serial number already exists'}, 404
        
        data = request.get_json()
        try:
            guitar.name = data.get('name', guitar.name),
            guitar.data.get('description', guitar.description),
            guitar.data.get('serial_number', guitar.serial_number),
            guitar.user_id=data.get('user_id', guitar.user_id),
            guitar.model_id=data.get('model.id', guitar.model_id)
            db.session.commit()
            return guitar.to_dict(), 200

        except Exception as e:
            print(str(e)) 
            return {'error': str(e)}, 400

    def delete(self, guitar_id):
        if not (guitar := Guitar.query.filter_by(id=guitar_id).one_or_none()):
            return {'error': 'Guitar not found'}, 404
        
        #removed image handling for now

        db.session.delete(guitar)
        db.session.commit()
        return '', 204

#models (all)
class Models(Resource):
    def get(self):    
        return [models.to_dict() for models in Models.query.all()], 200
    
    def post(self):
        data = request.get_json()

        try:
            new_model = Model(
                name=data.get('name'),
                years=data.get('years'),
                body_id=data.get('body_id'),
                neck_id=data.get('neck_id'),
                fretboard_id=data.get('fretboard_id'),
                nut_id=data.get('nut_id'),
                truss_rod_id=data.get('truss_rod_id'),
                pickups_id=data.get('pickups_id'),
                bridge_id=data.get('bridge_id'),
                tuning_machine_id=data.get('tuning_machine_id'),
                string_tree_id=data.get('string_tree_id'),
                pickguard_id=data.get('pickguard_id'),
                control_knob_id=data.get('control_knob_id'),
                switch_tip_id=data.get('switch_tip_id'),
                neck_plate_id=data.get('neck_plate_id'),
            )

            #need to figure out how to add attributes smoothly.
            #by ID? need to search each model for cooresponding ID?
            #should I modify the Model? is ID tied to dropdowns/searching?

            db.session.add(new_model)
            db.session.commit()

            return new_model.to_dict(), 201
        
        #look into rollback function
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

#models (by ID)

#models (by given data: could be many)

if __name__ == '__main__':
    app.run(port=5555, debug=True)

