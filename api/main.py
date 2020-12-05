from flask import Flask,request
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class UserModel(db.Model):
	__tablename__ = "users"

	id = db.Column(db.Integer,primary_key=True)
	last_name = db.Column(db.String(50),nullable=False)
	first_name = db.Column(db.String(50),nullable=False)
	date_of_birth = db.Column(db.String(10),nullable = False)

	houses = db.relationship('HouseModel', backref='owner')

	def __repr__(self):
		return f"User (last_name = {last_name}, first_name = {first_name}, date_of_birth = {date_of_birth})"

class HouseModel(db.Model):
	__tablename__ = "houses"

	id = db.Column(db.Integer,primary_key=True)
	user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
	name = db.Column(db.String(50),nullable=False)
	location = db.Column(db.String(50),nullable=False)

	def __repr__(self):
		return f"House (name = {name}, user id = {user_id}, location = {location})"

# class RoomsModel(db.Model):
# 	__tablename__ = "rooms"

# 	id = db.Column(db.Integer,primary_key=True)
# 	fk = db.Column(db.Integer,db.ForeignKey("houses.id"))
# 	name = db.Column(db.String(50),nullable=False)
# 	surface_area = db.Column(db.Integer,nullable=True)

# 	def __repr__(self):
# 		return f"Room (name = {name}, surface_area = {surface_area})"

db.create_all()

##


# house_put_args = reqparse.RequestParser()
# house_put_args.add_argument("house", type=str,help="Name of house required",required=True)

# house_resource_fields = {
# 	"id" : fields.Integer,
# 	"user_id" : fields.Integer,
# 	"name" : fields.String,
# 	"location" : fields.String,
# 	"surface_area" : fields.Integer,
# }
# class HouseExplorer(Resource):
# 	@marshal_with(house_resource_fields)
# 	def get(self,name):
# 		results = HousesModel.query.filter_by(name=name)
# 		return results

# class User(Resource):
# 	def put(self,user_id):
# 		args = house_put_args.parse_args()
# 		return {user_id : args}

##--USER----------------------------------------------------------------------

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("last_name", type=str,help="Family name of user required",required=True)
user_put_args.add_argument("first_name", type=str,help="First name of user required",required=True)
user_put_args.add_argument("date_of_birth", type=str,help="Date of birth of user required",required=True)

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("last_name", type=str,help="Family name of user required",required=False)
user_update_args.add_argument("first_name", type=str,help="First name of user required",required=False)
user_update_args.add_argument("date_of_birth", type=str,help="Date of birth of user required",required=False)

user_fields = {
	"id" : fields.Integer,
	"last_name" : fields.String,
	"first_name" : fields.String,
	"date_of_birth" : fields.String
}
class User(Resource):
	@marshal_with(user_fields)
	def put(self,user_id):
		result = UserModel.query.filter_by(id=user_id).first()
		if result:
			abort(409,message="User id already exists")

		args = user_put_args.parse_args()
		user = UserModel(id=user_id,last_name=args["last_name"],first_name=args["first_name"],date_of_birth=args["date_of_birth"])
		db.session.add(user)
		db.session.commit()
		return user, 201

	@marshal_with(user_fields)
	def get(self,user_id):
		result = UserModel.query.filter_by(id=user_id).first()
		if not result:
			abort(404, message="User does not exist")
		return result

	@marshal_with(user_fields)
	def patch(self,user_id):
		args = user_update_args.parse_args()
		result = UserModel.query.filter_by(id=user_id).first()
		if not result:
			abort(404, message="User does not exist")

		if args["first_name"]:
			result.first_name = args["first_name"]
		if args["last_name"]:
			result.last_name = args["last_name"]
		if args["date_of_birth"]:
			result.date_of_birth = args["date_of_birth"]

		db.session.commit()
		return result
		

##--HOUSE--------------------------------------------------------------

house_put_args = reqparse.RequestParser()
house_put_args.add_argument("name", type=str,help="name of house is required",required=True)
house_put_args.add_argument("location", type=str,help="location of house is required",required=True)

house_update_args = reqparse.RequestParser()
house_update_args.add_argument("name", type=str,help="name of house is required",required=False)
house_update_args.add_argument("location", type=str,help="location of house is required",required=False)

house_fields = {
	"id" : fields.Integer,
	"user_id" : fields.Integer,
	"name" : fields.String,
	"location" : fields.String,
}
class House(Resource):
	@marshal_with(house_fields)
	def put(self,user_id,house_id):
		print(user_id)
		result = HouseModel.query.filter_by(id=house_id).first()
		if result:
			abort(409,message="house id already exists")

		args = house_put_args.parse_args()
		house = HouseModel(id=house_id,user_id=int(user_id),name=args["name"],location=args["location"])
		db.session.add(house)
		db.session.commit()
		return house, 201

	@marshal_with(house_fields)
	def get(self,user_id,house_id):
		result = HouseModel.query.filter_by(id=house_id).first()
		if not result:
			abort(404, message="House does not exist")
		if result.user_id != int(user_id):
			abort(403, message="Cannot access this property")
		return result

	@marshal_with(house_fields)
	def patch(self,user_id,house_id):
		args = house_update_args.parse_args()
		result = HouseModel.query.filter_by(id=house_id).first()
		if not result:
			abort(404, message="House does not exist")
		if result.user_id != int(user_id):
			print("result.userid : "+result.user_id )
			print("user_id : "+user_id)
			abort(403, message="Cannot access this property")

		if args["name"]:
			result.name = args["name"]
		if args["location"]:
			result.location = args["location"]

		db.session.commit()
		return result

##--BROWSER-------------------------------------------------------------------


class Search(Resource):
	@marshal_with(house_fields)
	def get(self,location):
		result = HouseModel.query.filter_by(location=location).all()
		if not result:
			abort(404, message="No results found")
		return result

##--ASSIGNMENTS-------------------------------------------------------------------

api.add_resource(User,"/user/<user_id>")
api.add_resource(House,"/user/<user_id>/<house_id>")
api.add_resource(Search,"/browse/<location>")

if __name__ == "__main__":
    app.run(debug=True)