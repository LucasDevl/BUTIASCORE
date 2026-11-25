import os
import tempfile
import unittest
from datetime import datetime

from app import create_app, db
from app.models.assist import Assist
from app.models.goal import Goal
from app.models.lineup_slot import LineupSlot
from app.models.match import Match
from app.models.match_lineup import MatchLineup
from app.models.player import Player
from app.models.player_match import PlayerMatch
from app.models.season import Season
from app.models.team import Team
from app.models.user import User


class LineupTests(unittest.TestCase):
    def setUp(self):
        self.previous_database_url = os.environ.get('DATABASE_URL')
        self.temp_dir = tempfile.TemporaryDirectory()
        database_path = os.path.join(self.temp_dir.name, 'lineup-test.db').replace('\\', '/')
        os.environ['DATABASE_URL'] = f'sqlite:///{database_path}'
        self.app = create_app()
        self.app.config['TESTING'] = True
        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()
        self.temp_dir.cleanup()
        if self.previous_database_url is None:
            os.environ.pop('DATABASE_URL', None)
        else:
            os.environ['DATABASE_URL'] = self.previous_database_url

    def create_match(self, players):
        with self.app.app_context():
            admin = User(username='organizer', role='admin')
            admin.set_password('test-password')
            season = Season(year=2025, name='2025')
            team_a = Team(name='Butiá A', color='#d5ad42')
            team_b = Team(name='Butiá B', color='#222222')
            db.session.add_all([admin, season, team_a, team_b, *players])
            db.session.flush()
            match = Match(
                season_id=season.id,
                team_a_id=team_a.id,
                team_b_id=team_b.id,
                date=datetime(2025, 5, 1),
                location='Campo',
            )
            db.session.add(match)
            db.session.commit()
            return match.id, team_a.id, team_b.id, [player.id for player in players]

    def login(self, client):
        response = client.post(
            '/auth/login',
            data={'username': 'organizer', 'password': 'test-password'},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_eight_player_formation_places_excess_in_reserves_and_renders(self):
        positions = ['Goleiro', 'Defesa', 'Meia', 'Atacante']
        players = [
            Player(name=f'Jogador {index:02}', position=positions[index % len(positions)])
            for index in range(17)
        ]
        match_id, team_a_id, team_b_id, player_ids = self.create_match(players)
        client = self.app.test_client()
        self.login(client)

        data = {
            'players_on_field': '8',
            'formation': '2-3-2',
            'lineup_mode': 'manual',
            'player_ids': [str(player_id) for player_id in player_ids],
        }
        for index, player_id in enumerate(player_ids):
            data[f'team_for_{player_id}'] = str(team_a_id if index < 9 else team_b_id)

        response = client.post(
            f'/matches/{match_id}/generate-lineup',
            data=data,
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Banco de reservas', response.data)
        self.assertIn(b'2-3-2', response.data)

        client.post(
            f'/matches/{match_id}/rate-player',
            data={'player_id': str(player_ids[0]), 'rating': '8.7'},
            follow_redirects=True,
        )
        response = client.post(
            f'/matches/{match_id}/generate-lineup',
            data=data,
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            self.assertEqual(MatchLineup.query.filter_by(
                match_id=match_id,
                players_on_field=8,
                formation='2-3-2',
            ).count(), 1)
            self.assertEqual(PlayerMatch.query.filter_by(match_id=match_id).count(), 17)
            self.assertEqual(LineupSlot.query.filter_by(match_id=match_id).count(), 16)
            self.assertEqual(LineupSlot.query.filter_by(
                match_id=match_id,
                team_id=team_a_id,
            ).count(), 8)
            self.assertEqual(LineupSlot.query.filter_by(
                match_id=match_id,
                team_id=team_b_id,
            ).count(), 8)
            self.assertEqual(PlayerMatch.query.filter_by(
                match_id=match_id,
                player_id=player_ids[0],
            ).one().rating, 8.7)
            starting_player_ids = {
                slot.player_id for slot in LineupSlot.query.filter_by(
                    match_id=match_id,
                    team_id=team_a_id,
                ).all()
            }
            reserve_player_id = next(
                player_id for player_id in player_ids
                if PlayerMatch.query.filter_by(
                    match_id=match_id,
                    team_id=team_a_id,
                    player_id=player_id,
                ).first() is not None
                and player_id not in starting_player_ids
            )
            reserve = PlayerMatch.query.filter_by(
                match_id=match_id,
                player_id=reserve_player_id,
            ).one()
            reserve.rating = 9.2
            goal = Goal(match_id=match_id, team_id=team_a_id, scorer_id=reserve_player_id)
            another_goal = Goal(match_id=match_id, team_id=team_a_id, scorer_id=player_ids[0])
            db.session.add_all([goal, another_goal])
            db.session.flush()
            db.session.add(Assist(
                goal_id=another_goal.id,
                match_id=match_id,
                assister_id=reserve_player_id,
            ))
            db.session.commit()

        response = client.get(f'/matches/{match_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'data-tab="teams"', response.data)
        self.assertIn(b'id="teams"', response.data)
        self.assertIn(b'class="complete-match-pitch"', response.data)
        self.assertNotIn(b'class="pitch-position-label"', response.data)
        bank_markup = response.data.split(b'<section class="lineup-bench">', 1)[1].split(b'</section>', 1)[0]
        self.assertIn(b'9.2', bank_markup)
        self.assertIn(b'alt="Gol"', bank_markup)
        self.assertIn(b'alt="Assist\xc3\xaancia"', bank_markup)
        self.assertIn(b'alt="MVP"', bank_markup)

    def test_slot_selection_swaps_players_and_can_move_one_to_the_bench(self):
        players = [
            Player(name='Goleiro Um', position='Goleiro'),
            Player(name='Defensor Um', position='Defesa'),
            Player(name='Outro Goleiro', position='Goleiro'),
        ]
        match_id, team_a_id, team_b_id, player_ids = self.create_match(players)
        client = self.app.test_client()
        self.login(client)

        response = client.post(
            f'/matches/{match_id}/generate-lineup',
            data={
                'players_on_field': '7',
                'formation': '2-2-2',
                'lineup_mode': 'manual',
                'player_ids': [str(player_id) for player_id in player_ids],
                f'team_for_{player_ids[0]}': str(team_a_id),
                f'team_for_{player_ids[1]}': str(team_a_id),
                f'team_for_{player_ids[2]}': str(team_b_id),
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

        response = client.post(
            f'/matches/{match_id}/lineup-slot',
            data={
                'team_id': str(team_a_id),
                'slot_key': 'gk',
                'player_id': str(player_ids[1]),
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            self.assertIsNotNone(LineupSlot.query.filter_by(
                match_id=match_id,
                team_id=team_a_id,
                slot_key='gk',
                player_id=player_ids[1],
            ).one_or_none())
            self.assertIsNotNone(LineupSlot.query.filter_by(
                match_id=match_id,
                team_id=team_a_id,
                slot_key='def-1',
                player_id=player_ids[0],
            ).one_or_none())

        response = client.post(
            f'/matches/{match_id}/lineup-slot',
            data={'team_id': str(team_a_id), 'slot_key': 'gk', 'player_id': ''},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            self.assertIsNone(LineupSlot.query.filter_by(
                match_id=match_id,
                team_id=team_a_id,
                slot_key='gk',
            ).first())
            self.assertIsNotNone(PlayerMatch.query.filter_by(
                match_id=match_id,
                team_id=team_a_id,
                player_id=player_ids[1],
            ).first())


if __name__ == '__main__':
    unittest.main()
