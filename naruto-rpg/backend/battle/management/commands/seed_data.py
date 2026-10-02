from django.core.management.base import BaseCommand
from battle.models import Ninja, Jutsu

class Command(BaseCommand):
    help = 'Popula o banco de dados com os ninjas e jutsus iniciais'

    def handle(self, *args, **options):
        self.stdout.write("Atualizando banco de dados com caminhos locais...")

        # Limpa dados antigos para evitar duplicatas ou conflitos
        Jutsu.objects.all().delete()
        Ninja.objects.all().delete()

        # Jutsus Básicos / Existentes
        rasengan = Jutsu.objects.create(name='Rasengan', description='Esfera de chakra.', chakra_cost=25, base_damage=40)
        chidori = Jutsu.objects.create(name='Chidori', description='Ataque elétrico.', chakra_cost=25, base_damage=42)
        katon = Jutsu.objects.create(name='Katon: Goukakyuu', description='Bola de fogo.', chakra_cost=20, base_damage=35)
        amaterasu = Jutsu.objects.create(name='Amaterasu', description='Chamas negras.', chakra_cost=40, base_damage=60)
        shinra_tensei = Jutsu.objects.create(name='Shinra Tensei', description='Repulsão gravitacional.', chakra_cost=45, base_damage=65)

        # Novos jutsus específicos da Sakura
        soco_monstruoso = Jutsu.objects.create(name='Oka Shō', description='Soco devastador com controle de chakra.', chakra_cost=20, base_damage=38)
        palma_mistica = Jutsu.objects.create(name='Shōsen Jutsu', description='Técnica de Palma Mística para cura.', chakra_cost=25, base_damage=0)

        # Criar Ninjas
        naruto = Ninja.objects.create(
            name='Naruto Uzumaki',
            village='Folha',
            avatar_url='/avatars/naruto.png',
            max_hp=100, max_chakra=100, attack=25, defense=10, speed=20
        )
        naruto.jutsus.add(rasengan)

        sasuke = Ninja.objects.create(
            name='Sasuke Uchiha',
            village='Folha',
            avatar_url='/avatars/sasuke.png',
            max_hp=90, max_chakra=110, attack=30, defense=12, speed=25
        )
        sasuke.jutsus.add(chidori, katon)

        kakashi = Ninja.objects.create(
            name='Kakashi Hatake',
            village='Folha',
            avatar_url='/avatars/kakashi.png',
            max_hp=100, max_chakra=130, attack=27, defense=14, speed=24
        )
        kakashi.jutsus.add(chidori)

        # Sakura configurada com os jutsus corretos e sem vestígios do Itachi
        sakura = Ninja.objects.create(
            name='Sakura Haruno',
            village='Folha',
            avatar_url='/avatars/sakura.png',
            max_hp=95, max_chakra=120, attack=28, defense=11, speed=22
        )
        sakura.jutsus.add(soco_monstruoso, palma_mistica)

        pain = Ninja.objects.create(
            name='Pain (Tendo)',
            village='Akatsuki',
            avatar_url='/avatars/pain.png',
            max_hp=120, max_chakra=150, attack=32, defense=15, speed=18
        )
        pain.jutsus.add(shinra_tensei)

        self.stdout.write(self.style.SUCCESS("Banco de dados populado com sucesso com a Sakura!"))