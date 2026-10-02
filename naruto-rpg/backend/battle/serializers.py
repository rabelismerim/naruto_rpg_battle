from rest_framework import serializers
from .models import Ninja, Jutsu

class JutsuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jutsu
        fields = '__all__'

class NinjaSerializer(serializers.ModelSerializer):
    # Traz os detalhes completos dos Jutsus associados ao ninja
    jutsus = JutsuSerializer(many=True, read_only=True)

    class Meta:
        model = Ninja
        fields = [
            'id', 
            'name', 
            'village', 
            'avatar_url', 
            'max_hp', 
            'max_chakra', 
            'attack', 
            'defense', 
            'speed', 
            'level', 
            'xp', 
            'xp_to_next_level', 
            'jutsus'
        ]