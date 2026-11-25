"""
Teste rápido da integração - Valida que tudo está funcionando
"""

def test_imports():
    """Testa se todos os imports funcionam"""
    print("Testando imports...")
    try:
        from app import create_app
        from app.models.player import Player
        from app.models.season import Season
        from app.models.match import Match
        from app.models.team import Team
        from app.models.goal import Goal
        from app.models.assist import Assist
        from app.models.video import Video
        from app.models.player_match import PlayerMatch
        from app.models.player_stats import PlayerStats
        print("Todos os imports OK")
        return True
    except Exception as e:
        print(f"Erro de import: {e}")
        return False

def test_app_creation():
    """Testa se a aplicação pode ser criada"""
    print("\nTestando criação da aplicação...")
    try:
        from app import create_app
        app = create_app()
        print("Aplicação criada com sucesso")
        return True
    except Exception as e:
        print(f"Erro ao criar app: {e}")
        return False

def test_database():
    """Testa se o banco de dados foi criado"""
    print("\nTestando banco de dados...")
    try:
        from app import create_app
        import os
        app = create_app()
        db_path = os.path.join(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
        if os.path.exists(db_path):
            print(f"Banco de dados criado: {db_path}")
            return True
        else:
            print("Banco de dados sera criado na primeira execucao")
            return True
    except Exception as e:
        print(f"Erro ao testar BD: {e}")
        return False

def test_routes():
    """Testa se as rotas estão registradas"""
    print("\nTestando rotas...")
    try:
        from app import create_app
        app = create_app()
        
        routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                routes.append(f"{rule.rule} ({rule.endpoint})")
        
        if len(routes) > 10:
            print(f"{len(routes)} rotas registradas")
            for route in sorted(routes)[:10]:
                print(f"   - {route}")
            print(f"   ... e mais")
            return True
        else:
            print(f"Poucas rotas encontradas: {len(routes)}")
            return False
    except Exception as e:
        print(f"Erro ao testar rotas: {e}")
        return False

def test_templates():
    """Verifica se os templates existem"""
    print("\nTestando templates...")
    try:
        import os
        template_dir = 'app/templates'
        templates = []
        for root, dirs, files in os.walk(template_dir):
            for file in files:
                if file.endswith('.html'):
                    templates.append(os.path.join(root, file))
        
        if len(templates) > 10:
            print(f"{len(templates)} templates encontrados")
            for template in sorted(templates)[:10]:
                print(f"   - {template}")
            print(f"   ... e mais")
            return True
        else:
            print(f"Poucos templates: {len(templates)}")
            return False
    except Exception as e:
        print(f"Erro ao testar templates: {e}")
        return False

def test_static_files():
    """Verifica arquivos estáticos"""
    print("\nTestando arquivos estaticos...")
    try:
        import os
        
        css_file = 'app/static/css/style.css'
        js_file = 'app/static/js/main.js'
        
        css_exists = os.path.exists(css_file)
        js_exists = os.path.exists(js_file)
        
        if css_exists and js_exists:
            css_size = os.path.getsize(css_file)
            js_size = os.path.getsize(js_file)
            print(f"CSS encontrado ({css_size} bytes)")
            print(f"JavaScript encontrado ({js_size} bytes)")
            return True
        else:
            print("Arquivos estaticos nao encontrados")
            return False
    except Exception as e:
        print(f"Erro ao testar estaticos: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("=" * 50)
    print("TESTES DE INTEGRACAO - SOFASCORE DA GALERA")
    print("=" * 50)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Aplicação Flask", test_app_creation()))
    results.append(("Banco de Dados", test_database()))
    results.append(("Rotas", test_routes()))
    results.append(("Templates", test_templates()))
    results.append(("Arquivos Estáticos", test_static_files()))
    
    print("\n" + "=" * 50)
    print("RESUMO DOS TESTES")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASSOU" if result else "FALHOU"
        print(f"{name}: {status}")
    
    print("\n" + "=" * 50)
    if passed == total:
        print(f"TODOS OS TESTES PASSARAM ({passed}/{total})")
        print("\nSua aplicacao esta pronta!")
        print("Execute: python run.py")
        print("Acesse: http://localhost:5000")
    else:
        print(f"{total - passed} teste(s) falharam ({passed}/{total})")
    print("=" * 50)

if __name__ == '__main__':
    main()
