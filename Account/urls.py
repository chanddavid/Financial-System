
from django.urls import path,include
from .views import RegisterView, LoginView, UserProfileView
from rest_framework.routers import DefaultRouter


app_name="account"

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),#for register
    path('login/', LoginView.as_view(), name='login'),#from remote repo
    path('profile/', UserProfileView.as_view(), name='profile'),#new changes
]
#nothing new




# router = DefaultRouter()
# router.register('register/', RegisterViewSet, basename='income')
# router.register('login/', LoginViewSet, basename='expense')
# router.register('profile/', UserProfileViewSet, basename='loan')

# urlpatterns = [
#     path('', include(router.urls)),
# ]
