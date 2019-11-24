

from rest_framework import routers

from api.v1.views import InterviewViewSet

router = routers.DefaultRouter()

router.register(r'interview', InterviewViewSet)