from typing import Any

from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet

from app import permissions
from app.viewsets import AppViewSet
from works.api import serializers
from works.models import Work


class WorkViewSet(ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Work.objects.all()
    serializer_class = serializers.WorkCreateSerializer

    def retrieve(self, **kwargs: Any):
        raise PermissionDenied

    def list(self, **kwargs: Any):
        raise PermissionDenied

    def update(self, **kwargs: Any):
        raise PermissionDenied


class ReviewViewSet(AppViewSet):
    queryset = Work.objects.for_viewset()
    serializer_class = serializers.WorkListSerializer
    pagination_class = None

    serializer_action_classes = {
        'create': serializers.ReviewCreateSerializer,
        'update': serializers.ReviewCreateSerializer,
        'retrieve': serializers.WorkDetailSerializer,
    }


class ReviewOnModerationViewSet(AppViewSet):
    queryset = Work.objects.on_moderation()
    serializer_class = serializers.WorkListSerializer

    serializer_action_classes = {
        'create': serializers.ReviewCreateSerializer,
        'update': serializers.ReviewCreateSerializer,
        'retrieve': serializers.WorkDetailSerializer,
    }
