"""Script para unificar nomes duplicados de jogadores"""
import sys
sys.path.insert(0, 'c:\\Users\\Usuario\\Desktop\\SOFASCORE DUS GURI')

from app import create_app, db
from app.models.player import Player
from app.models.player_stats import PlayerStats

app = create_app()

# Mapeamento de nomes duplicados (nome incorreto -> nome correto)
duplicatas = {
    'J.a': 'J.A',
    'G. hartmann': 'G. Hartmann',
    'G. mendonça': 'G. Mendonça',
    'Goleiro gh': 'Goleiro Gh',
    'Irmão gh': 'Irmão Gh',
    'Vitor h': 'Vitor H',
    'Vitor n': 'Vitor N',
}

with app.app_context():
    print("🔍 Procurando e unificando nomes duplicados...\n")
    
    unificados = 0
    
    for nome_errado, nome_certo in duplicatas.items():
        player_errado = Player.query.filter_by(name=nome_errado).first()
        player_certo = Player.query.filter_by(name=nome_certo).first()
        
        if player_errado:
            print(f"Encontrado: {nome_errado}")
            
            if player_certo:
                print(f"  → Mesclando com {nome_certo}")
                
                # Mover todas as estatísticas do jogador errado para o certo
                stats_errado = PlayerStats.query.filter_by(player_id=player_errado.id).all()
                for stat in stats_errado:
                    # Verificar se já existe estatística para essa temporada
                    stat_certo = PlayerStats.query.filter_by(
                        player_id=player_certo.id,
                        season_id=stat.season_id
                    ).first()
                    
                    if stat_certo:
                        # Somar as estatísticas
                        stat_certo.goals += stat.goals
                        stat_certo.assists += stat.assists
                        stat_certo.matches_played += stat.matches_played
                        print(f"  ✓ Estatísticas somadas da temporada {stat.season_id}")
                        db.session.delete(stat)
                    else:
                        # Transferir a estatística
                        stat.player_id = player_certo.id
                        print(f"  ✓ Estatísticas transferidas da temporada {stat.season_id}")
                
                # Deletar o jogador duplicado
                db.session.delete(player_errado)
                unificados += 1
            else:
                # Se o nome correto não existe, apenas renomear
                player_errado.name = nome_certo
                print(f"  → Renomeado para {nome_certo}")
                unificados += 1
    
    db.session.commit()
    print(f"\n✨ {unificados} jogadores unificados com sucesso!")
