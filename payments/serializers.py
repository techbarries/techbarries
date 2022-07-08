from rest_framework import serializers
from payments.models import EventTransaction
from django.utils.translation import gettext_lazy as _


class EventTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTransaction
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user_id', 'event_id'),
                message=_("The event is already paid by the user.")
            )
        ]
        fields='__all__'
