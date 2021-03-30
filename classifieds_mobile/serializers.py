from rest_framework import serializers
from classifieds.models import *


# User model serializer
class Usererializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', ]


# Aircraft Make model serializer
class AircraftMakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AircraftMake
        fields = '__all__'


# Aircraft type model serializer
class AircraftTypeSerializer(serializers.ModelSerializer):
    type_make = AircraftMakeSerializer(many=False)

    class Meta:
        model = AircraftType
        fields = '__all__'


class ClassifiedsPicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassifiedImage
        fields = '__all__'


# Classifieds List/Detail serializer


class ClassifiedsListAPISerializers(serializers.ModelSerializer):
    aircraft_type = AircraftTypeSerializer(many=False)
    aircraft_make = AircraftMakeSerializer(many=False)
    user = Usererializer(many=False)
    classifieds_pics = serializers.SerializerMethodField()

    class Meta:
        model = Classified
        fields = '__all__'

    def get_classifieds_pics(self, data):
        images = ClassifiedImage.objects.filter(classified_id=data.pk)
        serialize_images = ClassifiedsPicsSerializer(images, many=True)
        return serialize_images.data


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
