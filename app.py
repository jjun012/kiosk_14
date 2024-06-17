from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///motel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

db = SQLAlchemy(app)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    info = db.Column(db.String(1000), nullable=False)
    max_people_num = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    amenities = db.Column(db.String(1000), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    photo = db.Column(db.String(100), nullable=True)
    keys = db.relationship("Key", back_populates="room")
    scheduled_rooms = db.relationship("Scheduled_room", back_populates="room")

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String(100), nullable=True)
    scheduled_room_options = db.relationship("Scheduled_room_option", back_populates="option")

class Key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"))
    room = db.relationship("Room", back_populates="keys")
    scheduled_rooms = db.relationship("Scheduled_room", back_populates="key")

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime(timezone=True), server_default=func.now())
    scheduled_rooms = db.relationship("Scheduled_room", back_populates="payment")
    scheduled_room_options = db.relationship("Scheduled_room_option", back_populates="payment")

class Scheduled_room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scheduled_code = db.Column(db.String(20), nullable=False)
    scheduled_name = db.Column(db.String(20), nullable=False)
    scheduled_phone = db.Column(db.String(20), nullable=False)
    scheduled_people_num = db.Column(db.Integer, nullable=False)
    check_in_time = db.Column(db.DateTime(timezone=True))
    check_out_time = db.Column(db.DateTime(timezone=True))
    price = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"))
    room = db.relationship("Room", back_populates="scheduled_rooms")
    key_id = db.Column(db.Integer, db.ForeignKey("key.id"))
    key = db.relationship("Key", back_populates="scheduled_rooms")
    payment_id = db.Column(db.Integer, db.ForeignKey("payment.id"))
    payment = db.relationship("Payment", back_populates="scheduled_rooms")
    scheduled_room_options = db.relationship("Scheduled_room_option", back_populates="scheduled_room")

class Scheduled_room_option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scheduled_room_id = db.Column(db.Integer, db.ForeignKey("scheduled_room.id"))
    scheduled_room = db.relationship("Scheduled_room", back_populates="scheduled_room_options")
    option_id = db.Column(db.Integer, db.ForeignKey("option.id"))
    option = db.relationship("Option", back_populates="scheduled_room_options")
    payment_id = db.Column(db.Integer, db.ForeignKey("payment.id"))
    payment = db.relationship("Payment", back_populates="scheduled_room_options")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

@app.route('/')
@app.route('/home')
def index():
    initialize_database()
    rooms = Room.query.all()
    return render_template('index.html', rooms=rooms)

@app.route('/room_detail/<int:room_id>')
def room_detail(room_id):
    initialize_database()
    room = Room.query.get(room_id)
    return render_template('room_detail.html', room=room)

@app.route('/checkin/<int:room_id>')
def checkin(room_id):
    room = Room.query.get_or_404(room_id)
    if room.status == 'available':
        room.status = 'occupied'
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/checkout/<int:room_id>')
def checkout(room_id):
    room = Room.query.get_or_404(room_id)
    if room.status == 'occupied':
        room.status = 'available'
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/upload_photo/<int:room_id>', methods=['GET', 'POST'])
def upload_photo(room_id):
    room = Room.query.get_or_404(room_id)
    if request.method == 'POST':
        if 'photo' not in request.files:
            return redirect(request.url)
        file = request.files['photo']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            room.photo = file_path
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('upload_photo.html', room=room)

def initialize_database():
    with app.app_context():
        db.create_all()  # Create all tables for all models
        if Room.query.count() == 0:
            # Add initial room data
            initial_rooms = [
                Room(id=101, name='Room 101', info='Single bed', max_people_num=1, type='Single', price=100, amenities='WiFi, TV', status='available'),
                Room(id=102, name='Room 102', info='Double bed', max_people_num=2, type='Double', price=150, amenities='WiFi, TV', status='available'),
                Room(id=103, name='Room 103', info='Suite', max_people_num=4, type='Suite', price=300, amenities='WiFi, TV, Mini-bar', status='occupied')
            ]
            db.session.add_all(initial_rooms)
            db.session.commit()

if __name__ == '__main__':
    if not os.path.exists('static/uploads'):
        os.makedirs('static/uploads')
    with app.app_context():
        initialize_database()
    app.run(debug=True)