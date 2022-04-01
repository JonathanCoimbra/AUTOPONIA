from xmlrpc.client import boolean
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class WaterCanModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    volume = db.Column(db.Float, nullable=False)
    power = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Water Can(volume = {volume}, power = {power})"

db.create_all()

watercan_put_args = reqparse.RequestParser()
watercan_put_args.add_argument("volume", type=float, help="Volume of the watercan", required=True)
watercan_put_args.add_argument("power", type=float, help="Power of the watercan", required=True)

watercan_update_args = reqparse.RequestParser()
watercan_update_args.add_argument("volume", type=float, help="Volume of the watercan")
watercan_update_args.add_argument("power", type=float, help="Power of the watercan")

resource_fields_watercan = {
    'id': fields.Integer,
    'volume': fields.Float,
    'power': fields.Float,
}

def abort_if_watercan_id_doesnt_exist(watercan_id):
    result = WaterCanModel.query.filter_by(id=watercan_id).first()
    if not result:
        abort(404, message="Water Can doesn't exist.")

def abort_if_watercan_exists(watercan_id):
    result = WaterCanModel.query.filter_by(id=watercan_id).first()
    if result:
        abort(404, message="Water Can already exists.")

class WaterCans(Resource):
    @marshal_with(resource_fields_watercan)
    def get(self):
        result = WaterCanModel.query.all()
        if not result:
            abort(404, message="Could not find water can with that id.")
        return result

    @marshal_with(resource_fields_watercan)
    def post(self):
        args = watercan_put_args.parse_args()
        watercan = WaterCanModel(
                    volume=args['volume'],
                    power=args['power'])
        db.session.add(watercan)
        db.session.commit()
        return watercan, 201

class WaterCan(Resource):
    @marshal_with(resource_fields_watercan)
    def get(self, watercan_id):
        result = WaterCanModel.query.filter_by(id=watercan_id).first()
        if not result:
            abort(404, message="Could not find watercan with that id.")
        return result

    @marshal_with(resource_fields_watercan)
    def put(self, watercan_id):
        args = watercan_update_args.parse_args()
        abort_if_watercan_id_doesnt_exist(watercan_id)
        result = WaterCanModel.query.filter_by(id=watercan_id).first()
        if args['volume']:
            result.volume = args['volume']
        if args['power']:
            result.power = args['power']
        db.session.commit()
        return result

    def delete(self, watercan_id):
        abort_if_watercan_id_doesnt_exist(watercan_id)
        watercan = WaterCanModel.query.filter_by(id=watercan_id).first()
        db.session.delete(watercan)
        db.session.commit()
        return '', 204