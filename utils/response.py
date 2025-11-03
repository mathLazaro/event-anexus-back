from flask import jsonify, url_for


def response_created(resource_name: str, resource_id: int, mensagem="Created successfully"):
    bp_name = f"{resource_name}_bp.get_{resource_name}"
    id_kwargs = {f"{resource_name}_id": resource_id}
    location = url_for(bp_name, **id_kwargs, _external=True)
    return jsonify({
        "message": mensagem,
        "id": resource_id,
        "url": location
    }), 201, {"Location": location}


def response_resource(data):
    return jsonify(data), 200
