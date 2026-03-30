from flask_restx import Namespace,  Resource, fields
from http import HTTPStatus
from flask import request
from api.models.ticket_booking_model import TicketBooking, stationEnum, timeEnum, BookingStatusEnum, COACHES, CoachEnum
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date, datetime
from api.config.config import db


tickets_namespace = Namespace("Ticket", description = "Namespace for ticket booking operation")

booking_request = tickets_namespace.model(
    "BookingRequest",{
        "departure_date": fields.Date(required= True, description = "The date of departure in the format YYYY-MM-DD"),
        "depature_station": fields.String(required = True, description = "The station of depature"),
        "arrival_station": fields.String(required = True, description = "The station of arrival"),
        "departure_time": fields.String(required = True, description = "The time of departure, either Morning, Afternoon or Evening"),
        "passenger_class": fields.String(required= True, description = "The class  of travel, either First class, Business class or Standard class")
    }
)


booking_response = tickets_namespace.model(
    "Booking_Response",{
        "user_id": fields.Integer(),
        "departure_station": fields.String(),
        "arrival_station": fields.String(),
        "seat_number": fields.String(),
        "booking_status": fields.String(),
        "coach_id": fields.Integer()
    }
)


@tickets_namespace.route("/book")
class Booking(Resource):
    @jwt_required()
    @tickets_namespace.expect(booking_request)
    @tickets_namespace.marshal_with(booking_response, code = HTTPStatus.CREATED)
    def post(self):
        try:
            user_id = get_jwt_identity()
            data = request.get_json()
            departure_date_str = data.get("departure_date")#this is a string
            departure_date= datetime.strptime(departure_date_str, "%Y-%m-%d").date()
            departure_station = data.get("depature_station")
            arrival_station= data.get("arrival_station")
            departure_time= data.get("departure_time")
            passenger_class = data.get("passenger_class")



            if departure_station == arrival_station:
                return{"message": "Departure and arrival stations cannot be the same"}, HTTPStatus.BAD_REQUEST
            if departure_date < date.today():
                return {"message": "Departure date  cannot  be in the past"},HTTPStatus.BAD_REQUEST
            if departure_time not in timeEnum._value2member_map_:
                return {"message": "Invalid departure_time. Must be either Morning, Afternoon or Evening"},
            seat_number, coach_id  = COACHES.get_available_seats(CoachEnum(passenger_class), departure_date, departure_time)
        
            if not coach_id:
                return {"message": "No available seats for the selected class, date and time"}, HTTPStatus.BAD_REQUEST
            booking = TicketBooking(
                user_id =user_id,
                departure_time = timeEnum(departure_time),
                departure_date = departure_date,
                departure_station = stationEnum(departure_station),
                arrival_station = stationEnum(arrival_station),
                booking_status = BookingStatusEnum.BOOKED,
                seat_number = seat_number,
                coach_id = coach_id
            )
            db.session.add(booking)
            db.session.commit()

            return booking, HTTPStatus.CREATED
        except Exception as e:
            print("error is ",str(e))
            return({
                "status": "failure",
                "error": str(e)
            }), HTTPStatus.BAD_REQUEST

    @jwt_required()
    @tickets_namespace.marshal_list_with(booking_response, code = HTTPStatus.OK)
    def get(self):
        try:
            user_id = get_jwt_identity()
            bookings = TicketBooking.query.filter_by(user_id = user_id).all() 
            if not bookings:
                return {"message": "No bookings found for the user"}, HTTPStatus.NOT_FOUND
            return bookings, HTTPStatus.OK
        except  Exception as e:

            return {
                "status": "failure",
                "error": str(e)
            }

@tickets_namespace.route("/ticket/<int:id>")
class TicketById(Resource):
    @jwt_required()
    @tickets_namespace.marshal_with(booking_response, code = HTTPStatus.OK)
    def get(self, id):
            user= get_jwt_identity()
            booking =  TicketBooking.query.filter_by(id=id, user_id= user).first()
            if not booking:
                return {"message": "Ticket not found"}, HTTPStatus.NOT_FOUND
            return booking, HTTPStatus.OK