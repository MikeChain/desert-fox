from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import AlreadyExistsError, DatabaseError
from app.extensions import db
from app.models import SubcategoriesModel


class SubcategoriesService:
    def __init__(self):
        self.model = SubcategoriesModel

    def get_all_subcategories(self):
        return self.model.query.all()

    def get_all_subcategories_by_category(self, category_id):
        return self.model.query.filter_by(category_id=category_id).all()

    def get_subcategory(self, subcategory_id):
        return self.model.query.filter_by(id=subcategory_id).first()

    def get_subcategory_by_name(self, subcategory_name):
        return self.model.query.filter_by(name=subcategory_name).first()

    def create_subcategory(self, subcategory_data):
        subcategory = self.get_subcategory_by_name(
            subcategory_name=subcategory_data["name"]
        )

        if subcategory:
            raise AlreadyExistsError("Subcategory already exists.")

        subcategory = self.model(**subcategory_data)

        try:
            db.session.add(subcategory)
            db.session.commit()
        except SQLAlchemyError:
            raise DatabaseError

        return subcategory

    def update_subcategory(self, subcategory_data, subcategory_id):
        subcategory = self.get_subcategory(subcategory_id)

        if "name" in subcategory_data:
            subcategory.name = subcategory_data["name"]

        if "description" in subcategory_data:
            subcategory.description = subcategory_data["description"]

        try:
            db.session.add(subcategory)
            db.session.commit()
        except SQLAlchemyError:
            raise DatabaseError

        return subcategory
