from flask import Flask
from flask_restx import Api
from api.controllers.tickets_booking import tickets_namespace
from api.config.config import config_dict, db
from api.controllers.auth import auth_namespace
from api.models.user_model import User
from api.models.ticket_booking_model import TicketBooking, COACHES
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


def create_app(config= config_dict["dev"]):
    app = Flask(__name__)
    app.config.from_object(config)
    Authorizations = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Add a JWT with **Bearer &lt; JWTgt; to authorize **"
        }
    }
    api = Api(app=app,
              version= "v1.0",
              title="Railway Ticket Api",
              description= "A ticket booking system API railway management",
              authorizations= Authorizations,
              security= ["Bearer Auth"],
              prefix= "/api/v1")
    db.init_app(app)
    migrate = Migrate(app,db)
    JWTManager(app)
    api.add_namespace(tickets_namespace, path="/tickets")
    api.add_namespace(auth_namespace, path="/auth")


    @app.shell_context_processor
    def make_shell_context():
        return {
            "db":db,
            "Users":User,
            "tickets": TicketBooking,
            "coaches": COACHES
        }
    return app