# 🚀 Instruções de Execução - SofaScore da Galera

## ⚡ Forma Mais Rápida (Recomendada)

### Windows (PowerShell ou CMD)

```bash
# 1. Abra o terminal na pasta do projeto
cd "c:\Users\Usuario\Desktop\SOFASCORE DUS GURI"

# 2. Instale as dependências (primeira vez apenas)
pip install -r requirements.txt

# 3. Execute a aplicação
python run.py
```

### Linux/Mac

```bash
# 1. Navegue até a pasta
cd ~/Desktop/SOFASCORE DUS GURI

# 2. Crie um ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # No Mac, use: source venv/bin/activate

# 3. Instale dependências
pip install -r requirements.txt

# 4. Execute
python3 run.py
```

---

## 🌐 Acessar a Aplicação

Após executar `python run.py`, você verá algo como:

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

**Abra seu navegador e acesse:**
```
http://localhost:5000
```

---

## ⚙️ Configurações Importantes

### Acessar de Outro Computador (Rede Local)

Se quiser que outros computadores da rede acessem:

1. Abra `run.py`
2. Mude a última linha para:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5000)
   ```
3. Descubra seu IP:
   - **Windows:** `ipconfig` (procure por IPv4)
   - **Linux/Mac:** `ifconfig` (procure por inet)
4. Outros acessam: `http://SEU_IP:5000`

### Mudar Porta

Se a porta 5000 estiver em uso:

```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Usar porta 8080
```

Acessar: `http://localhost:8080`

---

## 🧪 Adicionar Dados de Teste (Opcional)

```bash
python populate_db.py
```

Isso criará:
- ✅ 1 Temporada (2026)
- ✅ 8 Jogadores
- ✅ 1 Partida de exemplo
- ✅ 3 Gols registrados
- ✅ Dados prontos para explorar

---

## ✅ Validar a Instalação

```bash
python test_integration.py
```

Você verá um relatório completo dos testes.

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'flask'"

**Solução:**
```bash
pip install Flask==2.3.3 Flask-SQLAlchemy==3.0.5 Werkzeug==2.3.7
```

Ou:
```bash
pip install -r requirements.txt
```

---

### Erro: "Address already in use"

**Significa:** Outra aplicação está usando a porta 5000.

**Soluções:**
1. Fechar a outra aplicação
2. Usar outra porta:
   ```python
   app.run(debug=True, host='0.0.0.0', port=8080)
   ```

---

### Banco de dados corrompido

**Solução:** Remova o arquivo de banco e deixe recriar:

```bash
# Windows
del instance\sofascore.db

# Linux/Mac
rm instance/sofascore.db

# Reinicie
python run.py
```

---

### Vídeos não carregam

- Verificar se está em formato MP4
- Confirmar tamanho (máx 500MB)
- Verificar diretório `app/static/uploads/videos/`

---

### Imagens não aparecem

- Verificar se a pasta `app/static/uploads/avatars/` existe
- Verificar se o arquivo foi salvo corretamente

---

## 📦 Dependências Instaladas

```bash
pip install -r requirements.txt
```

Instala:
- Flask 2.3.3
- Flask-SQLAlchemy 3.0.5
- Werkzeug 2.3.7

Tamanho total: ~50MB

---

## 🔄 Ambiente Virtual (Recomendado para Produção)

### Criar

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Após ativar

```bash
pip install -r requirements.txt
python run.py
```

### Desativar (quando terminar)

```bash
deactivate
```

---

## 📊 Verificar Versões

```bash
python --version        # Python (precisa 3.8+)
pip --version           # pip (package manager)
python -m flask --version  # Flask (após instalar)
```

---

## 🎯 Workflow Completo

```bash
# 1. Abrir terminal na pasta
cd "c:\Users\Usuario\Desktop\SOFASCORE DUS GURI"

# 2. Instalar (primeira vez)
pip install -r requirements.txt

# 3. Adicionar dados (opcional)
python populate_db.py

# 4. Validar tudo
python test_integration.py

# 5. Executar
python run.py

# 6. Acessar
# Abrir navegador em: http://localhost:5000
```

---

## 💡 Dicas Úteis

### Modo Debug

Já está ativado em `run.py`. Mudanças no código recarregam automaticamente.

### Ver Logs

Todos os logs aparecem no terminal onde executou `python run.py`.

### Parar a Aplicação

Pressione `Ctrl + C` no terminal.

---

## 🚀 Para Produção

Quando for usar em produção:

1. Mude `debug=False` em `run.py`
2. Use um servidor como Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```
3. Configure um proxy reverso (Nginx)
4. Use HTTPS com SSL

---

## 📞 Suporte

- Consulte README.md para mais informações
- Veja QUICKSTART.md para guia rápido
- Verifique o código comentado em cada arquivo

---

**Tudo pronto! Bom jogo! ⚽🎯**
