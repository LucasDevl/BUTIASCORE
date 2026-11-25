"""Entry point da aplicação"""
from app import create_app
import os

if __name__ == '__main__':
    app = create_app()
    debug = os.environ.get('FLASK_DEBUG', '1') == '1'
    port = int(os.environ.get('PORT', '5000'))
    app.run(debug=debug, host='0.0.0.0', port=port)
