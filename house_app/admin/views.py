from sqladmin import ModelView
from house_app.db.models import House, UserProfile


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.username]


class HouseAdmin(ModelView, model=House):
    column_list = [House.id, House.GrLivArea]

