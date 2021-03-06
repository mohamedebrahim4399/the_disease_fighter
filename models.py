from flask_sqlalchemy import SQLAlchemy

# database_path = "postgresql://mpbbfngyetvwwh:e6b72d158aba28dddaa1463877f9d6232aa84d65838800d5d4192ff5f1269123@ec2-52-19-164-214.eu-west-1.compute.amazonaws.com:5432/d5pp6e2lfl6cgb"
# database_path = "postgresql://{}:{}@{}/{}".format("postgres", "mohamed", "localhost:5432", "api")
database_path = "mysql+mysqlconnector://diseasefighter:mohamed159716@diseasefighter.mysql.pythonanywhere-services.com/diseasefighter$api"
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
    name = db.Column(db.String(30))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(350))
    phone = db.Column(db.String(15))
    location = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    about = db.Column(db.String(350))
    avatar = db.Column(db.String(250), default = "default.png")
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
            'avatar': "http://diseasefighter.pythonanywhere.com/static/" + self.avatar,
            'dob': self.dob and self.dob.strftime('%Y-%m-%d')
        }


'''
Doctor
'''


class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(350))
    phone = db.Column(db.String(15))
    clinic_location = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    x_y = db.Column(db.String(50))
    about = db.Column(db.String(350))
    avatar = db.Column(db.String(250), default="default.png")
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
        specialization = None
        if self.spec_id:
            specialization = Specialization.query.get(self.spec_id) and Specialization.query.get(self.spec_id).format()

        print(specialization)

        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'clinic_location': self.clinic_location,
            'gender': self.gender,
            'x_y': self.x_y,
            'about': self.about,
            'avatar': "http://diseasefighter.pythonanywhere.com/static/" + self.avatar,
            'dob': self.dob and self.dob.strftime('%Y-%m-%d'),
            'spec_id': self.spec_id,
            'available_dates': [available_date.format() for available_date in
                                Available_date.query.filter_by(doctor_id=self.id)],
            "specialization":  specialization or {}
        }


'''
Specialization
'''


class Specialization(db.Model):
    __tablename__ = 'specializations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    image = db.Column(db.String(150))

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
        image = self.image
        if image[:3].lower() != 'htt':
            image = "http://diseasefighter.pythonanywhere.com/static/specializations/" + self.image
        return {
            'id': self.id,
            'name': self.name,
            'image': image,
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
            'is_in_favorite_list': bool(self.is_in_favorite_list),
        }


'''
Review
'''


class Review(db.Model):
    __tablename__ = 'reviews'

    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'))
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id', ondelete='CASCADE'), primary_key=True)
    comment = db.Column(db.String(250))
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
    name = db.Column(db.String(30))
    gender = db.Column(db.String(10))
    date = db.Column(db.String(15))
    day = db.Column(db.String(15))
    time = db.Column(db.Time(10))
    am_pm = db.Column(db.String(5))
    phone = db.Column(db.String(15))
    comment = db.Column(db.String(250))
    diagnosis = db.Column(db.String(250))
    medicines = db.Column(db.String(250))
    files = db.Column(db.String(100))
    notification_seen = db.Column(db.Boolean)
    notification_time = db.Column(db.Time())
    deleted = db.Column(db.Boolean)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='CASCADE'))

    def __repr__(self):
        return f'<Session id: {self.id} name: {self.name} gender: {self.gender} day: {self.day} time: {self.time} am_pm: {self.am_pm} phone:{self.phone} comment: {self.comment} diagnosis: {self.diagnosis} medicines: {self.medicines} files: {self.files} notification_time: {self.notification_time} notification_seen: {self.notification_seen} deleted: {self.deleted} patient_id: {self.patient_id} doctor_id: {self.doctor_id}>'

    def __init__(self, name, gender, date, day, time, am_pm, phone, comment, diagnosis, medicines, files, notification_seen, notification_time, deleted, patient_id,
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
        self.notification_seen = notification_seen
        self.notification_time = notification_time
        self.deleted = deleted
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
            'files': (self.files or []) and ["https://diseasefighter.pythonanywhere.com/static/" + file for file in
                                             self.files.split(", ")],
            # This line will update when you deploy the app.
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
        }



'''
Available Date
'''


class Available_date(db.Model):
    __tablename__ = 'available_dates'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.String(50))
    end_time = db.Column(db.String(50))
    day = db.Column(db.String(20))
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
Period
'''


class Period(db.Model):
    __tablename__ = 'periods'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(20))
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
            'is_available': bool(self.is_available),
            'available_date_id': self.available_date_id,
            'session_id': self.session_id
        }
