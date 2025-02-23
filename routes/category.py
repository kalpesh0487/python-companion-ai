from flask import Blueprint, request, jsonify
from models import Category
from database import db

category_bp = Blueprint('category', __name__)

@category_bp.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': category.id,
        'name': category.name
    } for category in categories])

@category_bp.route('/api/category', methods=['POST'])
def create_category():
    data = request.get_json()
    new_category = Category(
        name=data['name']
    )
    db.session.add(new_category)
    db.session.commit()
    return jsonify({
        'id': new_category.id,
        'name': new_category.name
    }), 201
