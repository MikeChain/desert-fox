from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import AlreadyExistsError, DatabaseError
from app.extensions import db
from app.models import CategoriesModel


class CategoriesService:
    def __init__(self):
        self.model = CategoriesModel

    def get_all_categories(self):
        return self.model.query.all()

    def get_all_categories_by_type(self, type):
        return self.model.query.filter_by(type=type).all()

    def get_category(self, category_id):
        return self.model.query.filter_by(id=category_id).first()

    def get_category_by_name(self, category_name):
        return self.model.query.filter_by(name=category_name).first()

    def create_category(self, category_data):
        category = self.get_category_by_name(
            category_name=category_data["name"]
        )

        if category:
            raise AlreadyExistsError("Category already exists.")

        category = self.model(**category_data)

        try:
            db.session.add(category)
            db.session.commit()
        except SQLAlchemyError:
            raise DatabaseError

        return category

    def update_category(self, category_data, category_id):
        category = self.get_category(category_id)

        if "name" in category_data:
            category.name = category_data["name"]

        if "description" in category_data:
            category.description = category_data["description"]

        try:
            db.session.add(category)
            db.session.commit()
        except SQLAlchemyError:
            raise DatabaseError

        return category
