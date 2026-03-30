from flask_restx import Namespace, Resource, fields
from flask import request
from api.models.user_model import User, IdEnum, GenderEnum
from http import HTTPStatus
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity


auth_namespace= Namespace("Auth", description="Namespace for authentication")

signup_model = auth_namespace.model(
    "SignupRequest",{
    "first_name": fields.String(required=True, description = "First name"),
    "last_name": fields.String(required= True, description= "Last name"),
    "email": fields.String(required= True, description= "The email of the user"),
    "password":fields.String(required= True, description= "A very strong password"),
    "gender": fields.String(required= True, description= "Male or Female"),
    "phone": fields.String(required= True, description= "The telephone of the user"),
    "id_type": fields.String(required= True, description= "Type means of identification provided"),
    "id_number": fields.String(required= True, description= "The number on the means of identification"),
    }
)

signup_response= auth_namespace.model(
    "SignupResponse",{
    "id": fields.Integer(),
    "first_name": fields.String(),
    "last_name": fields.String(),
    "email": fields.String(),
    "gender": fields.String(),
    "phone": fields.String(),
    "id_type": fields.String(),
    "id_number": fields.String(),
    "created_at":fields.String()

    }
)


@ auth_namespace.route("/signup")
class Signup(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(signup_response, code=HTTPStatus.CREATED)
    def post (self):
        try:
            data = request.get_json()
            first_name= data.get("first_name")
            last_name= data.get("last_name")
            email= data.get("email")
            password= data.get("password")
            gender= (data.get("gender") or "").strip().lower()
            print(gender)
            phone = data.get("phone")
            id_type= (data.get("id_type") or "").strip().lower()
            id_number=data.get("id_number")


            email_check = User.query.filter_by(email=email).first()
            id_check = User.query.filter_by(id_number=id_number).first()
             

    
            #This is to check if email already exsists
            if email_check:
                return {"message":"Email already exsists" }, HTTPStatus.CONFLICT
        
            if id_check:
                return{"message": "Id_number provided already exsists"}, HTTPStatus.CONFLICT
            if gender not in(g.value for g in GenderEnum):
                return {"message": "invalid gender"}, HTTPStatus.BAD_REQUEST

            if id_type not in (i.value for i in IdEnum):
                return {"message": "invalid id_type"}, HTTPStatus.BAD_REQUEST

        
            new_user = User(
                first_name= first_name,
            last_name= last_name,
            email= email,
            password = generate_password_hash(password),
            gender= gender,
            phone = phone,
            id_type= id_type,
            id_number= id_number
            )

            new_user.save()

            return new_user, HTTPStatus.CREATED
    
        except Exception as e:
            print(str(e))
            return ({
            "status": "failure",
            "error": str(e)
                }), HTTPStatus.BAD_REQUEST  
        
login_request= auth_namespace.model(
    "LoginRequest",{
        "email": fields.String(required=True, description = "A registered email"),
        "password": fields.String(required= True, description= "A registered password")
    }
)

login_response= auth_namespace.model(
    "LoginResponse", {
        "message": fields.String(),
        "access_token": fields.String(),
        "refresh_token": fields.String()
    }
)
@auth_namespace.route("/login")
class Login(Resource):

    @auth_namespace.expect(login_request)
    @auth_namespace.marshal_with(login_response)
    def post(self):
        try:
            data = request.get_json()
            email=data.get("email")
            password = data.get("password")
            user_check = User.query.filter_by(email=email).first()
            if user_check and check_password_hash(user_check.password, password):
                access_token = create_access_token(identity=str(user_check.id))
                refresh_token = create_refresh_token(identity=str(user_check.id))
                return {
                    "message": "Login succesfully",
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            return {
                "message": "Invalid email or password"
            }
        except Exception as e:
            return ({
                "status": "failure",
                "error": str(e)
            }), HTTPStatus.BAD_REQUEST
        

            
@auth_namespace.route("/refresh")
class refresh(Resource):
    @jwt_required(refresh= True)
    def post(self):
        user_id= get_jwt_identity()
        access_token = create_access_token(identity=str(user_id))
        refresh_token = create_refresh_token(identity=str(user_id))
        return {
            "message": "refresh succesful",
            "access_token": refresh_token
        }