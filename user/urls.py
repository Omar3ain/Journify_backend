from django.urls import include, path   
from .views import ProtectedView, CreateUserView, GetUserView, ListUsersView, DeleteUserView, UserProfileView, CustomAuthToken ,LoginView, UpdateUserView, UserChangePassword
from flight.views import ListFlight_ReservationsView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', ListUsersView.as_view(), name='list_users'),
    path('<int:user_id>/', GetUserView.as_view(), name='get_user'),
    path('delete/<int:user_id>/', DeleteUserView.as_view(), name='delete_user'),
    path('update/<int:user_id>/', UpdateUserView.as_view(), name='update_user'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='user_profile'),
    path('<int:user_id>/change-password/', UserChangePassword.as_view(), name='user_change_password'),
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('login/', LoginView.as_view(), name='login'),
    path('auth/',include('drf_social_oauth2.urls',namespace='drf')), # add this
    path('protected/', ProtectedView.as_view(), name='protected_view'),
    # path('accounts/', include('allauth.urls')),
    path('reservations/', ListFlight_ReservationsView.as_view(), name='list_flightReservations'),

]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)