from dictalchemy import asdict
from flask import Blueprint, request, jsonify
from services import target_service as ts

target_blueprint = Blueprint('target_controller', __name__)


@target_blueprint.route("/create", methods=['POST'])
def create_target_endpoint():
    result = ts.create_target(request.json)
    return (result.map(lambda t: (jsonify(t), 201))
            .value_or((jsonify({"error": "Invalid input or target creation failed"}), 400)))


@target_blueprint.route("/update/<int:target_id>", methods=['PUT'])
def update_target_endpoint(target_id):
    result = ts.update_target(target_id, request.json)
    return (result.map(lambda t: (jsonify(t), 200))
            .value_or((jsonify({"error": "Target not found or update failed"}), 400)))


@target_blueprint.route("/delete/<int:target_id>", methods=['DELETE'])
def delete_target_endpoint(target_id):
    result = ts.delete_target(target_id)
    return (result.map(lambda _: ("", 204))
            .value_or((jsonify({"error": "Target not found or deletion failed"}), 400)))

@target_blueprint.route("/<int:target_id>", methods=['GET'])
def get_target_endpoint(target_id):
    return ts.get_target_by_id(target_id).map(
        lambda target: (jsonify(asdict(target)), 200)
    ).value_or((jsonify({"error": "Target not found"}), 404))


@target_blueprint.route("/", methods=['GET'])
def list_targets_endpoint():
    industry = request.args.get('industry')
    priority = request.args.get('priority')

    if industry:
        result = ts.get_targets_by_industry_pattern(industry)
    elif priority:
        try:
            result = ts.get_targets_by_priority(int(priority))
        except ValueError:
            return jsonify({"error": "Invalid priority value"}), 400
    else:
        result = ts.get_all_targets()

    return (result.map(lambda targets: (jsonify(ts.serialize_targets(targets)), 200))
            .value_or((jsonify({"error": "Failed to retrieve targets"}), 400)))
