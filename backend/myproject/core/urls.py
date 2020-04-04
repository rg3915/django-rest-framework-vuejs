from django.urls import include, path
from rest_framework import routers
from myproject.core import views as v


app_name = 'core'


router = routers.DefaultRouter()
router.register('user', v.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
