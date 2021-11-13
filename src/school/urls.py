from django.urls import path, include

from rest_framework import routers

from school.views import SchoolViewSet

app_name = 'school'

router = routers.SimpleRouter()
router.register(prefix=r'schools', viewset=SchoolViewSet)

urlpatterns = router.urls
