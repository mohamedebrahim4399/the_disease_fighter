import os
from flask_sqlalchemy import SQLAlchemy

database_name = "api"
database_path = "postgresql://{}:{}@{}/{}".format("postgres", "mohamed", "localhost:5432", database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Patient
'''


class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    phone = db.Column(db.String())
    location = db.Column(db.String())
    gender = db.Column(db.String())
    about = db.Column(db.String())
    avatar = db.Column(db.String(), default="default.png")
    dob = db.Column(db.Date())

    def __repr__(self):
        return f'<Patient id: {self.id} name: {self.name} email: {self.email} password: {self.password} phone: {self.phone} location: {self.location} gender: {self.gender} about: {self.about} avatar: {self.avatar} dob: {self.dob}>'

    def __init__(self, name, email, password, phone, location, gender, about, avatar, dob):
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.location = location
        self.gender = gender
        self.about = about
        self.avatar = avatar
        self.dob = dob

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'gender': self.gender,
            'about': self.about,
            'avatar': "http://127.0.0.1:5000/static/" + self.avatar,
            'dob': self.dob and self.dob.strftime('%Y-%m-%d')
        }


'''
Doctor
'''


class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    phone = db.Column(db.String())
    clinic_location = db.Column(db.String())
    gender = db.Column(db.String())
    x_y = db.Column(db.String())
    about = db.Column(db.String())
    avatar = db.Column(db.String(), default="default.png")
    dob = db.Column(db.Date())
    spec_id = db.Column(db.Integer, db.ForeignKey('specializations.id', ondelete='CASCADE'))

    def __repr__(self):
        return f'<Doctor id: {self.id} name: {self.name} email: {self.email} password: {self.password} phone: {self.phone} clinic_location: {self.clinic_location} gender: {self.gender} x_y: {self.x_y} about: {self.about} avatar: {self.avatar} dob: {self.dob}, spec_id: {self.spec_id}>'

    def __init__(self, name, email, password, phone, clinic_location, gender, x_y, about, avatar, dob, spec_id):
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.clinic_location = clinic_location
        self.gender = gender
        self.x_y = x_y
        self.about = about
        self.avatar = avatar
        self.dob = dob
        self.spec_id = spec_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'clinic_location': self.clinic_location,
            'gender': self.gender,
            'x_y': self.x_y,
            'about': self.about,
            'avatar': "http://127.0.0.1:5000/static/" + self.avatar,
            'dob': self.dob and self.dob.strftime('%Y-%m-%d'),
            'spec_id': self.spec_id,
            "specialization": [specialization.format() for specialization in
                               Specialization.query.filter_by(id=self.spec_id)],
            'available_dates': [available_date.format() for available_date in
                                Available_date.query.filter_by(doctor_id=self.id)]

        }


'''
Specialization
'''


class Specialization(db.Model):
    __tablename__ = 'specializations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    image = db.Column(db.String())

    def __repr__(self):
        return f'<Specialization id: {self.id} name: {self.name} image: {self.image}>'

    def __init__(self, name, image):
        self.name = name
        self.image = image

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image,
        }


'''
Favorite
'''


class Favorite(db.Model):
    __tablename__ = 'favorites'

    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='CASCADE'), primary_key=True)
    is_in_favorite_list = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Favorite patient_id: {self.patient_id} doctor_id: {self.doctor_id} is_in_favorite_list: {self.is_in_favorite_list}>'

    def __init__(self, patient_id, doctor_id, is_in_favorite_list):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.is_in_favorite_list = is_in_favorite_list

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'is_in_favorite_list': self.is_in_favorite_list,
        }


'''
Review
'''


class Review(db.Model):
    __tablename__ = 'reviews'

    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'))
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id', ondelete='CASCADE'), primary_key=True)
    comment = db.Column(db.String())
    stars = db.Column(db.Integer)

    def __repr__(self):
        return f'<Review patient_id: {self.patient_id} session_id: {self.session_id} comment: {self.comment} stars: {self.stars}>'

    def __init__(self, patient_id, session_id, comment, stars):
        self.patient_id = patient_id
        self.session_id = session_id
        self.comment = comment
        self.stars = stars

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'patient_id': self.patient_id,
            'session_id': self.session_id,
            'comment': self.comment,
            'stars': self.stars,
        }


'''
Session
'''


class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    gender = db.Column(db.String())
    date = db.Column(db.String())
    day = db.Column(db.String())
    time = db.Column(db.Time())
    am_pm = db.Column(db.String(5))
    phone = db.Column(db.String())
    comment = db.Column(db.String())
    diagnosis = db.Column(db.String())
    medicines = db.Column(db.String())
    files = db.Column(db.String())
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='CASCADE'))

    def __repr__(self):
        return f'<Session id: {self.id} name: {self.name} gender: {self.gender} day: {self.day} time: {self.time} am_pm: {self.am_pm} phone:{self.phone} comment: {self.comment} diagnosis: {self.diagnosis} medicines: {self.medicines} files: {self.files} patient_id: {self.patient_id} doctor_id: {self.doctor_id}>'

    def __init__(self, name, gender, date, day, time, am_pm, phone, comment, diagnosis, medicines, files, patient_id,
                 doctor_id):
        self.name = name
        self.gender = gender
        self.date = date
        self.day = day
        self.time = time
        self.am_pm = am_pm
        self.phone = phone
        self.comment = comment
        self.diagnosis = diagnosis
        self.medicines = medicines
        self.files = files
        self.patient_id = patient_id
        self.doctor_id = doctor_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'date': self.date,
            'day': self.day,
            'time': str(self.time),
            'am_pm': self.am_pm,
            'phone': self.phone,
            'comment': self.comment,
            'diagnosis': self.diagnosis,
            'medicines': self.medicines,
            'files': (self.files or []) and ["http://127.0.0.1:5000/static/" + file for file in self.files.split(", ")],
            # This line will update when you deploy the app.
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id
        }


'''
Available Date
'''


class Available_date(db.Model):
    __tablename__ = 'available_dates'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.String())
    end_time = db.Column(db.String())
    day = db.Column(db.String())
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='CASCADE'))

    def __repr__(self):
        return f'<Available_date id: {self.id} start_time: {self.start_time} end_time: {self.end_time} day: {self.day} doctor_id: {self.doctor_id}>'

    def __init__(self, start_time, end_time, day, doctor_id):
        self.start_time = start_time
        self.end_time = end_time
        self.day = day
        self.doctor_id = doctor_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'day': self.day,
            'doctor_id': self.doctor_id,
        }


'''
Notification
'''


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    seen = db.Column(db.Boolean)
    time = db.Column(db.Time())
    doctor_name = db.Column(db.String())
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'))

    def __repr__(self):
        return f'<Notification id: {self.id} seen: {self.seen} time: {self.time}  doctor_name: {self.doctor_name} patient_id: {self.patient_id}>'

    def __init__(self, seen, time, doctor_name, patient_id):
        self.seen = seen
        self.time = time
        self.doctor_name = doctor_name
        self.patient_id = patient_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'seen': self.seen,
            'time': str(self.time),
            'doctor_name': self.doctor_name,
            'patient_id': self.patient_id,
        }


'''
Period
'''


class Period(db.Model):
    __tablename__ = 'periods'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String())
    is_available = db.Column(db.Boolean, default=False)
    available_date_id = db.Column(db.Integer, db.ForeignKey('available_dates.id', ondelete='CASCADE'))
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id', ondelete='SET NULL'), nullable=True)

    def __repr__(self):
        return f'<Period id: {self.id} time: {self.time} is_available: {self.is_available} available_date_id: {self.available_date_id} session_id:{self.session_id}>'

    def __init__(self, time, is_available, available_date_id, session_id):
        self.time = time
        self.is_available = is_available
        self.available_date_id = available_date_id
        self.session_id = session_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'time': self.time,
            'is_available': self.is_available,
            'available_date_id': self.available_date_id,
            'session_id': self.session_id
        }
