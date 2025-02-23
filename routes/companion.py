from flask import Blueprint, request, jsonify
from models import Companion
from database import db

companion_bp = Blueprint('companion', __name__)

@companion_bp.route('/api/companions', methods=['GET'])
def get_companions():
    companions = Companion.query.all()
    return jsonify([{
        'id': companion.id,
        'name': companion.name,
        'description': companion.description,
        'instructions': companion.instructions,
        'seed': companion.seed,
        'src': companion.src,
        'category_id': companion.category_id,
        'created_at': companion.created_at.isoformat()
    } for companion in companions])

@companion_bp.route('/api/companions/<int:id>', methods=['GET'])
def get_one_companion(id):
    companion = Companion.query.get_or_404(id)
    messages = [{
        'id': message.id,
        'content': message.content,
        'role': message.role,
        'created_at': message.created_at.isoformat()
    } for message in companion.messages]
    
    return jsonify({
        'id': companion.id,
        'name': companion.name,
        'description': companion.description,
        'instructions': companion.instructions,
        'seed': companion.seed,
        'src': companion.src,
        'category_id': companion.category_id,
        'created_at': companion.created_at.isoformat(),
        'messages': messages
    })



@companion_bp.route('/api/companion', methods=['POST'])
def create_companion():
    data = request.get_json()
    new_companion = Companion(
        name=data['name'],
        description=data['description'],
        instructions=data['instructions'],
        seed=data['seed'],
        src=data['src'],
        category_id=data.get('category_id')  # Make it optional
    )
    db.session.add(new_companion)
    db.session.commit()
    return jsonify({'message': 'Companion created successfully!'}), 201

@companion_bp.route('/api/companion/<int:id>', methods=['GET'])
def get_companion(id):
    companion = Companion.query.get_or_404(id)
    return jsonify({
        'id': companion.id,
        'name': companion.name,
        'description': companion.description,
        'instructions': companion.instructions,
        'seed': companion.seed,
        'src': companion.src
    })

@companion_bp.route('/api/companion/<int:id>', methods=['PATCH'])
def update_companion(id):
    companion = Companion.query.get_or_404(id)
    data = request.get_json()
    companion.name = data.get('name', companion.name)
    companion.description = data.get('description', companion.description)
    companion.instructions = data.get('instructions', companion.instructions)
    companion.seed = data.get('seed', companion.seed)
    companion.src = data.get('src', companion.src)
    companion.category_id = data.get('category_id', companion.category_id)
    db.session.commit()
    return jsonify({'message': 'Companion updated successfully!'})

@companion_bp.route('/api/companion/<int:id>', methods=['DELETE'])
def delete_companion(id):
    companion = Companion.query.get_or_404(id)
    db.session.delete(companion)
    db.session.commit()
    return jsonify({'message': 'Companion deleted successfully!'})