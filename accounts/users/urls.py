# accounts/urls.py
from django.urls import path

from .views import EditProfileView, SignUpView, ViewProfileView
from .views import SuperadminUserListView, SuperadminHomeView ,AdminHomeView, UserEditView, DeleteUserView, ViewUserDetailsView, AddUserView
from .views import custom_login

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    #path('superadmin-home/', SuperadminHomeView.as_view(), name='superadmin-home'),
    path('user-list/', SuperadminUserListView.as_view(), name='superadmin-user-list'),
    path('superadmin-home/', SuperadminHomeView.as_view(), name='superadmin-home'),
    path('user/edit/<int:pk>/', UserEditView.as_view(), name='superuser-edit'),
    path('user/delete/<int:user_id>/', DeleteUserView.as_view(), name='superuser-delete'),
    path('user/view-detail/<int:user_id>/', ViewUserDetailsView.as_view(), name='superuser-viewdetail'),
    path('user/add-user/', AddUserView.as_view(), name='superuser-adduser'),
    
    # profile urls
    path('profile/', ViewProfileView.as_view(), name='view-profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit-profile'),
    # 
    #path('assign-role/<int:user_id>/', AssignRoleView.as_view(), name='assign-role'),

    path('admin-home/', AdminHomeView.as_view(), name='admin-home'),
    # path('admin-user-list/', AdminUserListView.as_view(), name='admin-user-list'),
    
]