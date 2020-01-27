from rest_framework import serializers
from vocabulary_trainer.models import VokabelList, Vokabel


# Vokabel, Vokabellisten, ListAccess
class VokabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vokabel
        fields = ['name1', 'name2', 'done']

    def update(self, instance, validated_data):
        instance.name1 = validated_data.get('name1', instance.name1)
        instance.name2 = validated_data.get('name2', instance.name2)
        instance.done = validated_data.get('done', instance.done)

        instance.save()
        return instance


class VokabelListSerializer(serializers.ModelSerializer):
    vokabellists = VokabelSerializer(many=True)

    class Meta:
        model = VokabelList
        fields = ['name', 'description']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)

        instance.save()
        return instance
