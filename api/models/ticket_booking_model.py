from api.config.config import db
from enum import Enum


class stationEnum(str,Enum):
    Abuja = "Abuja"
    LAGOS = "Lagos"
    KANGO = "Kango"
    PORT_HARCOURT = " Port Harcourt"
    Enugu = "Enugu"

class timeEnum(str, Enum):
    MORNING = "Morning"
    AFTERNOON = "Afternoon"
    EVENING = "Evening"

class BookingStatusEnum(str, Enum):
    BOOKED = "Booked"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"


class TicketBooking(db.Model):
    __tablename__ = "ticket_booking"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    departure_station = db.Column(db.Enum(stationEnum), nullable = False)
    arrival_station = db.Column(db.Enum(stationEnum), nullable = False)
    departure_date = db.Column(db.Date, nullable = False)
    departure_time = db.Column(db.Enum(timeEnum), nullable = False)
    booking_status = db.Column(db.Enum(BookingStatusEnum), nullable = False)
    seat_number = db.Column(db.String(), nullable = False)
    coach_id = db.Column(db.Integer(), db.ForeignKey("coaches.id"), nullable = False)
    user = db.relationship("User", backref= db.backref("ticket_booking", lazy = True))


class CoachEnum(str, Enum):
    FIRST_CLASS = "First class"
    BUSINESS_CLASS = "Business class"
    STANDARD_CLASS = "Standard class"

class COACHES(db.Model):
    __tablename__ = "coaches"
    id = db.Column(db.Integer, primary_key = True)
    coach_number = db.Column(db.String(), nullable = False)
    coach_type = db.Column(db.Enum(CoachEnum), nullable = False)
    capacity = db.Column(db.Integer, nullable = False)
    booking = db.relationship("TicketBooking", backref = db.backref("coaches"), lazy = True)


    @staticmethod
    def get_available_seats(passengerClass: CoachEnum, travel_date, travel_time: timeEnum):
        all_coaches = COACHES.query.filter_by(coach_type=passengerClass).all()
        for coach in all_coaches:
            taking_seats = TicketBooking.query.filter_by(coach_id=coach.id, departure_date= travel_date, departure_time = travel_time, booking_status = BookingStatusEnum.BOOKED).all()

            taken_seat_list = [seat[0] for seat in taking_seats]

            for i in range(1, coach.capacity + 1):
                prefix = coach.coach_type.value[0].upper()
                seat_number = f"{prefix}/{i}"
                if seat_number not in taken_seat_list:
                    return  seat_number, coach.id
        return None, None