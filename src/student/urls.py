from django.urls import path, include
from rest_framework import routers

from student.views import StudentViewSet

app_name = 'student'

router = routers.SimpleRouter()
router.register(prefix=r'students', viewset=StudentViewSet)

urlpatterns = router.urls
