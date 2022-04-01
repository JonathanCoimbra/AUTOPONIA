from xmlrpc.client import boolean
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class PlantModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    flower = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Plant(name = {name}, origin = {origin}, height = {height}, weight = {weight}, flower = {flower})"

db.create_all()

plant_put_args = reqparse.RequestParser()
plant_put_args.add_argument("name", type=str, help="Name of the plant is required", required=True)
plant_put_args.add_argument("origin", type=str, help="Origin of the plant", required=True)
plant_put_args.add_argument("height", type=float, help="Height on the plant", required=True)
plant_put_args.add_argument("weight", type=float, help="Weight of the plant", required=True)
plant_put_args.add_argument("flower", type=bool, help="The plant has a flower?", required=True)

plant_update_args = reqparse.RequestParser()
plant_update_args.add_argument("name", type=str, help="Name of the plant is required")
plant_update_args.add_argument("origin", type=str, help="Origin of the plant")
plant_update_args.add_argument("height", type=float, help="Height on the plant")
plant_update_args.add_argument("weight", type=float, help="Weight of the plant")
plant_update_args.add_argument("flower", type=bool, help="The plant has a flower?")

resource_fields_plant = {
    'id': fields.Integer,
    'name': fields.String,
    'origin': fields.String,
    'height': fields.Float,
    'weight': fields.Float,
    'flower': fields.Boolean,
}

def abort_if_plant_id_doesnt_exist(plant_id):
    result = PlantModel.query.filter_by(id=plant_id).first()
    if not result:
        abort(404, message="Plant doesn't exist.")

def abort_if_plant_exists(plant_id):
    result = PlantModel.query.filter_by(id=plant_id).first()
    if result:
        abort(404, message="Plant already exists.")

class Plants(Resource):
    @marshal_with(resource_fields_plant)
    def get(self):
        result = PlantModel.query.all()
        if not result:
            abort(404, message="Could not find plant with that id.")
        return result

    @marshal_with(resource_fields_plant)
    def post(self):
        args = plant_put_args.parse_args()
        plant = PlantModel(
                    name=args['name'],
                    origin=args['origin'],
                    height=args['height'],
                    weight=args['weight'],
                    flower=args['flower'])
        db.session.add(plant)
        db.session.commit()
        return plant, 201

class Plant(Resource):
    @marshal_with(resource_fields_plant)
    def get(self, plant_id):
        result = PlantModel.query.filter_by(id=plant_id).first()
        if not result:
            abort(404, message="Could not find plant with that id.")
        return result

    @marshal_with(resource_fields_plant)
    def put(self, plant_id):
        args = plant_update_args.parse_args()
        abort_if_plant_id_doesnt_exist(plant_id)
        result = PlantModel.query.filter_by(id=plant_id).first()
        if args['name']:
            result.name = args['name']
        if args['origin']:
            result.origin = args['origin']
        if args['height']:
            result.height = args['height']
        if args['weight']:
            result.weight = args['weight']
        if args['flower']:
            result.flower = args['flower']
        db.session.commit()
        return result

    def delete(self, plant_id):
        abort_if_plant_id_doesnt_exist(plant_id)
        plant = PlantModel.query.filter_by(id=plant_id).first()
        db.session.delete(plant)
        db.session.commit()
        return '', 204