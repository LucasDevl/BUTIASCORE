"""Script para adicionar estatísticas da temporada 2025"""
import sys
sys.path.insert(0, 'c:\\Users\\Usuario\\Desktop\\SOFASCORE DUS GURI')

from app import create_app, db
from app.models.player import Player
from app.models.season import Season
from app.models.player_stats import PlayerStats

app = create_app()

# Dados de jogos
jogos_data = {
    'THOMAS': 11, 'LUCÃO': 11, 'NIKÃO': 11, 'VITOR H': 10, 'KAUÊ': 10, 'VITOR N': 10,
    'BITELLO': 9, 'RAFA': 8, 'ANDRÉ': 8, 'ROGÉRIO': 7, 'ISRAEL': 7, 'JOKAS': 7,
    'PEIXE': 7, 'J.A': 7, 'ARTHUR': 5, 'G. HARTMANN': 5, 'BACELAR': 4, 'RAVI': 4,
    'ALEXANDRE': 2, 'G. MENDONÇA': 2, 'RODRIGO': 2, 'IRMÃO GH': 2, 'SIDNEI': 1,
    'THOMAZ': 1, 'PAULO': 1, 'GOLEIRO GH': 1, 'CLAUDIO': 1, 'DENILSON': 1,
    'MARCOS': 1, 'SONTAG': 1, 'ALEX': 1
}

# Dados de gols
gols_data = {
    'KAUÊ': 11, 'ISRAEL': 11, 'RAFA': 11, 'THOMAS': 9, 'NIKÃO': 7, 'LUCÃO': 6,
    'PEIXE': 4, 'ANDRÉ': 4, 'J.A': 3, 'ARTHUR': 3, 'BITELLO': 3, 'BACELAR': 2,
    'G. HARTMANN': 1, 'G. MENDONÇA': 1, 'RAVI': 1, 'DENILSON': 1, 'JOKAS': 1, 'GOETZ': 1
}

with app.app_context():
    # Buscar temporada 2025
    season_2025 = Season.query.filter_by(year=2025).first()
    if not season_2025:
        print("❌ Temporada 2025 não encontrada!")
        sys.exit(1)
    
    print(f"✅ Temporada 2025 encontrada (ID: {season_2025.id})")
    
    # Todos os nomes únicos dos jogadores
    todos_nomes = set(list(jogos_data.keys()) + list(gols_data.keys()))
    
    print(f"\n📋 Total de {len(todos_nomes)} jogadores para processar")
    
    criados = 0
    atualizados = 0
    
    for nome in sorted(todos_nomes):
        # Buscar ou criar jogador
        player = Player.query.filter_by(name=nome).first()
        
        if not player:
            player = Player(
                name=nome,
                position='Atacante'  # Padrão, pode ser ajustado depois
            )
            db.session.add(player)
            db.session.flush()  # Para pegar o ID
            criados += 1
            print(f"➕ Criado: {nome}")
        else:
            print(f"✅ Encontrado: {nome}")
        
        # Buscar ou criar estatísticas
        stats = PlayerStats.query.filter_by(player_id=player.id, season_id=season_2025.id).first()
        
        matches_played = jogos_data.get(nome, 0)
        goals = gols_data.get(nome, 0)
        
        if not stats:
            stats = PlayerStats(
                player_id=player.id,
                season_id=season_2025.id,
                matches_played=matches_played,
                goals=goals,
                assists=0
            )
            db.session.add(stats)
            print(f"   📊 Estatísticas adicionadas: {matches_played} jogos, {goals} gols")
        else:
            stats.matches_played = matches_played
            stats.goals = goals
            atualizados += 1
            print(f"   📊 Estatísticas atualizadas: {matches_played} jogos, {goals} gols")
    
    # Commit final
    db.session.commit()
    
    print(f"\n✨ Processo concluído!")
    print(f"   ➕ Jogadores criados: {criados}")
    print(f"   🔄 Jogadores atualizados: {atualizados}")
    print(f"   📊 Total processado: {len(todos_nomes)}")
