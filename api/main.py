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
	description = db.Column(db.String(1000),nullable=True)
	house_type = db.Column(db.Integer,nullable=False)
	location = db.Column(db.String(50),nullable=False)

	rooms = db.relationship('RoomModel', backref='house')

	def __repr__(self):
		return f"House (name = {name}, user id = {user_id}, description = {description},house_type = {house_type} location = {location})"

class RoomModel(db.Model):
	__tablename__ = "rooms"

	id = db.Column(db.Integer,primary_key=True)
	house_id = db.Column(db.Integer,db.ForeignKey("houses.id"))
	name = db.Column(db.String(50),nullable=False)
	surface_area = db.Column(db.Integer,nullable=True)

	def __repr__(self):
		return f"Room (name = {name}, surface_area = {surface_area})"

db.create_all()



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
house_put_args.add_argument("description", type=str,help="description of house is required",required=False)
house_put_args.add_argument("house_type", type=int,help="type of house is required",required=True)
house_put_args.add_argument("location", type=str,help="location of house is required",required=True)

house_update_args = reqparse.RequestParser()
house_update_args.add_argument("name", type=str,help="name of house is required",required=False)
house_update_args.add_argument("description", type=str,help="description of house is required",required=False)
house_update_args.add_argument("house_type", type=int,help="type of house is required",required=False)
house_update_args.add_argument("location", type=str,help="location of house is required",required=False)

house_fields = {
	"id" : fields.Integer,
	"user_id" : fields.Integer,
	"name" : fields.String,
	"description" : fields.String,
	"house_type" : fields.Integer,
	"location" : fields.String
}
class House(Resource):
	@marshal_with(house_fields)
	def put(self,user_id,house_id):
		result = HouseModel.query.filter_by(id=house_id).first()
		if result:
			abort(409,message="house id already exists")

		args = house_put_args.parse_args()
		house = HouseModel(id=house_id,user_id=int(user_id),name=args["name"],description=args["description"],house_type=args["house_type"],location=args["location"])
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
		if args["description"]:
			result.description = args["description"]
		if args["house_type"]:
			result.house_type = args["house_type"]
		if args["location"]:
			result.location = args["location"]

		db.session.commit()
		return result

##--ROOMS--------------------------------------------------


room_put_args = reqparse.RequestParser()
room_put_args.add_argument("name", type=str,help="name of room is required",required=True)
room_put_args.add_argument("surface_area", type=str,help="surface area of room is required",required=False)

room_update_args = reqparse.RequestParser()
room_update_args.add_argument("name", type=str,help="name of room is required",required=False)
room_update_args.add_argument("surface_area", type=str,help="surface area of room is required",required=False)

room_fields = {
	"id" : fields.Integer,
	"house_id" : fields.Integer,
	"name" : fields.String,
	"surface_area" : fields.Integer
}
class Room(Resource):
	@marshal_with(room_fields)
	def put(self,user_id,house_id,room_id):
		result = RoomModel.query.filter_by(id=room_id).first()
		if result:
			abort(409,message="room id already exists")

		args = room_put_args.parse_args()
		room = RoomModel(id=room_id,house_id=int(house_id),name=args["name"],surface_area=args["surface_area"])
		db.session.add(room)
		db.session.commit()
		return room, 201

	@marshal_with(room_fields)
	def get(self,user_id,house_id,room_id):
		result = RoomModel.query.filter_by(id=room_id).first()
		if not result:
			abort(404, message="Room does not exist")
		if result.house_id != int(house_id):
			abort(403, message="Cannot access this property")
		return result

	@marshal_with(room_fields)
	def patch(self,user_id,house_id,room_id):
		args = room_update_args.parse_args()
		result = RoomModel.query.filter_by(id=room_id).first()
		if not result:
			abort(404, message="Room does not exist")
		if result.house_id != int(house_id):
			print("result.houseid : "+result.house_id )
			print("house_id : "+house_id)
			abort(403, message="Cannot access this property")

		if args["name"]:
			result.name = args["name"]
		if args["surface_area"]:
			result.surface_area = args["surface_area"]

		db.session.commit()
		return result


##--BROWSER-------------------------------------------------------------------

class SearchResult():
	def __init__(self,name,description,house_type,location,last_name,first_name,rooms):
		self.name = name
		self.description = description
		self.house_type = house_type
		self.location = location
		self.last_name = last_name
		self.first_name = first_name
		self.rooms = rooms


room_fields_search = {
	"name" : fields.String,
	"surface_area" : fields.Integer	
}

search_result_fields = {
	"name" : fields.String,
	"description" : fields.String,
	"house_type" : fields.Integer,
	"location" : fields.String,
	"last_name" : fields.String,
	"first_name" : fields.String,
	"rooms" : fields.List(fields.Nested(room_fields_search))
}
class Search(Resource):
	@marshal_with(search_result_fields)
	def get(self,location):
		house_results = HouseModel.query.filter_by(location=location).all()
		print(len(house_results))
		results = []
		for result in house_results:
			print("house : " + result.name)
			owner = UserModel.query.filter_by(id=result.user_id).first()
			rooms = RoomModel.query.filter_by(house_id=result.id).all()
			search_result = SearchResult(result.name,result.description,result.house_type,result.location,owner.last_name,owner.first_name,rooms)
			results.append(search_result)



		if not results:
			abort(404, message="No results found")
		return results

##--ASSIGNMENTS-------------------------------------------------------------------

api.add_resource(User,"/user/<user_id>")
api.add_resource(House,"/user/<user_id>/<house_id>")
api.add_resource(Room,"/user/<user_id>/<house_id>/<room_id>")
api.add_resource(Search,"/browse/<location>")

if __name__ == "__main__":
    app.run(debug=True)