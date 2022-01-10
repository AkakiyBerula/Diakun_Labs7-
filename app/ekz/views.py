from flask import Flask, g, request, jsonify
from functools import wraps
from ..contract_activities.models import Contractypes, Contracts
from ..auth.models import User
from .. import db
from datetime import datetime

from . import api_ekz_blueprint

api_username = 'TonyDAngelo'
api_password = 'Caleb_konley_WithAK'


def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == api_username and auth.password == api_password:
            return f(*args, **kwargs)
        return jsonify({'message': 'Authentication failed!'}), 403

    return decorated


@api_ekz_blueprint.route('/contractypes', methods=['GET'])
@protected
def get_categories():
    categories = Contractypes.query.all()
    return_values = [{"id": category.type_id, "name": category.type} for category in categories]

    return jsonify({'categories': return_values})


@api_ekz_blueprint.route('/contractypes/<int:id>', methods=['GET'])
@protected
def get_category(id):
    category = Contractypes.query.get_or_404(id)
    return jsonify({"id": category.type_id, "name": category.type})


@api_ekz_blueprint.route('/contractypes', methods=['POST'])
def add_category():
    new_category = request.get_json()
    print(new_category)
    category = Contractypes.query.filter_by(name = new_category['name']).first()

    if category:
        return jsonify({"Message": "Category has already existed!"})

    category = Contractypes(name = new_category['name'])
    db.session.add(category)
    db.session.commit()
    return jsonify({"id": category.id, "name": category.name})


@api_ekz_blueprint.route('/contractypes/<int:id>', methods=['PUT', 'PATCH'])
@protected
def edit_category(id):
    category = Contractypes.query.get(id)
    if not category:
        return jsonify({"Message": "Category doesn't exist!"})

    update_category = request.get_json()
    categories = Contractypes.query.filter_by(name=update_category['type']).first()
    if categories:
        return jsonify({"Message": "Category has already existed!"})

    category.type = update_category['type']
    db.session.add(category)
    db.session.commit()

    return jsonify({"id": category.type_id, "name": category.type})


@api_ekz_blueprint.route('/contractypes/<int:id>', methods=['DELETE'])
@protected
def delete_category(id):
    category = Contractypes.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()

    return jsonify({'Message': 'Category has been removed!'})

@api_ekz_blueprint.route('/contracts', methods=['GET'])
@protected
def get_contracts():
    contracts = Contracts.query.all()
    #contract_type = Contractypes.query.get_or_404(contracts.contract_type)
    return_values = [
        {"id": contract.id, 
        "contract_code": contract.contract_code,
        "organization_name": contract.organization_name,
        "deadline": contract.deadline,
        "contract_amount": contract.contract_amount,
        "contract_type": contract.contract_type,
        "user_id" : contract.user_id} for contract in contracts]
    print(return_values)
    return jsonify({'contracts': return_values})


@api_ekz_blueprint.route('/contracts/<int:id>', methods=['GET'])
@protected
def get_contract(id):
    contract = Contracts.query.get_or_404(id)
    contract_type = Contractypes.query.get_or_404(contract.contract_type)

    return jsonify({"id": contract.id, 
        "contract_code": contract.contract_code,
        "organization_name": contract.organization_name,
        "deadline": contract.deadline,
        "contract_amount": contract.contract_amount,
        "contract_type": contract_type.type_id,
        "user_id" : contract.user_id}
    )


@api_ekz_blueprint.route('/contracts', methods=['POST'])
def add_contract():
    new_contract = request.get_json()
    contract = Contracts.query.filter_by(contract_code = new_contract['contract_code']).first()
    
    if contract:
        return jsonify({"Message": "Contract has already existed!"})
    
    category = Contractypes.query.filter_by(type_id = new_contract['contract_type'])

    if not category:
        return jsonify({"Message": "Category doesn't exist"})

    auth = request.authorization
    user = User.query.filter_by(username = auth.username).first()
    if not user:
        return jsonify({"Message": "User doesn't found in database"})
    contract = Contracts(contract_code = new_contract["contract_code"], 
                            organization_name = new_contract["organization_name"],
                            deadline = datetime.strptime(new_contract["deadline"], "%m %d %Y"),
                            contract_amount = new_contract["contract_amount"],
                            contract_type = new_contract["contract_type"],
                            user_id = user.id)
    db.session.add(contract)
    db.session.commit()
    return jsonify(
        {"id": contract.id, 
        "contract_code": contract.contract_code,
        "organization_name": contract.organization_name,
        "deadline": contract.deadline,
        "contract_amount": contract.contract_amount,
        "contract_type": contract.contract_type,
        "user_id" : contract.user_id}
    )


@api_ekz_blueprint.route('/contracts/<int:id>', methods=['PUT', 'PATCH'])
@protected
def edit_contract(id):

    edit_contract = request.get_json()
    contract = Contracts.query.filter_by(id = id).first()
    if not contract:
        return jsonify({"Message": "Contract doesn't exist!"})

    auth = request.authorization
    user = User.query.filter_by(username = auth.username).first()

    category = Contractypes.query.filter_by(type_id = edit_contract['contract_type'])
    if not category:
        return jsonify({"Message": "Category doesn't exist"})

    if not user:
        return jsonify({"Message": "User doesn't found in database"})
    elif user.id != contract.user_id:
        return jsonify({"Message": "This is not your contract! You can't update this"})

    print(str(edit_contract['deadline']))
    new_contract = []
    contract.contract_code = edit_contract['contract_code']
    contract.organization_name = edit_contract['organization_name']
    contract.deadline = datetime.strptime(edit_contract["deadline"], "%m %d %Y")
    contract.contract_amount = edit_contract['contract_amount']
    contract.contract_type = edit_contract['contract_type']
    db.session.add(contract)
    db.session.commit()

    return jsonify({"id": contract.id, 
        "contract_code": contract.contract_code,
        "organization_name": contract.organization_name,
        "deadline": edit_contract["deadline"],
        "contract_amount": contract.contract_amount,
        "contract_type": contract.contract_type,
        "user_id" : contract.user_id
    })


@api_ekz_blueprint.route('/contracts/<int:id>', methods=['DELETE'])
@protected
def delete_contract(id):
    contract = Contracts.query.get(id)
    if not contract:
        return jsonify({"Message": "Contract doesn't exist in database!"})
    auth = request.authorization
    user = User.query.filter_by(username = auth.username).first()
    if not user:
        return jsonify({"Message": "User doesn't found in database!"})
    elif user.id != contract.user_id:
        return jsonify({"Message": "This is not your contract! You can't delete this!"})
    
    db.session.delete(contract)
    db.session.commit()

    return jsonify({'Message': 'Contract has been deleted!'})