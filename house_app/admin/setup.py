from fastapi import FastAPI
from sqladmin import Admin
from .views import HouseAdmin, UserProfileAdmin
from house_app.db.models import House, UserProfile
from house_app.db.database import engine


def setup_admin(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(HouseAdmin)
    admin.add_view(UserProfileAdmin)
