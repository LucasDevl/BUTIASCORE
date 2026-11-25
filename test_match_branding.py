import os
import tempfile
import unittest
from io import BytesIO

from app import create_app, db
from app.models.goal import Goal
from app.models.match import Match
from app.models.player import Player
from app.models.player_match import PlayerMatch
from app.models.season import Season
from app.models.team import Team
from app.models.user import User


class MatchBrandingTests(unittest.TestCase):
    def setUp(self):
        self.previous_database_url = os.environ.get('DATABASE_URL')
        self.temp_dir = tempfile.TemporaryDirectory()
        database_path = os.path.join(self.temp_dir.name, 'branding-test.db').replace('\\', '/')
        os.environ['DATABASE_URL'] = f'sqlite:///{database_path}'
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['UPLOAD_FOLDER'] = os.path.join(self.temp_dir.name, 'uploads')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            admin = User(username='organizer', role='admin')
            admin.set_password('test-password')
            db.session.add_all([admin, Season(year=2026, name='2026')])
            db.session.commit()

        self.client = self.app.test_client()
        response = self.client.post(
            '/auth/login',
            data={'username': 'organizer', 'password': 'test-password'},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

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

    def create_match(self, logo_upload=None):
        data = {
            'date': '2026-06-15T10:00',
            'location': 'Campo do Butiá',
            'season_id': '1',
            'team_a_name': 'Butiá FC Preto',
            'team_b_name': 'Butiá FC Branco',
            'team_a_color': '#17191b',
            'team_b_color': '#f4f4f4',
            'team_a_logo_preset': 'butia_preto',
            'team_b_logo_preset': 'butia_branco',
        }
        if logo_upload:
            data['team_a_logo'] = logo_upload
        response = self.client.post('/matches/create', data=data, follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        return int(response.headers['Location'].rsplit('/', 1)[1])

    def test_sponsor_logos_appear_on_dashboard(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        for sponsor in ('betano', 'binance', 'eudajo'):
            self.assertIn(f'patrocinador-{sponsor}.png'.encode(), response.data)

    def test_preset_logos_and_goal_scorers_appear_in_score_header(self):
        match_id = self.create_match()
        with self.app.app_context():
            match = db.session.get(Match, match_id)
            team_a_id = match.team_a_id
            team_b_id = match.team_b_id
            player = Player(name='Jogador Marcador', position='Atacante')
            db.session.add(player)
            db.session.flush()
            db.session.add(PlayerMatch(
                player_id=player.id,
                match_id=match_id,
                team_id=team_a_id,
            ))
            db.session.add(Goal(
                match_id=match_id,
                team_id=team_a_id,
                scorer_id=player.id,
                minute=17,
            ))
            db.session.add(Goal(
                match_id=match_id,
                team_id=team_a_id,
                scorer_id=player.id,
                minute=30,
            ))
            opposing_scorer = Player(name='Outro Marcador', position='Atacante')
            db.session.add(opposing_scorer)
            db.session.flush()
            db.session.add(Goal(
                match_id=match_id,
                team_id=team_b_id,
                scorer_id=opposing_scorer.id,
                minute=42,
            ))
            match.status = 'finalizada'
            match.update_score()
            db.session.commit()
            player_id = player.id

        response = self.client.get(f'/matches/{match_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'images/butia-preto.png', response.data)
        self.assertIn(b'images/butia-branco.png', response.data)
        self.assertIn(
            b"Jogador Marcador <small>17&#39;, 30'</small>",
            response.data,
        )
        self.assertEqual(
            response.data.count(b'class="match-scorer">Jogador Marcador'),
            1,
        )
        self.assertIn(b'aria-label="Placar 2 a 1"', response.data)
        self.assertIn(b'Finalizado', response.data)
        header_start = response.data.index(b'<div class="match-header-large">')
        header_end = response.data.index(
            b'<div class="match-sponsor-row"',
            header_start,
        )
        self.assertNotIn('⚽'.encode(), response.data[header_start:header_end])

        with self.app.app_context():
            self.assertEqual(PlayerMatch.query.filter_by(player_id=player_id).count(), 1)
            self.assertEqual(Goal.query.filter_by(match_id=match_id).count(), 3)
            self.assertEqual(db.session.get(Match, match_id).score_a, 2)

    def test_uploaded_team_logo_is_saved_and_used_in_match_view(self):
        match_id = self.create_match(
            (BytesIO(b'fake-png-data'), 'custom-crest.png', 'image/png')
        )
        with self.app.app_context():
            match = db.session.get(Match, match_id)
            self.assertTrue(match.team_a.logo.startswith('uploads/logos/'))
            self.assertEqual(match.team_b.logo, 'images/butia-branco.png')
            uploaded_logo_path = os.path.join(
                self.app.config['UPLOAD_FOLDER'],
                *match.team_a.logo[len('uploads/'):].split('/'),
            )
            self.assertTrue(os.path.isfile(uploaded_logo_path))

        response = self.client.get(f'/matches/{match_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'/static/uploads/logos/', response.data)

        response = self.client.post(f'/matches/{match_id}/delete')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(os.path.exists(uploaded_logo_path))
        with self.app.app_context():
            self.assertEqual(Match.query.count(), 0)
            self.assertEqual(Team.query.count(), 0)


if __name__ == '__main__':
    unittest.main()
