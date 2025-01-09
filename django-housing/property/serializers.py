from rest_framework import serializers

from .models import Property, PropertyImage, Reservation

from useraccount.serializers import UserDetailSerializer


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ('image_url',)

class PropertiesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = (
            'id',
            'title',
            'price_per_night',
            'image_url',
            'favorited',
        )

    def get_favorited(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and obj.favorited.filter(id=user.id).exists()


class PropertiesDetailSerializer(serializers.ModelSerializer):
    additionnal_images = PropertyImageSerializer(many=True, read_only=True)
    landlord = UserDetailSerializer(read_only=True, many=False)
    class Meta:
        model = Property
        fields = (
            'id',
            'title',
            'description',
            'price_per_night',
            'image_url',
            'bedrooms',
            'bathrooms',
            'guests',
            'landlord',
            'additionnal_images',
        )


class ReservationListSerializer(serializers.ModelSerializer):
    property = PropertiesListSerializer(read_only=True, many=False)
    class Meta:
        model = Reservation
        fields = (
            'id',
            'start_date',
            'end_date',
            'number_of_nights',
            'total_price',
            'property'
        )