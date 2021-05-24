import os
from flask import Flask, request, abort, jsonify, session, redirect, url_for, render_template
from flask_cors import CORS
from sqlalchemy import text
import sqlalchemy
import json
from datetime import datetime, timedelta
from dateutil.parser import parse
import urllib.request
import requests
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from models import *

from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
    JWTManager
)

# create and configure the app
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkeyfordevelopmentonly*fordevelopment'
# app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this in your code!


app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)

# Set up upload image
app.config['UPLOAD_EXTENSIONS'] = ['jpg', 'jpeg', 'png', 'gif']
app.config['UPLOAD_PATH'] = 'static'

jwt = JWTManager(app)

setup_db(app)

# Set up CORS
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# The url of the client model and the url of the server.
base_url = "https://thediseasefighter.herokuapp.com/"
model_urls = []


@app.after_request
def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type, Authorization, true')
    response.headers.add(
        'Access-Control-Allow-Methods',
        'GET, PUT, POST, DELETE, OPTIONS')
    return response


@app.route('/')
def index():
    html = '''
    <div>
            <h1>API Documentation</h1>
            <h3><a target="_blank" href="https://github.com/mohamedebrahim4399/api_documention
    ">README</a>
    </div>
    '''
    return html


@app.route('/register', methods=["POST"])
def register():
    data = request.get_json()

    is_doctor = data.get('is_doctor')

    if "is_doctor" not in data:
        return jsonify({
            'message': 'is_doctor is missing',
            'error': 400,
            'success': False
        })

    name = data.get('name')
    email = data.get('email')
    password = generate_password_hash(data.get('password'), method="sha256")

    # -----------------------------------------------
    # if email exists
    patient = Patient.query.filter_by(email=email).first()
    doctor = Doctor.query.filter_by(email=email).first()
    if patient or doctor:
        return jsonify({
            "message": "This email already exists",
            "error": 409,
            "success": False
        }), 409
    # -----------------------------------------------

    phone = data.get('phone', None)
    gender = data.get('gender', None)
    about = data.get('about', None)
    avatar = data.get('avatar', "default.png")
    dob = data.get('dob', None)
    x_y = data.get('x_y', None)

    if is_doctor == True:
        clinic_location = data.get('clinic_location')
        spec_id = data.get('spec_id')

        try:
            doctor = Doctor(name=name, email=email, password=password, phone=phone, about=about, gender=gender,
                            avatar=avatar, dob=dob, clinic_location=clinic_location, spec_id=spec_id, x_y = x_y)
            doctor.insert()

            return login([doctor.email, doctor.password, True])

        except:
            abort(422)


    elif is_doctor == False:
        location = data.get('location', None)

        try:
            patient = Patient(name=name, email=email, password=password, phone=phone, about=about, gender=gender,
                              avatar=avatar, dob=dob, location=location)
            patient.insert()

            return login([patient.email, patient.password, False])

        except:
            abort(422)

    else:
        abort(400)


@app.route('/login', methods=["POST"])
def login(register_data=None):

    # Redirect From Registration Page
    if register_data is not None:
        email, password, is_doctor = register_data

        if is_doctor:
            doctor = Doctor.query.filter_by(email=email).first()
            return create_token(doctor.id, True)
        else:
            patient = Patient.query.filter_by(email=email).first()
            return create_token(patient.id, False)

    # ----- From Login Page ------------------------------------
    data = request.get_json()

    if "email" not in data or "password" not in data:
        return jsonify({
            'message': 'The email or password is missing',
            'error': 401,
            'success': False
        }), 401

    email = data.get('email').strip()

    patient = Patient.query.filter_by(email=email).first()
    doctor = Doctor.query.filter_by(email=email).first()

    if (patient or doctor) is None:
        abort(401)

    user = patient or doctor

    if check_password_hash(user.password, data['password']):
        if patient:
            return create_token(user.id, False)
        else:
            return create_token(user.id, True)

    # Password is incorrect
    return jsonify({
        'message': 'The email or password is incorrect',
        'error': 401,
        'success': False
    }), 401


def create_token(id, is_doctor):
    additional_claims = {
        "is_doctor": is_doctor
    }
    access_token = create_access_token(id, additional_claims=additional_claims)

    return jsonify(access_token=access_token, is_doctor=is_doctor, success=True)


# Not Used after not
@app.route("/logout")
def logout():
    return ({
        "message": "Clear the access token from yours to logout😊😊. Please don't use this route again😢"
    })


# ______________ Current Logged in User _______________

@app.route('/user')
@jwt_required()
def get_current_user():
    claims = get_jwt()
    try:
        format = ""
        current_user = ""

        if claims['is_doctor']:  # this is a doctor
            current_user = Doctor.query.get(claims['sub'])
            format=current_user.format()
        else:
            current_user = Patient.query.get(claims['sub'])
            format=current_user.format()

        return jsonify({
            "current_user": format,
            'success': True
        }), 200
    except:
        abort(422)


@app.route('/user', methods=['PATCH'])
@jwt_required()
def update_current_user():
    claims = get_jwt()
    data = request.get_json()
    try:

        if "email" in data:
            return jsonify({
                "message": "You can't update your email",
                "error": 422,
                "success": False
            }), 422

        if "avatar" in data:
            return jsonify({
                "message": "You can't update your avatar from this route, You should use /avatar route",
                "error": 422,
                "success": False
            }), 422

        current_user = ""
        if claims['is_doctor']:
            doctor = Doctor.query.get(claims['sub'])
            # To make necessary to enter the id of Specialization
            if doctor.spec_id is None:
                if data.get('spec_id') is None:
                    return jsonify({
                        "message": "You must send spec_id",
                        "error": 401,
                        "success": False
                    }), 401

            doctor.update(data)

        else:
            patient = Patient.query.get(claims['sub'])
            patient.update(data)

        return jsonify({
            'message': 'You have updated your data successfully',
            'success': True,
        })
    except:
        abort(400)


@app.route('/password', methods=["PATCH"])
@jwt_required()
def update_password():
    claims = get_jwt()
    data = request.get_json()

    if "new_password" not in data or "current_password" not in data:
        return jsonify({
            "message": "new_password or current_password is missing",
            "error": 400,
            "success": False
        }), 400

    current_user = ""

    if claims['is_doctor']:
        current_user = Doctor.query.get(claims['sub'])
    else:
        current_user = Patient.query.get(claims['sub'])

    if data['current_password'] == data['new_password']:
        return jsonify({
            'message': "The new password is the same of the current password",
            "error": "unprocessable",
            "success": False
        }), 422

    if check_password_hash(current_user.password, data['current_password']):
        password = generate_password_hash(data.get('new_password'), method="sha256")
        current_user.update({"password": password})

        return jsonify({
            "message": "The password has been updated",
            "success": True
        }), 200

    return jsonify({
        "message": "Your current password is wrong",
        "error": 422,
        "success": False
    }), 422


# ________________ Notification ________________
@app.route('/notifications')
@jwt_required()
def get_all_Notification():
    claims = get_jwt()
    try:
        if claims['is_doctor']:
            return jsonify({
                "message": "You aren't allowed to open this route",
                "error": 403,
                "success": False
            }), 403

        notifications = Session.query.filter(Session.patient_id == claims['sub'], Session.notification_time != None, Session.deleted != True).all()

        if len(notifications) == 0:
            return jsonify({
                "message": "There aren't any Notifications",
                "error": 404,
                "success": False
            }), 404

        return jsonify({
            "notifications": [notification.format(True) for notification in notifications],
            "total_notifications": len(notifications),
            'success': True
        })
    except:
        return jsonify({
            "message": "There's an Error",
            "error": 422,
            "success": False
        })

# To Delete or Seen the Notification
@app.route('/notifications/<int:session_id>', methods=['PATCH'])
@jwt_required()
def update_notification(session_id):
    data = request.get_json()
    claims = get_jwt()
    try:
        if claims['is_doctor']:
            return jsonify({
                "message": "You aren't allowed to open this route",
                "error": 403,
                "success": False
            }), 403

        notification = Session.query.filter(Session.id == session_id, Session.patient_id == claims['sub']).first()

        if notification is None:
            return jsonify({
                "message": "This notification wasn't found",
                "error": 404,
                "success": False
            })

        if notification.deleted:
            return jsonify({
                "message": "You have deleted this notification before",
                "error": 422,
                "success": False
            })

        if notification.notification_seen:#####################################
            return jsonify({
                "message": "You have seen this notification before",
                "error": 422,
                "success": False
            })

        if "type" in data:
            # print(data['type'])
            if data['type'] == 'delete':
                notification.update({"deleted": True})
                return jsonify({
                    "message": "You have delete the notification",
                    "success": True
                })
            elif data['type'] == 'update':
                notification.update({'notification_seen': True})
                return jsonify({
                    "message": "The Notification has been updated",
                    "success": True
                })
            else:
                return jsonify({
                    "message": "You should put 'type' with delete or update",
                    "error": 400,
                    "success": False
                })
        else:
            return jsonify({
                "message": "You should put 'type' with delete or update",
                "error": 400,
                "success": False
            })
    except:
        abort(422)


# ___________ doctor ___________
def doctor_reviews(doctor_id):
    query = sqlalchemy.text(
        f''' select reviews.stars, patients.avatar from sessions join reviews on sessions.id = reviews.session_id join patients on patients.id = reviews.patient_id where sessions.doctor_id = {doctor_id}; ''')
    query_result = db.engine.execute(query)
    fetch_data = query_result.fetchall()

    stars = 0
    count = 0
    rates = 0
    avatars = []

    for data in fetch_data:
        stars += data[0]
        count = count + 1

        if len(avatars) <= 2:
            avatars.append(f"https://thediseasefighter.herokuapp.com/static/{data[1]}")

    if not count == 0:
        rates = int(stars / count)
    else:
        rates = 0

    reviews = {
        "reviews": {
            "rates": rates,
            "no.patients": count,
            "avatars": avatars
        }
    }

    return reviews

def favorite_list(doctor_id, patient_id):
    is_in_favorite_list = False
    in_favorite = Favorite.query.filter_by(doctor_id=doctor_id, patient_id=patient_id).first()
    if in_favorite:
        is_in_favorite_list = in_favorite.is_in_favorite_list
    return {"is_in_favorite_list": is_in_favorite_list}

@app.route('/doctors')
@jwt_required()
def get_all_doctors():
    claims = get_jwt()
    try:
        if claims['is_doctor']:
            return jsonify({
                "message": "You aren't allowed to open this route",
                "error": 403,
                "success": True
            }), 403
        doctors = Doctor.query.order_by('id').all()

        if len(doctors) == 0 :
            return jsonify({
                "message": "There's not any doctors",
                "error": 404,
                "success": False
            }), 404

        doctors_list = []

        for doctor in doctors:
            reviews = doctor_reviews(doctor.id)

            doctor_obj = {}
            doctor_obj.update(doctor.format())
            doctor_obj.update(reviews)
            doctor_obj.update(favorite_list(doctor.id, claims['sub']))
            doctors_list.append(doctor_obj)

        return jsonify({
            'doctors': doctors_list,
            "total_doctors": len(doctors),
            "success": True
        })
    except:
        return jsonify({
            "message": "No doctors were found",
            "error": 404,
            "success": False,
        })

@app.route('/doctors/<int:doctor_id>')
@jwt_required()
def get_one_doctor(doctor_id):
    claims = get_jwt()
    try:
        if claims['is_doctor']:
            return jsonify({
                "message": "You aren't allowed to open this route",
                "error": 403,
                "success": False
            }), 403

        doctor = Doctor.query.get(doctor_id)
        reviews = doctor_reviews(doctor.id)
        is_in_favorite_list = favorite_list(doctor_id, claims['sub'])

        doctor_obj = {}
        doctor_obj.update(doctor.format())
        doctor_obj.update(reviews)
        doctor_obj.update(is_in_favorite_list)

        return jsonify({
            'doctor': doctor_obj,
            'success': True
        })
    except:
        return jsonify({
            "message": "The doctor was not found",
            "error": 404,
            "success": False
        })


@app.route('/doctors/top')
@jwt_required()
def top_doctors():
    claims = get_jwt()
    try:
        if claims['is_doctor']:
            return jsonify({
                "message": "You aren't allowed to open this route",
                "error": 403,
                "success": False
            }), 403
        doctors = Doctor.query.order_by('id').all()

        doctor_list = []

        for doctor in doctors:
            reviews = doctor_reviews(doctor.id)
            doctor_obj = {}
            doctor_obj.update(doctor.format())
            doctor_obj.update(reviews)
            doctor_obj.update(favorite_list(doctor.id, claims['sub']))
            doctor_list.append(doctor_obj)

        # Sort by the highest rated doctors
        doctor_list.sort(key=lambda e: e['reviews']['rates'], reverse=True)

        top_doctors = doctor_list[:10]

        return jsonify({
            "top_doctors": top_doctors,
            "Success": True,
            "total_top_doctors": len(top_doctors)
        })
    except:
        return jsonify({
            "message": "No Top doctors found",
            "error": 404,
            "success": False
        })


# _____________________Available_date _______________________
def available_dates(start_time, end_time):
    periods = []

    start = start_time
    end = end_time

    if start[-2:] == "pm":
        start = float(".".join(start[:-2].split(":")))
        start = start + 12
    else:
        start = float(".".join(start[:-2].split(":")))

    if end[-2:] == "pm":
        end = float(".".join(end[:-2].split(":")))
        end = end + 12
    else:
        end = float(".".join(end[:-2].split(":")))

    count = int((end - start) * 2)

    result = abs(start - end)

    def solve(s, n, count):
        h, m = map(int, s[:-2].split(':'))
        h %= 12
        if s[-2:] == 'pm':
            h += 12
        t = h * 60 + m + n
        h, m = divmod(t, 60)
        h %= 24
        suffix = 'a' if h < 12 else 'p'
        h %= 12
        if h == 0:
            h = 12

        st = "{:02d}:{:02d} {}m".format(h, m, suffix)

        periods.append(s)
        if count > 0:
            count -= 1
            solve(st, 30, count)

        else:
            return "{:02d}:{:02d} {}m".format(h, m, suffix)

    solve(start_time, 30, count)

    if not (str(start)[-1] == "0" and str(end)[-1] != "0") or (str(start)[-1] != "0" and str(end)[-1] == "0"):
        periods.pop()

    return periods


def sort_dates(dates):
    days = {
        "Saturday": 0,
        "Sunday": 1,
        "Monday": 2,
        "Tuesday": 3,
        "Wednesday": 4,
        "Thursday": 5,
        "Friday": 6
    }

    doctor_days = dates

    for i in range(1, len(doctor_days)):

        key = doctor_days[i]

        j = i - 1
        while j >= 0 and days[key.day] < days[doctor_days[j].day]:
            doctor_days[j + 1] = doctor_days[j]
            j -= 1
        doctor_days[j + 1] = key


def sort_days(dates):
    days = {
        "Saturday": 0,
        "Sunday": 1,
        "Monday": 2,
        "Tuesday": 3,
        "Wednesday": 4,
        "Thursday": 5,
        "Friday": 6
    }

    # Order generalized dates
    sort_dates(dates)

    today = datetime.now().strftime("%A")
    # today = datetime(2021, 4, 14).strftime('%A')

    doctor_days = []  # Will contain the id & name of a day.
    days_list = []  # For days name.

    for date in dates:
        days_list.append(date.day)  # Get all the days name only
        day_obj = {}
        day_obj.update({"id": date.id, "day": date.day})
        doctor_days.append(day_obj)

    if (
            days[today] not in days_list  # if today is not in doctors date
    ) and (
            days[today] > days[days_list[len(days_list) - 1]]
            # The today value is greater than of the greatest value of doctor days
    ):

        if days[today] >= days[days_list[-1]]:  # if today is the last value in the dictionary
            today = "Saturday"  # Make today is the first day in the dictionary.

    i = 0
    while i < len(days_list):
        if days[today] > days[doctor_days[i]['day']]:
            doctor_days.append(doctor_days.pop(0))
        else:
            return doctor_days


def create_periods(date_id, start, end):
    periods = available_dates(start, end)
    for p in periods:
        period = Period(time=p, is_available=False, available_date_id=date_id, session_id=None)
        period.insert()


def delete_periods(date_id):
    periods = Period.query.filter_by(available_date_id=date_id)
    for period in periods:
        period.delete()


def update_period(session_id, period_id, previous_period_id=None):
    if previous_period_id is not None:
        previous_period = Period.query.get(previous_period_id)
        previous_period.session_id = None
        previous_period.is_available = False
        previous_period.update()

    period = Period.query.get(period_id)
    period.session_id = session_id
    period.is_available = True
    period.update()

# Delete the unused period appointment.
def delete_unused_appointment():
    # Delete the unused period appointment.
    query = sqlalchemy.text(
        f''' select periods.id as period_id, periods.time, sessions.name, sessions.date from periods join sessions on periods.session_id = sessions.id order by sessions.date; ''')

    today = datetime.now().strftime('%Y-%m-%d')

    query_result = db.engine.execute(query)
    fetch_data = query_result.fetchall()

    for data in fetch_data:
        if str(today) > str(data.date):
            period = Period.query.get(data.period_id)
            period.is_available = False
            period.session_id = None
            period.update()
        else:
            break

@app.route('/doctors/<int:doctor_id>/days')
@jwt_required()
def get_doctor_days(doctor_id):
    claims = get_jwt()
    try:
        if claims['is_doctor']:
            return jsonify({
                "message": "You aren't allowed to open this route",
                "error": 403,
                "success": False
            }), 403
        dates = Available_date.query.filter(Available_date.doctor_id == doctor_id).order_by('id').all()

        delete_unused_appointment()

        if dates == []:
            return jsonify({
                "message": "There are no dates",
                "error": 404,
                "success": False
            }), 404

        days_list = []
        days = sort_days(dates)

        return jsonify({
            "days": days,
            "success": True,
            "total_days": len(days),
        })
    except:
        abort(404)


# -- periods of day
@app.route('/doctors/days/<int:day_id>')
@jwt_required()
def get_periods(day_id):
    claims = get_jwt()
    try:
        if claims['is_doctor']:
            return jsonify({
                "message": "You aren't allowed to open this route",
                "error": 403,
                "success": False
            }), 403
        periods = Period.query.filter(Period.available_date_id == day_id).order_by("id").all()

        if periods == []:
            return jsonify({
                "message": "There are no time periods",
                "error": 404,
                "success": False
            }), 404

        return jsonify({
            "periods": [period.format() for period in periods]
        })
    except:
        abort(404)


@app.route('/doctors/<int:doctor_id>/dates')
@jwt_required()
def get_all_dates(doctor_id):
    claims = get_jwt()
    try:
        if claims['is_doctor']:
            return jsonify({
                "message": "You aren't allowed to open this route",
                "error": 403,
                "success": False
            }), 403
        dates = Available_date.query.filter(Available_date.doctor_id == doctor_id).order_by('id').all()

        if len(dates) == 0:
            return jsonify({
                "message": "There are not any dates",
                "error": 404,
                "success": False
            }), 404

        dates_list = []

        for date in dates:
            dates_object = {}
            dates_object.update(date.format())

            available_dates = Period.query.filter_by(available_date_id=date.id).order_by('id').all()
            dates_object.update({"available_dates": [available_date.format() for available_date in available_dates]})

            dates_list.append(dates_object)

        return jsonify({
            "dates": dates_list,
            "success": True
        })
    except:
        abort(404)


@app.route('/doctors/dates', methods=['POST'])
@jwt_required()
def create_date():
    claims = get_jwt()
    try:
        if not claims['is_doctor']:  # this is a patient
            return jsonify({
                "message": "You aren't allowed to open this route",
                "error": 403,
                "success": False
            }), 403
        data = request.get_json()

        start_time = data.get('start_time')
        end_time = data.get('end_time')
        day = data.get('day')

        if "start_time" not in data or "end_time" not in data or "day" not in data:
            return jsonify({
                "message": "start_time, end_time, or day are not in the body request",
                "error": 400,
                "success": False
            }), 400

        status, result = check_time([start_time, end_time])
        if status == False:
            return result

        start_time, end_time = result

        date = Available_date(
            start_time=start_time,
            end_time=end_time,
            day=day.capitalize(),
            doctor_id=claims['sub']
        )

        date.insert()

        create_periods(date.id, date.start_time, date.end_time)

        return jsonify({
        "message": "You have created a new date",
        "success": True
    })
    except:
        abort(422)


@app.route("/doctors/dates/<int:date_id>", methods=['PATCH'])
@jwt_required()
def update_date(date_id):
    claims = get_jwt()
    try:
        if not claims['is_doctor']:
            return jsonify({
                "message": "You aren't allowed to open this route",
                "error": 403,
                "success": False
            }), 403
        data = request.get_json()
        date = Available_date.query.filter_by(id = date_id, doctor_id = claims['sub']).first()

        if date is None:
            return jsonify({
                "message": "This route isn't for you.",
                "error": 403,
                "success": False
            })

        if date is None:
            abort(404)

        if "start_time" in data or "end_time" in data:
            start_time = data.get('start_time', date.start_time)
            end_time = data.get('end_time', date.end_time)

            status, result = check_time([start_time, end_time])
            if status == False:
                return result

            start_time, end_time = result
            data.update({"start_time": start_time, "end_time": end_time})

        date.update(data)

        delete_periods(date.id)
        create_periods(date.id, date.start_time, date.end_time)

        return jsonify({
            "message": "Date has been updated successfully",
            "success": True
        })
    except:
        abort(422)


@app.route('/doctors/dates/<int:date_id>', methods=["DELETE"])
@jwt_required()
def delete_date(date_id):
    claims = get_jwt()
    try:
        if not claims['is_doctor']:
            return jsonify({
                "message": "You aren't allowed to open this route",
                "error": 403,
                "success": False
            }), 403
        date = Available_date.query.get(date_id)

        if date is None:
            return jsonify({
                "message": "The date not found",
                "error": 404,
                "success": False
            }), 404

        date.delete()

        return jsonify({
            "message": "You've deleted the date successfully",
            "success": True
        })
    except:
        abort(422)


# Check the start and end time and make it suitable for storing it in db.
def check_time(times):
    am_pm = ["am", "pm"]
    result = []
    calc = []

    for time in times:
        time = time.strip()
        time = time.lower()

        if ":" not in time:
            return [False, {
                "message": "Enter a valid time",
                "error": 422,
                "success": False
            }]

        if time[-2:] not in am_pm:
            return [False, {
                "message": "You should put the pm or am with start_time and end_time",
                "error": 422,
                "success": False
            }]

        am_pm_desired = ""
        for i in range(0, len(am_pm)):
            if am_pm[i] in time:
                index = time.index(am_pm[i])
                am_pm_desired = time[index:]
                time = time[:index]
            time = time.split(":")

            if len(time[i]) == 1:
                time[i] = "0" + time[i]
            time = ":".join(time)

        if am_pm_desired.lower() == 'pm':
            calc.append(int(time.split(":")[0]) + float("." + time.split(":")[1]) + 12)
        else:
            calc.append(int(time.split(":")[0]) + float("." + time.split(":")[1]))

        time = time.strip() + " " + am_pm_desired
        result.append(time)

    print(calc)

    if len(times) >= 2 and calc[0] >= calc[1]:
        return [False, {
            "message": "The end_time should be greater than start_time",
            "error": 422,
            "success": False
        }]

    return [True, result]


# ______________ specializations ______________
@app.route('/specializations')
def get_all_specializations():
    try:
        specializations = Specialization.query.order_by('id').all()

        if specializations == []:
            return jsonify({
                "message": "There are not any specializations",
                'error': 404,
                "success": False
            }), 404

        return jsonify({
            "specializations": [specialization.format() for specialization in specializations],
            "total_specializations": len(specializations),
            "success": True
        })
    except:
        abort(404)


@app.route('/specializations/<int:specialization_id>/doctors')
@jwt_required()
def get_doctors_by_specialization(specialization_id):
    claims = get_jwt()
    try:
        if claims['is_doctor']:
            return jsonify({
                "message": "You aren't allowed to open this route",
                "error": 403,
                "success": False
            }), 403
        doctors = Doctor.query.filter(Doctor.spec_id == specialization_id).order_by('id').all()

        if len(doctors) == 0:
            return jsonify({
                'message': "There are no doctors in this specialization yet.",
                "error": 404,
                "success": False
            }), 404

        doctors_list = []

        for doctor in doctors:
            reviews = doctor_reviews(doctor.id)

            doctor_obj = {}
            doctor_obj.update(doctor.format())
            doctor_obj.update(reviews)
            doctors_list.append(doctor_obj)

        return jsonify({
            'success': True,
            'specialization': specialization_id,
            'doctors': doctors_list,
            'total_doctors_in_specialization': len(doctors_list),
        })
    except:
        abort(404)


# ______________ Sessions ______________

# Get date from day name
def get_day_date(day):
    days = {
        "Saturday": 0,
        "Sunday": 1,
        "Monday": 2,
        "Tuesday": 3,
        "Wednesday": 4,
        "Thursday": 5,
        "Friday": 6
    }

    today = datetime.now()
    today_day = today.strftime('%A')

    days_list = list(days.keys())
    index = days_list.index(today_day)
    difference = 0

    while index is not days_list.index(day):
        if index == len(days_list):
            index = 0
        else:
            difference += 1
            index += 1

    desired_date = today + timedelta(days=difference)
    desired_date = desired_date.strftime('%Y-%m-%d')

    return desired_date


@app.route('/sessions')
@jwt_required()
def get_sessions():
    claims = get_jwt()

    delete_unused_appointment()

    if claims['is_doctor']:
        sessions = Session.query.filter_by(doctor_id=claims['sub']).order_by('id').all()

        if sessions == []:
            return jsonify({
                "message": "You don't have any appointments",
                "error": 404,
                "success": False
            }), 404

        future_appointments, current_appointments, previous_appointments = create_appointments(sessions, claims['is_doctor'])

        return jsonify({
            'all_appointments': [session.format(False, "is_doctor") for session in sessions],
            'future_appointments': future_appointments,
            'current_appointments': current_appointments,
            'previous_appointments': previous_appointments,
            "total_appointments": len(sessions),
            'success': True
        })

    else:

        sessions = Session.query.filter_by(patient_id=claims['sub']).order_by('id').all()

        if sessions == []:
            return jsonify({
                "message": "You don't have any appointments",
                "error": 404,
                "success": False
            }), 404

        future_appointments, previous_appointments = create_appointments(sessions, claims['is_doctor'])

        return jsonify({
            "future_appointments": future_appointments,
            "previous_appointments": previous_appointments,
            "total_appointments": len(sessions),
            'success': True
        })


@app.route('/sessions/<int:session_id>')
@jwt_required()
def get_one_session(session_id):
    claims = get_jwt()
    try:
        delete_unused_appointment()
        current_session = ''
        if claims['is_doctor']:
            current_session = Session.query.filter_by(id=session_id, doctor_id=claims['sub']).first()
        else:
            current_session = Session.query.filter_by(id=session_id, patient_id=claims['sub']).first()

        if current_session is None or current_session == '':
            return jsonify({
                'message': "This session is not for you.",
                'error': 403,
                'success': False
            }), 403

        return jsonify({
            'session': current_session.format(False, claims['is_doctor']),
            'success': True
        })
    except:
        return jsonify({
            "message": "This session was not found",
            "error": 404,
            "success": False
        }), 404


# filtered sessions => For Doctor only not user
@app.route('/sessions/filter')
@jwt_required()
def filter_doctors():
    claims = get_jwt()
    data = request.args

    doctor_id = claims['sub']
    claims = get_jwt()
    try:
        if not claims['is_doctor']:
            return jsonify({
                "message": "You aren't allowed to open this route",
                "error": 403,
                "success": False
            }), 403
        if "date" not in data:
            return jsonify({
                "message": "date is not in body request",
                "error": 400,
                "success": False
            }), 400

        date = parse(data.get('date')).strftime('%Y-%m-%d')
        sessions = Session.query.filter_by(date=date, doctor_id=doctor_id).all()

        if sessions == []:
            return jsonify({
                "message": "There is any appointments",
                "error": 404,
                "success": False
            }), 404

        session_list = []

        for s in sessions:
            patient = Patient.query.get(s.patient_id)
            session_obj = {}
            session_obj.update(s.format())
            session_obj.update({"avatar": patient.avatar})
            session_list.append(session_obj)

        return jsonify({
            "sessions": session_list,
            "Success": True,
            "total_sessions": len(session_list)
        })
    except:
        return jsonify({
            "message": "There is any appointments",
            "error": 404,
            "success": False
        }), 404


# Patient only that has the access to create the session
@app.route('/doctors/<int:doctor_id>/sessions', methods=['POST'])
@jwt_required()
def create_session(doctor_id):
    claims = get_jwt()
    data = request.get_json()
    try:
        if claims['is_doctor']:
            return jsonify({
                "message": "You aren't allowed to open this route",
                "error": 403,
                "success": False
            }), 403
        if "period_id" not in data or "previous_period_id" not in data or "day" not in data:
            return jsonify({
                "message": "You don't send period_id, previous_period_id and day in the body request",
                "error": 401,
                "success": False
            }), 401

        patient_id = claims['sub']

        day = data.get('day', None).capitalize()
        date = get_day_date(day)

        time = data.get('time', None)
        am_pm = data.get('am_pm', None)
        name = data.get('name', None)
        gender = data.get('gender', None)
        phone = data.get('phone', None)
        comment = data.get('comment', None)

        diagnosis = data.get('diagnosis', None)
        medicines = data.get('medicines', None)
        files = data.get('files', None)

        # To reserve an appointment with a period of time
        period_id = data.get("period_id", None)
        previous_period_id = data.get("previous_period_id", None)

        notification_time = None
        notification_seen = False
        deleted = False

        new_session = Session(
            date=date,
            day=day.capitalize(),
            time=time,
            am_pm=am_pm,
            name=name,
            gender=gender,
            phone=phone,
            comment=comment,
            doctor_id=doctor_id,
            patient_id=patient_id,
            diagnosis=diagnosis,
            medicines=medicines,
            files=files,
            notification_time = notification_time,
            notification_seen = notification_seen,
            deleted = deleted
        )

        new_session.insert()
        session_id = new_session.id

        update_period(session_id, period_id, previous_period_id)

        return jsonify({
            "message": "You have reserved an appointment with the doctor",
            'success': True
        })
    except:
        abort(422)


@app.route('/sessions/<int:session_id>', methods=['PATCH'])
@jwt_required()
def update_session(session_id):
    claims = get_jwt()
    data = request.get_json()
    try:
        current_session = []

        if claims['is_doctor']:
            current_session = Session.query.filter_by(id=session_id, doctor_id=claims['sub']).first()
        else:
            current_session = Session.query.filter_by(id=session_id, patient_id=claims['sub']).first()

        if current_session is None:
            return jsonify({
                "message": "This appointment is not for you.",
                "error": 404,
                "success": False
            }), 404

        if "day" in data:
            day = data.get('day', None).capitalize()
            date = get_day_date(day)

            data.update({"day": day, "date": date})

        if "files" in data:
            if type(data['files']) != type([]):
                return jsonify({
                    "message": "You should send the files as an array",
                    "error": 422,
                    "success": False
                }), 422
            files = ", ".join(data['files'])
            data['files'] = files

        if "diagnosis" in data or "medicines" in data:
            notification_time = datetime.now().strftime("%H:%M:%S")[:-3]
            notification_seen = False
            data.update({
                "notification_time": notification_time,
                "notification_seen": notification_seen
            })

        current_session.update(data)

        if "day" in data or "time" in data or "am_pm" in data:
            session_id = session_id
            if "period_id" in data and "previous_period_id" in data:
                period_id = data.get("period_id")
                previous_period_id = data.get("previous_period_id")
                update_period(session_id, period_id, previous_period_id)

                return jsonify({
                    "message": "The appointment has been updated successfully",
                    'success': True
                })
            else:
                return jsonify({
                    "message": "You should send period_id and previous_period_id",
                    "error": 422,
                    "success": False
                }), 422

        return jsonify({
            "message": "You have updated the appointment",
            'success': True
        })
    except:
        abort(422)


@app.route('/sessions/<int:session_id>', methods=["DELETE"])
@jwt_required()
def delete_session(session_id):
    claims = get_jwt()
    try:
        current_session = []

        if claims['is_doctor']:
            current_session = Session.query.filter_by(id=session_id, doctor_id=claims['sub']).first()
        else:
            current_session = Session.query.filter_by(id=session_id, patient_id=claims['sub']).first()

        if current_session is None:
            return jsonify({
                "message": "The session wasn't found",
                "error": 404,
                "success": False
            }), 404


        periods = Period.query.filter_by(session_id=session_id).first()


        if periods is None:
            current_session.delete()
            return jsonify({
                'message': "You've deleted the appointment successfully",
                'success': True
            })

        periods.is_available = False
        periods.update()
        current_session.delete()

        return jsonify({
            'message': "You've deleted the appointment successfully",
            'success': True
        })
    except:
        abort(422)


# - Upload Diagnosis Files inside Session -
@app.route('/sessions/<int:session_id>/reviews', methods=["POST"])
@jwt_required()
def create_reviews(session_id):
    claims = get_jwt()
    try:
        if claims['is_doctor']:
            return jsonify({
                "message": "You aren't allowed to open this route",
                "error": 403,
                "success": False
            }), 403
        data = request.get_json()

        session = Session.query.get(session_id)
        if session is None:
            return jsonify({
                "message": "This session isn't valid",
                "error": 422,
                "success": False
            })


        patient_id = claims['sub']
        session_id = session_id
        comment = data.get('comment', None)
        stars = data.get('stars', None)

        if (comment and stars) is None:
            return jsonify({
                "message": "You should send comment and star in the body request",
                "error": 400,
                "success": False
            }), 400

        review = Review(
            patient_id=patient_id,
            session_id=session_id,
            comment=comment,
            stars=stars,

        )

        review.insert()

        return jsonify({
            "message": "You have added a review successfully",
            'success': True
        })
    except:
        abort(422)


@app.route('/sessions/<int:session_id>/files', methods=['PATCH'])
@jwt_required()
def upload_files(session_id):
    claims = get_jwt()
    try:
        if not claims['is_doctor']:
            return jsonify({
                "message": "You aren't allowed to open this route",
                "error": 403,
                "success": False
            }), 403
        status, result = get_images()
        if not status:
            return result

        new_files = result
        current_session = Session.query.get(session_id)

        files_str = ", ".join(new_files)

        current_session.update({"files": files_str})

        return jsonify({
            "message": "The files have been uploaded successfully",
            "success": True
        })
    except:
        abort(422)


# ______________ Favorite List ______________

@app.route('/doctors/<int:doctor_id>/favorite', methods=["POST"])
@jwt_required()
def add_to_favorite_list(doctor_id):
    data = request.get_json()
    claims = get_jwt()
    try:
        if claims['is_doctor']:
            return jsonify({
                "message": "You aren't allowed to open this route",
                "error": 403,
                "success": False
            }), 403
        patient_id = claims['sub']
        doctor_id = doctor_id
        is_in_favorite_list = data.get('is_in_favorite_list')

        if "is_in_favorite_list" not in data:
            return jsonify({
                "message": "You should send is_in_favorite_list in the body",
                "error": 400,
                "success": False
            }), 400

        favorite = Favorite(
            patient_id=patient_id,
            doctor_id=doctor_id,
            is_in_favorite_list=is_in_favorite_list

        )

        favorite.insert()

        return jsonify({
            "message": "You have added this doctor to your favorites list.",
            'success': True
        })
    except:
        abort(400)


@app.route('/favorites')
@jwt_required()
def get_all_favorite_doctors():
    claims = get_jwt()
    try:
        if claims['is_doctor']:
            return jsonify({
                "message": "You aren't allowed to open this route",
                "error": 403,
                "success": False
            }), 403
        patient_id = claims['sub']  # => From token

        query = sqlalchemy.text(
            f''' select doctors.id, doctors.name, doctors.avatar, doctors.clinic_location, favorites.is_in_favorite_list from doctors join favorites on favorites.doctor_id = doctors.id and favorites.patient_id = {patient_id} where favorites.is_in_favorite_list = true; ''')

        doctors_list = []

        query_result = db.engine.execute(query)
        fetch_data = query_result.fetchall()

        if len(fetch_data) == 0:
            return jsonify({
                "message": "You don't have any doctors in your Favorite List",
                "error": 404,
                "success": False
            })
            abort(404)

        for data in fetch_data:
            doctor_obj = {}
            doctor_obj.update({"id": data[0], "name": data[1], "avatar": data[2], "clinic_location": data[3], "is_in_favorite_list": data[4]})

            doctor_obj.update(doctor_reviews(data[0]))

            doctors_list.append(doctor_obj)

        return jsonify({
            "success": True,
            "doctors": doctors_list
        })
    except:
        abort(404)


@app.route('/doctors/<int:doctor_id>/favorite', methods=["DELETE"])
@jwt_required()
def update_favorites_doctors(doctor_id):
    claims = get_jwt()
    # try:
    if claims['is_doctor']:
        return jsonify({
            "message": "You aren't allowed to open this route",
            "error": 403,
            "success": False
        }), 403
    favorites = Favorite.query.filter_by(doctor_id=doctor_id).first()

    if favorites is None:
        return jsonify({
            "message": "This item wasn't found",
            "error": 404,
            "success": False
        })

    favorites.delete()

    return jsonify({
        "message": "You've deleted the doctor in the favorite list",
        'success': True
    })
    # except:
    #     abort(422)


# _____________Reviews __________

@app.route('/doctors/<int:doctor_id>/reviews')
@jwt_required()
def get_reviews(doctor_id):
    claims = get_jwt()
    try:
        if claims['is_doctor']:
            return jsonify({
                "message": "You aren't allowed to open this route",
                "error": 403,
                "success": False
            }), 403
        query = sqlalchemy.text(
            f''' select reviews.stars, patients.avatar, patients.name, reviews.comment from sessions join reviews on sessions.id = reviews.session_id join patients on patients.id = reviews.patient_id where sessions.doctor_id = {doctor_id}; ''')
        query_result = db.engine.execute(query)
        fetch_data = query_result.fetchall()

        if len(fetch_data) == 0:
            return jsonify({
                "message": "This doctor doesn't have any reviews.",
                "error": 404,
                "success": False
            }), 404

        reviews_list = []
        for data in fetch_data:
            reviews_obg = {}
            reviews_obg.update({"name": data[2], "avatar": data[1], "stars": data[0], "comment": data[3]})
            reviews_list.append(reviews_obg)

        return jsonify({
            "reviews": reviews_list,
            "total_reviews": len(reviews_list),
            "success": True
        })
    except:
        abort(404)


# ______________ Update Avatar ______________
@app.route('/avatar', methods=['PATCH'])
@jwt_required()
def update_avatar():
    claims = get_jwt()
    try:
        status, result = get_images()
        if not status:
            return result

        avatar = result[0]
        current_user = ""

        if claims['is_doctor']:
            current_user = Doctor.query.get(claims['sub'])
        else:
            current_user = Patient.query.get(claims['sub'])

        current_user.update({"avatar": avatar})

        return jsonify({
            "message": "The avatar has been updated successfully",
            "success": True
        })
    except:
        abort(422)


# ______________ Model ______________

# Check the url of the model server is working or not.
def check(urls):
    if not len(urls):
        return None

    try:
        # http://127.0.0.1:5000/predict ==> http://127.0.0.1:5000
        url = "/".join(urls[0].split("/")[:-1])
        status_code = urllib.request.urlopen(url).getcode()

        # webUrl = urllib.request.urlopen(url)
        # data = webUrl.read()

        if status_code == 200:
            return urls

    except:
        urls.pop(0)
        check(urls)


def prediction(server_url, image_name):
    img_url = base_url + "static/" + image_name
    response = requests.post(server_url, json={"url": img_url})

    return response.json()


# Add model server url to the online server.
@app.route('/addurl', methods=['POST'])
def add_url():
    body = request.get_json()
    url = body.get('url', None)

    if url is None:
        abort(404)

    try:
        if not url in model_urls:
            model_urls.append(url)

        return jsonify({
            'success': True,
            'model_urls': [url for url in model_urls]
        })
    except BaseException:
        abort(422)


@app.route('/model/brain', methods=['POST'])
@jwt_required()
def get_result_from_brain_model():
    try:
        # Check on the image
        status, result = get_images()
        if not status:
            return result
        filename = result[0]

        # Check out the Model Server is running.
        print('---url before checking ---')
        print(model_urls)

        check(model_urls)
        print('--url after checking')
        print(model_urls)

        if len(model_urls) == 0:
            print("The Servers's Model is not wokring")
            return jsonify({
                "message": "The server's Model is not working",
                "error": 400,
                "success": False
            }), 400

        server_url = model_urls[0]

        # -------------------
        # Get the prediction based on image.
        prediction_result = prediction(server_url + "brain", filename)

        # return "True"
        return prediction_result
    except:
        abort(422)


@app.route('/model/covid19', methods=['POST'])
@jwt_required()
def get_result_from_covid19_model():
    try:
        # Check on the image
        status, result = get_images()
        if not status:
            return result
        filename = result[0]

        # Check out the Model Server is running.
        checking_result = check(model_urls)

        if len(model_urls) == 0:
            print("The Servers's Model is not wokring")
            return jsonify({
                "message": "The server's Model is not working",
                "error": 400,
                "success": False
            }), 400

        server_url = model_urls[0]

        # -------------------
        # Get the prediction based on image.
        prediction_result = prediction(server_url + "covid19", filename)

        # return "True"
        return prediction_result
    except:
        abort(422)


# ______________ Global Functions ______________

def create_appointments(sessions, is_doctor):
    current_date = datetime.now().strftime('%Y-%m-%d')

    future_appointments = []
    current_appointments = []
    previous_appointments = []

    if is_doctor:
        for current_session in sessions:
            if str(current_date) < str(current_session.date):
                future_appointments.append(current_session.format(False, is_doctor))
            elif str(current_date) == str(current_session.date):
                current_appointments.append(current_session.format(False, is_doctor))
            else:
                previous_appointments.append(current_session.format(False, is_doctor))

        future_appointments.sort(key=lambda e: e['date'])

        return [future_appointments, current_appointments, previous_appointments]

    else:
        for current_session in sessions:
            if str(current_date) < str(current_session.date):
                future_appointments.append(current_session.format(False, is_doctor))
            else:
                previous_appointments.append(current_session.format(False, is_doctor))

        future_appointments.sort(key=lambda e: e['date'])
        return [future_appointments, previous_appointments]


def get_images():
    try:
        if 'file' not in request.files:
            return [False, {
                "message": "You should send file in the body request",
                "error": 400,
                "success": False
            }]
        else:
            filenames = []
            uploaded_files = request.files.getlist("file")
            print(uploaded_files)
            for file in uploaded_files:
                if file.filename == '':
                    return [False, {
                        "message": "You should select a valid image(s)",
                        "error": 422,
                        "success": False
                    }], 422
                else:
                    filename = secure_filename(file.filename)
                    filename_extension = filename.split('.')
                    filename_extension = filename_extension[len(filename_extension) - 1]
                    if filename_extension not in app.config['UPLOAD_EXTENSIONS']:
                        return [False, {
                            "message": "The allowed extensions are ['jpg', 'jpeg', 'png', 'gif']",
                            "error": 422,
                            "success": False
                        }]

                    file.save(os.path.join(app.config["UPLOAD_PATH"], filename))

                    filenames.append(filename)
            return [True, filenames]
    except:
        abort(422)


'''
Create error handlers for all expected errors
including 404 and 422.
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable'
    }), 422


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized'
    }), 401


if __name__ == '__main__':
    app.run(debug=True)
