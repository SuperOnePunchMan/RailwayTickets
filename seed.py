
from api import create_app
from api.config.config import db
from api.models.ticket_booking_model import COACHES, CoachEnum


def seed_coaches():
    coaches = [
        {"coach_number": "C1", "coach_type": CoachEnum.FIRST_CLASS, "capacity":25},
        {"coach_number": "C2", "coach_type": CoachEnum.FIRST_CLASS, "capacity":25},
        {"coach_number": "C3", "coach_type": CoachEnum.BUSINESS_CLASS, "capacity": 50},
        {"coach_number": "C4", "coach_type": CoachEnum.BUSINESS_CLASS, "capacity": 50},
        {"coach_number": "C5", "coach_type": CoachEnum.STANDARD_CLASS, "capacity": 150 },
        {"coach_number": "C6", "coach_type": CoachEnum.STANDARD_CLASS, "capacity": 150 },
        {"coach_number": "C7", "coach_type": CoachEnum.STANDARD_CLASS, "capacity": 150 } 


    ]

    for data in coaches:
        exsisting = COACHES.query.filter_by(coach_number=data["coach_number"]).first()
        if not exsisting:
            coach = COACHES(coach_number=data["coach_number"], coach_type=data["coach_type"], capacity=data["capacity"])
            db.session.add(coach)

    db.session.commit()
    print("Seeded coaches")

def run_seed():
    app = create_app()
    with app.app_context():
        db.create_all()
        seed_coaches()

if __name__ == "__main__":
    run_seed()