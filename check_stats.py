"""Script para verificar as estatísticas salvas no banco"""
import sys
sys.path.insert(0, 'c:\\Users\\Usuario\\Desktop\\SOFASCORE DUS GURI')

from app import create_app, db
from app.models.player import Player
from app.models.season import Season
from app.models.player_stats import PlayerStats

app = create_app()

with app.app_context():
    season_2025 = Season.query.filter_by(year=2025).first()
    
    if not season_2025:
        print("❌ Temporada 2025 não encontrada!")
        sys.exit(1)
    
    print(f"🔍 Verificando estatísticas da Temporada 2025 (ID: {season_2025.id})\n")
    
    # Buscar todas as estatísticas da temporada 2025
    stats = PlayerStats.query.filter_by(season_id=season_2025.id).all()
    
    print(f"📊 Total de registros de estatísticas: {len(stats)}\n")
    
    # Mostrar os dados
    for stat in sorted(stats, key=lambda x: x.goals, reverse=True)[:15]:
        player = stat.player
        print(f"{player.name:20} | Jogos: {stat.matches_played:2} | Gols: {stat.goals:2} | Assistências: {stat.assists}")
    
    print(f"\n... ({len(stats) - 15} outros jogadores)")
