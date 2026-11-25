"""Corrigir avatar do Bitello"""
import sys
sys.path.insert(0, 'c:\\Users\\Usuario\\Desktop\\SOFASCORE DUS GURI')

from app import create_app, db
from app.models.player import Player

app = create_app()

with app.app_context():
    bitello = Player.query.filter_by(name='Bitello').first()
    
    if bitello and bitello.avatar:
        print(f"Avatar atual: {bitello.avatar}")
        
        if bitello.avatar.startswith('avatars/'):
            novo_avatar = bitello.avatar.replace('avatars/', 'uploads/avatars/')
            bitello.avatar = novo_avatar
            db.session.commit()
            print(f"✓ Avatar corrigido para: {bitello.avatar}")
        else:
            print(f"Avatar já está com caminho correto")
