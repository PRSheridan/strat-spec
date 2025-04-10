#models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import JSON
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from werkzeug.utils import secure_filename
import re, os, io, zipfile
from datetime import datetime
from config import db, bcrypt, app

user_guitar_images = db.Table(
    'user_guitar_images',
    db.Column('user_guitar_id', db.Integer, db.ForeignKey('user_guitar.id'), primary_key=True),
    db.Column('image_id', db.Integer, db.ForeignKey('image.id'), primary_key=True)
)

model_pickups = db.Table(
    'model_pickups',
    db.Column('model_id', db.Integer, db.ForeignKey('model.id'), primary_key=True),
    db.Column('pickup_id', db.Integer, db.ForeignKey('guitar_pickup.id'), primary_key=True)
)

user_guitar_pickups = db.Table(
    'user_guitar_pickups',
    db.Column('user_guitar_id', db.Integer, db.ForeignKey('user_guitar.id'), primary_key=True),
    db.Column('pickup_id', db.Integer, db.ForeignKey('guitar_pickup.id'), primary_key=True)
)

model_body = db.Table(
    'model_body',
    db.Column('model_id', db.Integer, db.ForeignKey('model.id'), primary_key=True),
    db.Column('body_id', db.Integer, db.ForeignKey('body.id'), primary_key=True)
)

model_fretboard = db.Table(
    'model_fretboard',
    db.Column('model_id', db.Integer, db.ForeignKey('model.id'), primary_key=True),
    db.Column('fretboard_id', db.Integer, db.ForeignKey('fretboard.id'), primary_key=True)
)

model_pickguard = db.Table(
    'model_pickguard',
    db.Column('model_id', db.Integer, db.ForeignKey('model.id'), primary_key=True),
    db.Column('pickguard_id', db.Integer, db.ForeignKey('pickguard.id'), primary_key=True)
)

model_switch = db.Table(
    'model_switch',
    db.Column('model_id', db.Integer, db.ForeignKey('model.id'), primary_key=True),
    db.Column('switch_id', db.Integer, db.ForeignKey('switch.id'), primary_key=True)
)

model_controls = db.Table(
    'model_controls',
    db.Column('model_id', db.Integer, db.ForeignKey('model.id'), primary_key=True),
    db.Column('controls_id', db.Integer, db.ForeignKey('controls.id'), primary_key=True)
)

model_hardware_finish = db.Table(
    'model_hardware_finish',
    db.Column('model_id', db.Integer, db.ForeignKey('model.id'), primary_key=True),
    db.Column('hardware_finish_id', db.Integer, db.ForeignKey('hardware_finish.id'), primary_key=True)
)

model_plastic_color = db.Table(
    'model_plastic_color',
    db.Column('model_id', db.Integer, db.ForeignKey('model.id'), primary_key=True),
    db.Column('plastic_color_id', db.Integer, db.ForeignKey('plastic_color.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(128), unique=True, nullable=False, index=True)
    _password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), nullable=False, default='client')
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to guitars
    user_guitars = db.relationship('UserGuitar', back_populates='owner', cascade='all, delete-orphan')

    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError("Invalid email format")
        return email.lower()

    @validates('role')
    def validate_role(self, key, role):
        if role not in ['client', 'admin']:
            raise ValueError("Role must be either 'client' or 'admin'.")
        return role

    @validates('username')
    def validate_username(self, key, username):
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return username

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes cannot be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, 
            password.encode('utf-8')
        )

    def update_last_login(self):
        self.last_login = datetime.utcnow()
        db.session.commit()

    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.id}, {self.username}>'
    
class Image(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String, nullable=False)
    caption = db.Column(db.String, nullable=True)
    file_path = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user_guitars = db.relationship('UserGuitar', secondary=user_guitar_images, back_populates='images')
    
    def to_dict(self):
        return {
            "id": self.id,
            "file_name": self.file_name,
            "caption": self.caption,
            "file_path": self.file_path
        }
    
    @classmethod
    def save_image(cls, image_file, **kwargs):
        if not image_file or image_file.filename == '':
            return None, 400, "No selected file"
            
        filename = secure_filename(image_file.filename)
        if not filename:
            return None, 400, "File type not supported"
            
        try:
            # Save the file to your configured upload path
            upload_path = app.config["UPLOAD_PATH"]
            
            # Make sure directory exists
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
                
            # Save the file
            file_path = os.path.join(upload_path, filename)
            image_file.save(file_path)
            
            # Create a new Image object
            new_image = cls(
                file_name=filename,
                file_path=file_path,
                **kwargs
            )
            
            # Add and commit to database
            db.session.add(new_image)
            db.session.commit()
            
            return new_image, 201, "Image saved successfully"
            
        except Exception as e:
            db.session.rollback()
            return None, 500, f"Error saving image: {str(e)}"

# Model Model
class Model(db.Model):
    __tablename__ = 'model'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    model_name = db.Column(db.String(100), nullable=False)
    year_range = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String, nullable=True)
    scale_length = db.Column(db.Float, nullable=False)
    relic = db.Column(db.String(50), nullable=False)
    other_controls = db.Column(JSON, nullable=True)
    pickup_configuration = db.Column(JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Many-to-Many Relationships (Variations)
    pickups = db.relationship('GuitarPickup', secondary='model_pickups', back_populates='models')
    bodies = db.relationship('Body', secondary='model_body', back_populates='models')
    fretboards = db.relationship('Fretboard', secondary='model_fretboard', back_populates='models')
    pickguards = db.relationship('Pickguard', secondary='model_pickguard', back_populates='models')
    switches = db.relationship('Switch', secondary='model_switch', back_populates='models')
    controls = db.relationship('Controls', secondary='model_controls', back_populates='models')
    hardware_finish = db.relationship('HardwareFinish', secondary='model_hardware_finish', back_populates='models')
    plastic_color = db.relationship('PlasticColor', secondary='model_plastic_color', back_populates='models')


    # Many-to-One Relationships (Fixed parts of the model)
    neck_id = db.Column(db.Integer, db.ForeignKey('neck.id'), nullable=False)
    neck = db.relationship('Neck', back_populates='models')

    headstock_id = db.Column(db.Integer, db.ForeignKey('headstock.id'), nullable=False)
    headstock = db.relationship('Headstock', back_populates='models')

    nut_id = db.Column(db.Integer, db.ForeignKey('nut.id'), nullable=False)
    nut = db.relationship('Nut', back_populates='models')

    frets_id = db.Column(db.Integer, db.ForeignKey('frets.id'), nullable=False)
    frets = db.relationship('Frets', back_populates='models')

    inlays_id = db.Column(db.Integer, db.ForeignKey('inlays.id'), nullable=False)
    inlays = db.relationship('Inlays', back_populates='models')

    bridge_id = db.Column(db.Integer, db.ForeignKey('bridge.id'), nullable=False)
    bridge = db.relationship('Bridge', back_populates='models')

    saddles_id = db.Column(db.Integer, db.ForeignKey('saddles.id'), nullable=False)
    saddles = db.relationship('Saddles', back_populates='models')

    tuning_machine_id = db.Column(db.Integer, db.ForeignKey('tuning_machine.id'), nullable=False)
    tuning_machine = db.relationship('TuningMachine', back_populates='models')

    string_tree_id = db.Column(db.Integer, db.ForeignKey('string_tree.id'), nullable=False)
    string_tree = db.relationship('StringTree', back_populates='models')

    neck_plate_id = db.Column(db.Integer, db.ForeignKey('neck_plate.id'), nullable=False)
    neck_plate = db.relationship('NeckPlate', back_populates='models')

    # One-to-Many: Model → UserGuitar
    user_guitars = db.relationship('UserGuitar', back_populates='model', lazy=True)

    # Field validations
    @validates('brand')
    def validate_brand(self, key, brand):
        if not brand or len(brand.strip()) == 0:
            raise ValueError("Brand cannot be empty")
        return brand

    @validates('model_name')
    def validate_model_name(self, key, model_name):
        if not model_name or len(model_name.strip()) == 0:
            raise ValueError("Model name cannot be empty")
        return model_name

    @validates('year_range')
    def validate_year_range(self, key, year_range):
        # Validate format like "1954-1957" or "1965-present"
        pattern = r'^\d{4}-(\d{4}|present)$'
        if not re.match(pattern, year_range):
            raise ValueError("Year range must be in format 'YYYY-YYYY' or 'YYYY-present'")
        return year_range

    @validates('country')
    def validate_country(self, key, country):
        # List of countries where Stratocasters are manufactured
        valid_countries = ['USA', 'Mexico', 'Japan', 'China', 'Indonesia', 'Korea', 'Custom'] 
        
        if country not in valid_countries:
            raise ValueError(f"Country must be a valid Stratocaster manufacturing location: {', '.join(valid_countries)}")
        return country

    @validates('scale_length')
    def validate_scale_length(self, key, scale_length):
        if not 20.0 <= scale_length <= 30.0:
            raise ValueError("Scale length must be between 20.0 and 30.0 inches")
        return scale_length

    @validates('relic')
    def validate_relic(self, key, relic):
        valid_options = ['None', 'Light', 'Medium', 'Heavy', 'Custom']
        if relic not in valid_options:
            raise ValueError(f"Relic must be one of: {', '.join(valid_options)}")
        return relic


class UserGuitar(db.Model):
    __tablename__ = 'user_guitar'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    serial_number = db.Column(db.String, nullable=False)
    serial_number_location = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=True)
    country = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    scale_length = db.Column(db.Float, nullable=True)
    weight = db.Column(db.String, nullable=True)
    relic = db.Column(db.String, nullable=False)
    other_controls = db.Column(db.String, nullable=True)
    pickup_configuration = db.Column(db.String, nullable=False)
    modified = db.Column(db.Boolean, default=True)
    modifications = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    pickups = db.relationship('GuitarPickup', secondary=user_guitar_pickups, back_populates='user_guitars')
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'), nullable=True)
    model = db.relationship('Model', back_populates='user_guitars')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', back_populates='user_guitars')
    images = db.relationship('Image', secondary='user_guitar_images', back_populates='user_guitars')
    
    # Relationships to components
    body_id = db.Column(db.Integer, db.ForeignKey('body.id'))
    body = db.relationship('Body', back_populates='user_guitars')

    neck_id = db.Column(db.Integer, db.ForeignKey('neck.id'))
    neck = db.relationship('Neck', back_populates='user_guitars')

    headstock_id = db.Column(db.Integer, db.ForeignKey('headstock.id'))
    headstock = db.relationship('Headstock', back_populates='user_guitars')

    fretboard_id = db.Column(db.Integer, db.ForeignKey('fretboard.id'))
    fretboard = db.relationship('Fretboard', back_populates='user_guitars')

    nut_id = db.Column(db.Integer, db.ForeignKey('nut.id'))
    nut = db.relationship('Nut', back_populates='user_guitars')

    frets_id = db.Column(db.Integer, db.ForeignKey('frets.id'))
    frets = db.relationship('Frets', back_populates='user_guitars')

    inlays_id = db.Column(db.Integer, db.ForeignKey('inlays.id'))
    inlays = db.relationship('Inlays', back_populates='user_guitars')

    bridge_id = db.Column(db.Integer, db.ForeignKey('bridge.id'))
    bridge = db.relationship('Bridge', back_populates='user_guitars')

    saddles_id = db.Column(db.Integer, db.ForeignKey('saddles.id'))
    saddles = db.relationship('Saddles', back_populates='user_guitars')

    switch_id = db.Column(db.Integer, db.ForeignKey('switch.id'))
    switch = db.relationship('Switch', back_populates='user_guitars')

    controls_id = db.Column(db.Integer, db.ForeignKey('controls.id'))
    controls = db.relationship('Controls', back_populates='user_guitars')

    tuning_machine_id = db.Column(db.Integer, db.ForeignKey('tuning_machine.id'))
    tuning_machine = db.relationship('TuningMachine', back_populates='user_guitars')

    string_tree_id = db.Column(db.Integer, db.ForeignKey('string_tree.id'))
    string_tree = db.relationship('StringTree', back_populates='user_guitars')

    neck_plate_id = db.Column(db.Integer, db.ForeignKey('neck_plate.id'))
    neck_plate = db.relationship('NeckPlate', back_populates='user_guitars')

    pickguard_id = db.Column(db.Integer, db.ForeignKey('pickguard.id'))
    pickguard = db.relationship('Pickguard', back_populates='user_guitars')

    hardware_finish_id = db.Column(db.Integer, db.ForeignKey('hardware_finish.id'))
    hardware_finish = db.relationship('HardwareFinish', back_populates='user_guitars')

    plastic_color_id = db.Column(db.Integer, db.ForeignKey('plastic_color.id'))
    plastic_color = db.relationship('PlasticColor', back_populates='user_guitars')

    def __init__(self, *args, **kwargs):
        """Set name to model name if unmodified and model exists upon creation."""
        super().__init__(*args, **kwargs)
        self.sync_name_with_model()

    @validates('serial_number')
    def validate_serial_number(self, key, value):
        # Strip whitespace and validate minimum length
        value = value.strip()
        if len(value) < 3:  # Adjust minimum length as needed
            raise ValueError("Serial number must be at least 3 characters")
        return value

    @validates('year')
    def validate_year(self, key, year):
        if year is not None:
            current_year = datetime.utcnow().year
            if not (1930 <= year <= current_year):
                raise ValueError(f"Year must be between 1930 and {current_year}")
        return year

    @validates('country')
    def validate_country(self, key, value):
        valid_countries = ['USA', 'Mexico', 'Japan', 'China', 'Indonesia', 'Korea', 'Custom']  # Add others as needed
        if value not in valid_countries:
            raise ValueError(f"Country must be one of: {', '.join(valid_countries)}")
        return value

    def sync_name_with_model(self):
        """Update the name to the model's name if it hasn't been modified."""
        if not self.modified and self.model and self.name != self.model.model_name:
            self.name = self.model.model_name
            db.session.add(self)

    @property
    def display_name(self):
        """Returns the model's name if unmodified, otherwise the guitar's name."""
        return self.model.model_name if not self.modified and self.model else self.name or "Unnamed Guitar"


# Guitar Attributes
class GuitarPickup(db.Model):
    __tablename__ = "guitar_pickup"

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String, nullable=True)
    model = db.Column(db.String, nullable=True)
    position = db.Column(JSON, nullable=False)
    type = db.Column(db.String, nullable=False)
    magnet = db.Column(db.String, nullable=True)
    active = db.Column(db.Boolean, nullable=True)
    noiseless = db.Column(db.Boolean, nullable=True)
    cover = db.Column(db.String, nullable=True)

    # Relationships
    models = db.relationship('Model', secondary='model_pickups', back_populates='pickups')
    user_guitars = db.relationship('UserGuitar', secondary='user_guitar_pickups', back_populates='pickups')
    
    @validates('type')
    def validate_type(self, key, type_val):
        valid_types = [
            'Single-coil', 'Humbucker', 'Hot Rails', 'Noiseless', 'Lace Sensor',
            'P90', 'Mini-humbucker', 'Lipstick', 'Rail', 'Other'
        ]
        if type_val not in valid_types:
            raise ValueError(f"Pickup type must be one of: {', '.join(valid_types)}")
        return type_val
    
    @validates('magnet')
    def validate_magnet(self, key, magnet):
        if magnet is not None:
            valid_magnets = ['Alnico II', 'Alnico III', 'Alnico IV', 'Alnico V', 
                          'Ceramic', 'Neodymium', 'Other']
            if magnet not in valid_magnets:
                raise ValueError(f"Magnet type must be one of: {', '.join(valid_magnets)}")
        return magnet
    
    @validates('cover')
    def validate_cover(self, key, cover):
        if cover is not None:
            valid_covers = ['None', 'Chrome', 'Nickel', 'Gold', 'Black', 'Cream', 'Zebra', 'Other']
            if cover not in valid_covers:
                raise ValueError(f"Cover must be one of: {', '.join(valid_covers)}")
        return cover

# Body Model
class Body(db.Model):
    __tablename__ = 'body'

    id = db.Column(db.Integer, primary_key=True)
    wood = db.Column(db.String, nullable=True)
    contour = db.Column(db.String, nullable=True)
    routing = db.Column(db.String, nullable=True)
    chambering = db.Column(db.Boolean, nullable=True)
    binding = db.Column(db.Boolean, nullable=False)
    finish = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', secondary='model_body', back_populates='bodies')
    user_guitars = db.relationship('UserGuitar', back_populates='body')
    
    @validates('wood')
    def validate_wood(self, key, wood):
        if wood is not None:
            valid_woods = ['Alder', 'Ash', 'Basswood', 'Mahogany', 'Poplar', 'Pine', 
                           'Maple', 'Korina', 'Walnut', 'Other']
            if wood not in valid_woods:
                raise ValueError(f"Body wood must be one of: {', '.join(valid_woods)}")
        return wood
    
    @validates('contour')
    def validate_contour(self, key, contour):
        if contour is not None:
            valid_contours = ['Shallow', 'Deep']
            if contour not in valid_contours:
                raise ValueError(f"Body contour must be one of: {', '.join(valid_contours)}")
        return contour
    
    @validates('routing')
    def validate_routing(self, key, routing):
        if routing is not None:
            valid_routings = ['Standard', 'HH', 'HSH', 'HSS', 'SSS', 'HS', 'S', 'H', 'Other']
            if routing not in valid_routings:
                raise ValueError(f"Routing must be one of: {', '.join(valid_routings)}")
        return routing
    
    @validates('finish')
    def validate_finish(self, key, finish):
        valid_finishes = ['Nitrocellulose', 'Polyurethane', 'Other']
        if finish not in valid_finishes:
            raise ValueError(f"Finish must be one of: {', '.join(valid_finishes)}")
        return finish

# Neck Model
class Neck(db.Model):
    __tablename__ = 'neck'

    id = db.Column(db.Integer, primary_key=True)
    wood = db.Column(db.String, nullable=True)
    finish = db.Column(db.String, nullable=False)
    shape = db.Column(db.String, nullable=True)
    truss_rod = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='neck')
    user_guitars = db.relationship('UserGuitar', back_populates='neck')
    
    @validates('wood')
    def validate_wood(self, key, wood):
        if wood is not None:
            valid_woods = ['Maple', 'Mahogany', 'Roasted Maple', 'Flame Maple', 'Other']
            if wood not in valid_woods:
                raise ValueError(f"Neck wood must be one of: {', '.join(valid_woods)}")
        return wood
    
    @validates('finish')
    def validate_finish(self, key, finish):
        valid_finishes = ['Gloss', 'Satin', 'Natural']
        if finish not in valid_finishes:
            raise ValueError(f"Neck finish must be one of: {', '.join(valid_finishes)}")
        return finish
    
    @validates('truss_rod')
    def validate_truss_rod(self, key, truss_rod):
        if truss_rod is not None:
            valid_types = ['Modern', 'Vintage']
            if truss_rod not in valid_types:
                raise ValueError(f"Truss rod location must be one of: {', '.join(valid_types)}")
        return truss_rod

# Headstock Model
class Headstock(db.Model):
    __tablename__ = 'headstock'

    id = db.Column(db.Integer, primary_key=True)
    shape = db.Column(db.String, nullable=True)
    decal_style = db.Column(db.String, nullable=True)
    reverse = db.Column(db.Boolean, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='headstock')
    user_guitars = db.relationship('UserGuitar', back_populates='headstock')
    
    @validates('decal_style')
    def validate_decal_style(self, key, style):
        if style is not None:
            valid_styles = ['Vintage', 'Modern', 'Spaghetti Logo', 'CBS Logo', 'Block', 'None', 'Other']
            if style not in valid_styles:
                raise ValueError(f"Decal style must be one of: {', '.join(valid_styles)}")
        return style

# Fretboard Model
class Fretboard(db.Model):
    __tablename__ = 'fretboard'

    id = db.Column(db.Integer, primary_key=True)
    material = db.Column(db.String, nullable=True)
    radius = db.Column(db.String, nullable=True)
    fret_count = db.Column(db.Integer, nullable=False)
    binding = db.Column(db.Boolean, nullable=False)
    scalloped = db.Column(db.Boolean, nullable=False)

    # Relationships
    models = db.relationship('Model', secondary='model_fretboard', back_populates='fretboards')
    user_guitars = db.relationship('UserGuitar', back_populates='fretboard')
    
    @validates('material')
    def validate_material(self, key, material):
        valid_materials = ['Maple', 'Rosewood', 'Ebony', 'Pau Ferro', 'Richlite', 'Walnut', 
                         'Laurel', 'Wenge', 'Other']
        if material not in valid_materials:
            raise ValueError(f"Fretboard material must be one of: {', '.join(valid_materials)}")
        return material
    
    @validates('radius')
    def validate_radius(self, key, radius):
        if radius is not None:
            try:
                radius_value = float(radius.rstrip('"'))
                if not 5.0 <= radius_value <= 25.0:
                    raise ValueError("Fretboard radius must be between 5.0 and 25.0 inches")
            except (ValueError, AttributeError):
                if radius != "Compound":
                    raise ValueError("Fretboard radius must be a number between 5.0 and 25.0 inches or 'Compound'")
        return radius
    
    @validates('fret_count')
    def validate_fret_count(self, key, count):
        if not 19 <= count <= 36:
            raise ValueError("Fret count must be between 19 and 36")
        return count

# Frets Model
class Frets(db.Model):
    __tablename__ = 'frets'

    id = db.Column(db.Integer, primary_key=True)
    material = db.Column(db.String, nullable=True)
    size = db.Column(db.String, nullable=True)

    # Relationships
    models = db.relationship('Model', back_populates='frets')
    user_guitars = db.relationship('UserGuitar', back_populates='frets')
    
    @validates('material')
    def validate_material(self, key, material):
        if material is not None:
            valid_materials = ['Nickel', 'Stainless Steel', 'Other']
            if material not in valid_materials:
                raise ValueError(f"Fret material must be one of: {', '.join(valid_materials)}")
        return material
    
    @validates('size')
    def validate_size(self, key, size):
        if size is not None:
            valid_sizes = ['Vintage', 'Medium', 'Jumbo', 'Medium Jumbo', 'Narrow Tall', 'Other']
            if size not in valid_sizes:
                raise ValueError(f"Fret size must be one of: {', '.join(valid_sizes)}")
        return size

# Nut Model
class Nut(db.Model):
    __tablename__ = 'nut'

    id = db.Column(db.Integer, primary_key=True)
    width = db.Column(db.String, nullable=True)
    material = db.Column(db.String, nullable=True)
    locking = db.Column(db.Boolean, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='nut')
    user_guitars = db.relationship('UserGuitar', back_populates='nut')
    
    @validates('width')
    def validate_width(self, key, width):
        if width is not None:
            try:
                width_value = float(width.rstrip('"'))
                if not 1.5 <= width_value <= 2.0:
                    raise ValueError("Nut width must be between 1.5 and 2.0 inches")
            except (ValueError, AttributeError):
                raise ValueError("Nut width must be a number between 1.5 and 2.0 inches")
        return width
    
    @validates('material')
    def validate_material(self, key, material):
        if material is not None:
            valid_materials = ['Bone', 'Plastic', 'Graphite', 'Brass', 'Tusq', 'Other']
            if material not in valid_materials:
                raise ValueError(f"Nut material must be one of: {', '.join(valid_materials)}")
        return material

# Inlays Model
class Inlays(db.Model):
    __tablename__ = 'inlays'

    id = db.Column(db.Integer, primary_key=True)
    shape = db.Column(db.String, nullable=True)
    material = db.Column(db.String, nullable=True)
    spacing = db.Column(db.String, nullable=True)

    # Relationships
    models = db.relationship('Model', back_populates='inlays')
    user_guitars = db.relationship('UserGuitar', back_populates='inlays')
    
    @validates('shape')
    def validate_shape(self, key, shape):
        if shape is not None:
            valid_shapes = ['Dot', 'Block', 'Shark Fin', 'Trapezoid', 'Bird', 'None', 'Other']
            if shape not in valid_shapes:
                raise ValueError(f"Inlay shape must be one of: {', '.join(valid_shapes)}")
        return shape
    
    @validates('material')
    def validate_material(self, key, material):
        if material is not None:
            valid_materials = ['Pearloid', 'Mother of Pearl', 'Abalone', 'Acrylic', 'Stone', 'Plastic', 'None', 'Other']
            if material not in valid_materials:
                raise ValueError(f"Inlay material must be one of: {', '.join(valid_materials)}")
        return material
    
    @validates('spacing')
    def validate_spacing(self, key, spacing):
        if spacing is not None:
            if self.shape == 'Dot':
                valid_spacings = ['Modern', 'Vintage']
                if spacing not in valid_spacings:
                    raise ValueError(f"Dot inlay spacing must be one of: {', '.join(valid_spacings)}")
            else:
                return None
        return spacing

# Bridge Model
class Bridge(db.Model):
    __tablename__ = 'bridge'

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String, nullable=True)
    screws = db.Column(db.Integer, nullable=False)
    spacing = db.Column(db.Integer, nullable=True)
    tremolo = db.Column(db.Boolean, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='bridge')
    user_guitars = db.relationship('UserGuitar', back_populates='bridge')
    
    @validates('screws')
    def validate_screws(self, key, screws):
        if not 2 <= screws <= 6:
            raise ValueError("Bridge screw count must be between 2 and 6")
        return screws

# Saddles Model
class Saddles(db.Model):
    __tablename__ = 'saddles'

    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String, nullable=True)
    material = db.Column(db.String, nullable=True)

    # Relationships
    models = db.relationship('Model', back_populates='saddles')
    user_guitars = db.relationship('UserGuitar', back_populates='saddles')
    
    @validates('style')
    def validate_style(self, key, style):
        valid_styles = ['Vintage', 'Modern', 'Block', 'Roller', 'Compensated', 'Graphtech', 'Other']
        if style not in valid_styles:
            raise ValueError(f"Saddle style must be one of: {', '.join(valid_styles)}")
        return style
    
    @validates('material')
    def validate_material(self, key, material):
        if material is not None:
            valid_materials = ['Steel', 'Brass', 'Graphite', 'Titanium', 'Chrome', 'Nickel', 'Other']
            if material not in valid_materials:
                raise ValueError(f"Saddle material must be one of: {', '.join(valid_materials)}")
        return material

# Switch Model
class Switch(db.Model):
    __tablename__ = 'switch'

    id = db.Column(db.Integer, primary_key=True)
    positions = db.Column(db.Integer, nullable=False)

    # Relationships
    models = db.relationship('Model', secondary='model_switch', back_populates='switches')
    user_guitars = db.relationship('UserGuitar', back_populates='switch')
    
    @validates('positions')
    def validate_positions(self, key, positions):
        if not 2 <= positions <= 7:
            raise ValueError("Switch positions must be between 2 and 7")
        return positions

# Controls Model
class Controls(db.Model):
    __tablename__ = 'controls'

    id = db.Column(db.Integer, primary_key=True)
    configuration = db.Column(db.String, nullable=False)

    # Relationships
    models = db.relationship('Model', secondary='model_controls', back_populates='controls')
    user_guitars = db.relationship('UserGuitar', back_populates='controls')

# Tuning Machine Model
class TuningMachine(db.Model):
    __tablename__ = 'tuning_machine'

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String, nullable=True)
    locking = db.Column(db.Boolean, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='tuning_machine')
    user_guitars = db.relationship('UserGuitar', back_populates='tuning_machine')
    
    @validates('model')
    def validate_model(self, key, model):
        if model is not None:
            valid_models = ['Vintage', 'Modern', 'Locking', 'Kluson', 'Gotoh', 'Grover', 
                           'Sperzel', 'Hipshot', 'Schaller', 'Other']
            if model not in valid_models:
                raise ValueError(f"Tuning machine model must be one of: {', '.join(valid_models)}")
        return model

# String Tree Model
class StringTree(db.Model):
    __tablename__ = 'string_tree'

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String, nullable=True)
    count = db.Column(db.Integer, nullable=False)

    # Relationships
    models = db.relationship('Model', back_populates='string_tree')
    user_guitars = db.relationship('UserGuitar', back_populates='string_tree')
    
    @validates('count')
    def validate_count(self, key, count):
        if not 0 <= count <= 4:
            raise ValueError("String tree count must be between 0 and 4")
        return count
    
    @validates('model')
    def validate_model(self, key, model):
        if model is not None:
            valid_models = ['Vintage', 'Modern', 'Butterfly', 'Disc', 'None', 'Other']
            if model not in valid_models:
                raise ValueError(f"String tree model must be one of: {', '.join(valid_models)}")
        return model

# Neck Plate Model
class NeckPlate(db.Model):
    __tablename__ = 'neck_plate'

    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String, nullable=False)
    bolts = db.Column(db.Integer, nullable=False)
    details = db.Column(db.String, nullable=True)

    # Relationships
    models = db.relationship('Model', back_populates='neck_plate')
    user_guitars = db.relationship('UserGuitar', back_populates='neck_plate')
    
    @validates('bolts')
    def validate_bolts(self, key, bolts):
        if bolts not in [3, 4, 5, 6]:
            raise ValueError("Neck plate bolt count must be 3, 4, 5, or 6")
        return bolts
    
    @validates('style')
    def validate_style(self, key, style):
        valid_styles = ['Vintage', 'Contour']
        if style not in valid_styles:
            raise ValueError(f"Neck plate style must be one of: {', '.join(valid_styles)}")
        return style
    
    @validates('details')
    def validate_details(self, key, details):
        if details is not None:
            valid_details = ['Serial Number', 'F Logo', 'Anniversary', 'Other']
            if details not in valid_details:
                raise ValueError(f"Neck plate details must be one of: {', '.join(valid_details)}")
        return details

# Pickguard Model
class Pickguard(db.Model):
    __tablename__ = 'pickguard'

    id = db.Column(db.Integer, primary_key=True)
    ply_count = db.Column(db.Integer, nullable=True)
    screws = db.Column(db.Integer, nullable=False)

    # Relationships
    models = db.relationship('Model', secondary='model_pickguard', back_populates='pickguards')
    user_guitars = db.relationship('UserGuitar', back_populates='pickguard')
    
    @validates('screws')
    def validate_screws(self, key, screws):
        if not 6 <= screws <= 13:
            raise ValueError("Pickguard screw count must be between 6 and 13")
        return screws
    
    @validates('ply_count')
    def validate_ply_count(self, key, ply_count):
        if ply_count is not None and ply_count not in [1, 2, 3, 4, 5]:
            raise ValueError("Pickguard ply count must be 1, 2, 3, 4, or 5")
        return ply_count
    
class HardwareFinish(db.Model):
    __tablename__ = 'hardware_finish'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50), nullable=False, unique=True)

    user_guitars = db.relationship('UserGuitar', back_populates='hardware_finish')
    models = db.relationship('Model', secondary='model_hardware_finish', back_populates='hardware_finish')

    @validates('label')
    def validate_label(self, key, value):
        if value not in ['Chrome', 'Nickel', 'Gold', 'Black', 'Brushed', 'Cosmo Black', 'Aged Chrome', 'Raw Steel', 'Relic Nickel']:
            raise ValueError(f"'{value}' is not a recognized hardware finish")
        return value
    
class PlasticColor(db.Model):
    __tablename__ = 'plastic_color'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50), nullable=False, unique=True)

    user_guitars = db.relationship('UserGuitar', back_populates='plastic_color')
    models = db.relationship('Model', secondary='model_plastic_color', back_populates='plastic_color')

    @validates('label')
    def validate_label(self, key, value):
        if value not in ['White', 'Black', 'Parchment', 'Mint Green', 'Aged White', 'Cream', 'Pearloid', 'Tortoiseshell', 'Anodized Gold', 'Gray', 'Ivory', 'Custom']:
            raise ValueError(f"'{value}' is not a recognized plastic color")
        return value
