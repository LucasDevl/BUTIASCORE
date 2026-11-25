"""Teste simples de upload"""
import sys
sys.path.insert(0, 'c:\\Users\\Usuario\\Desktop\\SOFASCORE DUS GURI')

from app import create_app, db
from app.models.player import Player

app = create_app()

with app.app_context():
    # Pegar Bitello
    bitello = Player.query.filter_by(name='Bitello').first()
    
    if bitello:
        print(f"Bitello encontrado!")
        print(f"  ID: {bitello.id}")
        print(f"  Avatar: {bitello.avatar}")
        print(f"  Name: {bitello.name}")
        
        # Tentar atualizar manualmente
        bitello.avatar = 'avatars/test.jpg'
        db.session.commit()
        print(f"\nApós atualização manual:")
        print(f"  Avatar: {bitello.avatar}")
        
        # Recuperar do banco
        bitello_reloaded = Player.query.filter_by(name='Bitello').first()
        print(f"\nApós reload:")
        print(f"  Avatar: {bitello_reloaded.avatar}")
    else:
        print("Bitello não encontrado")
