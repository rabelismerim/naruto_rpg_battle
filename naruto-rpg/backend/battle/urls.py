from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NinjaViewSet, JutsuViewSet, BattleTurnView

router = DefaultRouter()
router.register(r'ninjas', NinjaViewSet, basename='ninja')
router.register(r'jutsus', JutsuViewSet, basename='jutsu')

urlpatterns = [
    path('', include(router.urls)),
    path('battle/turn/', BattleTurnView.as_view(), name='battle-turn'),
]