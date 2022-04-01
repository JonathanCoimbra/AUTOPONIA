from xmlrpc.client import boolean
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from plant import PlantModel, Plant, Plants, plant_put_args, plant_update_args, abort_if_plant_exists, abort_if_plant_id_doesnt_exist, resource_fields_plant
from watercan import WaterCanModel, WaterCan, WaterCans, watercan_put_args, watercan_update_args, abort_if_watercan_exists, abort_if_watercan_id_doesnt_exist, resource_fields_watercan

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
db.create_all()

api.add_resource(Plant, "/plant/<int:plant_id>")
api.add_resource(Plants, "/plant")
api.add_resource(WaterCan, "/watercan/<int:watercan_id>")
api.add_resource(WaterCans, "/watercan")

if __name__ == "__main__":
    app.run(debug = True)