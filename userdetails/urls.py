from django.urls import path, include
from rest_framework.routers import DefaultRouter

from userdetails.views import DevUserCreateView, UserDetailsViewSet, UserLoginView, UserReferralView

routers = DefaultRouter()
routers.register("", UserDetailsViewSet, basename="userdetails")

urlpatterns = [
    path("", include(routers.urls)),
    path("referral/<str:referral_code>/", UserReferralView.as_view()),
    path("user/login/", UserLoginView.as_view()),
    
    # developer User Api
    path("dev/usercreate/", DevUserCreateView.as_view())
]
