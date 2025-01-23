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

#check session

#signup

#login

#logout

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
        
        data = request.get_json()
        try:
            guitar.requestor_id = data.get('requestor_id', ticket.requestor_id)
            ticket.email = data.get('email', ticket.email)
            ticket.phone = data.get('phone', ticket.phone)
            ticket.title = data.get('title', ticket.title)
            ticket.description = data.get('description', ticket.description)
            ticket.priority = data.get('priority', ticket.priority)
            ticket.status = data.get('status', ticket.status)
            db.session.commit()
            return ticket.to_dict(), 200

        except Exception as e:
            print(str(e)) 
            return {'error': str(e)}, 400

    def delete(self, ticket_id):
        ticket = Ticket.query.filter(Ticket.id == ticket_id).one_or_none()
        if ticket is None:
            return {'error': 'Ticket not found'}, 404
        
        for image in ticket.images:
            file_path = os.path.join(app.config["UPLOAD_PATH"], image.file_path)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except OSError as e:
                    return {'error': f'Error deleting file: {e}'}, 500

        db.session.delete(ticket)
        db.session.commit()
        return '', 204

#guitar (by ID)

#models (all)

#models (by ID)

#models (by year, wood, pickups fretboard...)

if __name__ == '__main__':
    app.run(port=5555, debug=True)

