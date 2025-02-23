from database import db
from models import Category

def seed_categories():
    categories = [
        {'name': 'Technology'},
        {'name': 'Sports'},
        {'name': 'Politics'},
        {'name': 'Business'},
        {'name': 'Health'},
        {'name': 'Science/Tech'},
        {'name': 'World'},
        {'name': 'Entertainment'},
        {'name': 'Education'},
        {'name': 'Science/Nature'},
        {'name': 'Family'},
    ]

    try:
        # Add categories to the session
        for category_data in categories:
            category = Category(**category_data)
            db.session.add(category)

        # Commit the session to save changes to the database
        db.session.commit()
        print("Categories seeded successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding categories: {e}")
    finally:
        db.session.close()

if __name__ == '__main__':
    from app import create_app

    # Create the Flask app and initialize the database
    app = create_app()
    with app.app_context():
        seed_categories()