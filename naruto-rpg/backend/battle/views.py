from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Ninja, Jutsu
from .serializers import NinjaSerializer, JutsuSerializer
import random

class NinjaViewSet(viewsets.ModelViewSet):
    queryset = Ninja.objects.all()
    serializer_class = NinjaSerializer


class JutsuViewSet(viewsets.ModelViewSet):
    queryset = Jutsu.objects.all()
    serializer_class = JutsuSerializer


class BattleTurnView(APIView):
    """
    Processa a lógica do turno de batalha entre o Player e o Inimigo (IA).
    Calcula dano, aplica o contra-ataque da IA e verifica condições de vitória.
    """
    def post(self, request):
        data = request.data
        action = data.get('action') # 'ATTACK' ou 'JUTSU'
        jutsu_id = data.get('jutsu_id')
        
        player = data.get('player')
        enemy = data.get('enemy')
        
        logs = []
        winner = None

        # 1. TURNO DO PLAYER
        if action == 'ATTACK':
            # Dano básico de Taijutsu baseado no ataque do ninja
            base_dmg = player.get('attack', 20)
            damage = random.randint(base_dmg - 5, base_dmg + 5)
            enemy['current_hp'] = max(0, enemy['current_hp'] - damage)
            logs.append(f"{player['name']} atacou com Taijutsu causando {damage} de dano!")
            
        elif action == 'JUTSU' and jutsu_id:
            try:
                jutsu = Jutsu.objects.get(id=jutsu_id)
                if player['current_chakra'] >= jutsu.chakra_cost:
                    player['current_chakra'] -= jutsu.chakra_cost
                    damage = jutsu.base_damage + random.randint(-3, 5)
                    enemy['current_hp'] = max(0, enemy['current_hp'] - damage)
                    logs.append(f"{player['name']} lançou {jutsu.name} causando {damage} de dano!")
                else:
                    damage = 10
                    enemy['current_hp'] = max(0, enemy['current_hp'] - damage)
                    logs.append(f"Sem chakra suficiente! {player['name']} usou um ataque fraco causando {damage} de dano.")
            except Jutsu.DoesNotExist:
                damage = 15
                enemy['current_hp'] = max(0, enemy['current_hp'] - damage)
                logs.append(f"{player['name']} desferiu um golpe básico causando {damage} de dano.")

        # Verifica se o Inimigo foi derrotado
        if enemy['current_hp'] <= 0:
            enemy['current_hp'] = 0
            winner = 'player'
            logs.append(f"{enemy['name']} foi derrotado! Vitória!")
            return Response({
                'player': player,
                'enemy': enemy,
                'log': logs,
                'winner': winner
            })

        # 2. CONTRA-ATAQUE DA IA (INIMIGO)
        # IA um pouco mais agressiva e desafiadora
        ai_attack_dmg = random.randint(18, 30)
        player['current_hp'] = max(0, player['current_hp'] - ai_attack_dmg)
        logs.append(f"{enemy['name']} contra-atacou causando {ai_attack_dmg} de dano!")

        # Verifica se o Player foi derrotado
        if player['current_hp'] <= 0:
            player['current_hp'] = 0
            winner = 'enemy'
            logs.append(f"{player['name']} foi derrotado... Derrota!")

        return Response({
            'player': player,
            'enemy': enemy,
            'log': logs,
            'winner': winner
        })