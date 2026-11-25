"""
Arquivo de inicialização para garantir que os diretórios de upload existem
"""

import os

def ensure_upload_directories():
    """Cria os diretórios de upload se não existirem"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    upload_dir = os.path.join(base_dir, 'app', 'static', 'uploads')
    avatars_dir = os.path.join(upload_dir, 'avatars')
    videos_dir = os.path.join(upload_dir, 'videos')
    instance_dir = os.path.join(base_dir, 'instance')
    
    for directory in [upload_dir, avatars_dir, videos_dir, instance_dir]:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Diretório confirmado: {directory}")

if __name__ == '__main__':
    ensure_upload_directories()
    print("\n✅ Todos os diretórios estão prontos!")
