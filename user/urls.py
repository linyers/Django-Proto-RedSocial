from django.urls import path

from .views import DetailProfile, EditProfile, AddFollower, RemoveFollower, ListFollowers

app_name = 'user'

urlpatterns = [
    path('<username>/', DetailProfile, name='profile'),
    path('profile/edit/', EditProfile, name='edit'),
    path('profile/<int:pk>/follow', AddFollower.as_view(), name='follow'),
    path('profile/<int:pk>/unfollow', RemoveFollower.as_view(), name='unfollow'),
    path('profile/<int:pk>/followers/', ListFollowers.as_view(), name='followers'),
]
