from django.urls import include, path
from .views import CreateUserView, GetUserView, ListUsersView, DeleteUserView, UserProfileView, CustomAuthToken ,LoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', ListUsersView.as_view(), name='list_users'),
    path('<int:user_id>/', GetUserView.as_view(), name='get_user'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='user_profile'),
    path('delete/<int:user_id>/', DeleteUserView.as_view(), name='delete_user'),
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('login/', LoginView.as_view(), name='login'),
] 