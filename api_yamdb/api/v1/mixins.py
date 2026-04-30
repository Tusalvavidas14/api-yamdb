from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework import viewsets, mixins


class PatchModelMixin:
    """Обеспечивает частичную модификацию объекта (`PATCH`)."""

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = True
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class UsernameValidationMixin:
    """Миксин, добавляющий валидацию поля username."""

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Использовать "me" запрещено.')
        return value


class CustomUserViewSet(
    PatchModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class NoPutMixin:
    """Миксин запрещающий PUT запросы."""

    def update(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Метод PUT не разрешен. Используйте PATCH.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
