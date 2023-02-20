import uuid

from flask_smorest import abort
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import AlreadyExistsError, DatabaseError, ResourceInUseError
from app.extensions import db
from app.models import CategoriesModel
from app.models.subcategories import SubcategoriesModel


class CategoriesService:
    def __init__(self):
        self.model = CategoriesModel
        self.subs = SubcategoriesModel

    def get_subcategories(self, category_id) -> list[SubcategoriesModel]:
        return self.subs.query.filter_by(category_id=category_id).all()

    def get_all_categories(self):
        return self.model.query.all()

    def get_all_categories_by_type(self, type):
        return self.model.query.filter_by(type=type).all()

    def get_category(self, category_id):
        category = self.model.query.filter_by(id=category_id).first()
        if not category:
            abort(404, message="This is not the category you are looking for.")
        return category

    def get_category_by_name(self, category_name):
        return self.model.query.filter_by(name=category_name).first()

    def create_category(self, category_data):
        category = self.get_category_by_name(
            category_name=category_data["name"]
        )

        if category:
            raise AlreadyExistsError("Category already exists.")

        if "id" in category_data:
            category_data["id"] = uuid.UUID(category_data["id"]).hex

        category = self.model(**category_data)

        try:
            db.session.add(category)
            db.session.commit()
        except SQLAlchemyError:
            raise DatabaseError

        return category

    def update_category(self, category_data, category_id):
        category = self.get_category_by_name(
            category_name=category_data["name"]
        )

        if category and category.id != category_id:
            raise AlreadyExistsError("Category already exists.")

        if not category:
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

    def delete_category(self, category_id) -> bool:
        category = self.get_category(category_id)

        subcategories = self.get_subcategories(category_id)

        if len(subcategories) > 0:
            raise ResourceInUseError

        try:
            db.session.delete(category)
            db.session.commit()
        except SQLAlchemyError:
            raise DatabaseError

        return True
