"""Script para verificar se as fotos estão sendo salvas corretamente"""
import sys
import os
sys.path.insert(0, 'c:\\Users\\Usuario\\Desktop\\SOFASCORE DUS GURI')

from app import create_app, db
from app.models.player import Player

app = create_app()

with app.app_context():
    players = Player.query.all()
    
    print("🔍 Verificando avatares dos jogadores:\n")
    
    for player in players:
        if player.avatar:
            print(f"✓ {player.name}: {player.avatar}")
            
            # Verificar se o arquivo existe
            upload_folder = app.config.get('UPLOAD_FOLDER', 'app/static/uploads')
            full_path = os.path.join(upload_folder, player.avatar)
            
            if os.path.exists(full_path):
                size = os.path.getsize(full_path)
                print(f"  📁 Arquivo encontrado: {full_path} ({size} bytes)")
            else:
                print(f"  ❌ Arquivo NÃO encontrado: {full_path}")
        else:
            print(f"✗ {player.name}: Sem avatar")
    
    print(f"\nTotal de jogadores: {len(players)}")
    print(f"Com avatar: {sum(1 for p in players if p.avatar)}")
    print(f"Sem avatar: {sum(1 for p in players if not p.avatar)}")
