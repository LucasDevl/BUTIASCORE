"""
Arquivo de exemplo para popular o banco com dados de teste.
Execute este arquivo com: python populate_db.py
"""

from app import create_app
from app.models.player import Player
from app.models.season import Season
from app.models.match import Match
from app.models.team import Team
from app.models.player_match import PlayerMatch
from app.models.goal import Goal
from app.models.assist import Assist
from app import db
from datetime import datetime, timedelta

def populate_database():
    """Popula o banco de dados com dados de teste"""
    
    app = create_app()
    
    with app.app_context():
        # Limpar dados existentes (opcional)
        # db.drop_all()
        # db.create_all()
        
        print("Adicionando dados de teste...")
        
        # Criar temporada
        season = Season(
            year=2026,
            name="Temporada 2026",
            description="Primeira temporada do SofaScore da Galera",
            is_active=True
        )
        db.session.add(season)
        db.session.flush()
        
        # Criar jogadores
        players_data = [
            {"name": "João Silva", "position": "Atacante", "shirt_number": 10},
            {"name": "Marco Santos", "position": "Meia", "shirt_number": 8},
            {"name": "Pedro Oliveira", "position": "Defesa", "shirt_number": 4},
            {"name": "Carlos Alves", "position": "Goleiro", "shirt_number": 1},
            {"name": "Felipe Costa", "position": "Atacante", "shirt_number": 9},
            {"name": "Gustavo Rocha", "position": "Meia", "shirt_number": 6},
            {"name": "Leonardo Barbosa", "position": "Defesa", "shirt_number": 3},
            {"name": "Rafael Nunes", "position": "Goleiro", "shirt_number": 1},
        ]
        
        players = []
        for data in players_data:
            player = Player(**data)
            db.session.add(player)
            players.append(player)
        db.session.flush()
        
        # Criar times
        team_a = Team(name="Time A", color="#FF0000")  # Vermelho
        team_b = Team(name="Time B", color="#0000FF")  # Azul
        db.session.add(team_a)
        db.session.add(team_b)
        db.session.flush()
        
        # Criar partida
        match_date = datetime.now() - timedelta(days=7)
        match = Match(
            date=match_date,
            location="Campo Municipal",
            season_id=season.id,
            team_a_id=team_a.id,
            team_b_id=team_b.id,
            status="finalizada"
        )
        db.session.add(match)
        db.session.flush()
        
        # Escalar jogadores
        for i, player in enumerate(players[:4]):
            pm = PlayerMatch(
                player_id=player.id,
                match_id=match.id,
                team_id=team_a.id,
                rating=7.5 + (i * 0.3)
            )
            db.session.add(pm)
        
        for i, player in enumerate(players[4:8]):
            pm = PlayerMatch(
                player_id=player.id,
                match_id=match.id,
                team_id=team_b.id,
                rating=6.5 + (i * 0.2)
            )
            db.session.add(pm)
        
        db.session.flush()
        
        # Registrar gols
        goal1 = Goal(
            match_id=match.id,
            team_id=team_a.id,
            scorer_id=players[0].id,  # João Silva
            minute=15
        )
        db.session.add(goal1)
        db.session.flush()
        
        # Registrar assistência
        assist1 = Assist(
            goal_id=goal1.id,
            match_id=match.id,
            assister_id=players[1].id  # Marco Santos
        )
        db.session.add(assist1)
        
        goal2 = Goal(
            match_id=match.id,
            team_id=team_a.id,
            scorer_id=players[0].id,
            minute=32
        )
        db.session.add(goal2)
        db.session.flush()
        
        goal3 = Goal(
            match_id=match.id,
            team_id=team_b.id,
            scorer_id=players[4].id,  # Felipe Costa
            minute=45
        )
        db.session.add(goal3)
        
        # Atualizar placar
        match.update_score()
        
        db.session.commit()
        
        print("✅ Dados de teste adicionados com sucesso!")
        print(f"✅ Temporada: {season.name}")
        print(f"✅ Jogadores: {len(players)}")
        print(f"✅ Partida: {team_a.name} {match.score_a} x {match.score_b} {team_b.name}")

if __name__ == '__main__':
    populate_database()
    print("\n💡 Dica: Acesse http://localhost:5000 para ver os dados!")
