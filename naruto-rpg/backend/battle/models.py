from django.db import models

class Jutsu(models.Model):
    ELEMENT_CHOICES = [
        ('FIRE', 'Katon (Fogo)'),
        ('WATER', 'Suiton (Água)'),
        ('WIND', 'Fuuton (Vento)'),
        ('LIGHTNING', 'Raiton (Trovão)'),
        ('EARTH', 'Doton (Terra)'),
        ('NEUTRAL', 'Taijutsu/Geral'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    chakra_cost = models.IntegerField(default=20)
    base_damage = models.IntegerField(default=35)
    element = models.CharField(max_length=20, choices=ELEMENT_CHOICES, default='NEUTRAL')
    is_healing = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.get_element_display()})"


class Ninja(models.Model):
    VILLAGE_CHOICES = [
        ('KONOHA', 'Folha'),
        ('AKATSUKI', 'Akatsuki'),
        ('SUNAGAKURE', 'Areia'),
        ('OTOGAKURE', 'Som'),
    ]

    name = models.CharField(max_length=100)
    village = models.CharField(max_length=20, choices=VILLAGE_CHOICES, default='KONOHA')
    avatar_url = models.URLField(max_length=500)
    
    # Atributos Base
    max_hp = models.IntegerField(default=100)
    max_chakra = models.IntegerField(default=100)
    attack = models.IntegerField(default=20)
    defense = models.IntegerField(default=10)
    speed = models.IntegerField(default=15)
    
    # NOVOS CAMPOS: Sistema de Níveis e XP
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
    xp_to_next_level = models.IntegerField(default=100)
    
    # Relacionamento com os Jutsus do Ninja
    jutsus = models.ManyToManyField(Jutsu, related_name='ninjas')

    def __str__(self):
        return f"{self.name} (Lv. {self.level}) - {self.get_village_display()}"