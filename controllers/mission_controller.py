from flask import Blueprint, jsonify
from services import mission_service

mission_blueprint = Blueprint('mission_controller', __name__)


@mission_blueprint.route("/", methods=['GET'])
def list_missions_endpoint():
    result = mission_service.get_all_missions_service()
    return (result.map(lambda missions: (jsonify(missions), 200))
            .value_or((jsonify({"error": "Failed to retrieve missions"}), 400)))


@mission_blueprint.route("/<int:mission_id>", methods=['GET'])
def get_mission_by_id_endpoint(mission_id):
    result = mission_service.get_mission(mission_id)
    return (result.map(lambda mission: (jsonify(mission), 200))
            .value_or((jsonify({"error": "Mission not found"}), 404)))
