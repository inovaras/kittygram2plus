from rest_framework.throttling import AnonRateThrottle
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from .models import Achievement, Cat, User

from .serializers import AchievementSerializer, CatSerializer, UserSerializer
from .pagination import CatsPagination


class CatViewSet(viewsets.ModelViewSet):

    serializer_class = CatSerializer
    throttle_scope = 'low_request'
    pagination_class = CatsPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = Cat.objects.all()
        # Добыть параметр color из GET-запроса
        color = self.request.query_params.get('color')
        if color is not None:
            #  через ORM отфильтровать объекты модели Cat
            #  по значению параметра color, полученного в запросе
            queryset = queryset.filter(color=color)
        return queryset


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
