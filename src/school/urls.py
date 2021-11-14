from django.urls import path, include

from rest_framework_nested import routers

from school.views import SchoolViewSet
from student.views import StudentNestedViewSet

app_name = 'school'

router = routers.SimpleRouter()
router.register(prefix=r'schools', viewset=SchoolViewSet)

student_router = routers.NestedSimpleRouter(parent_router=router, parent_prefix='schools', lookup='school')
student_router.register(prefix=r'students', viewset=StudentNestedViewSet, basename='school-student-nested-url')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(student_router.urls)),
]
