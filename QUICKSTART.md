# SofaScore da Galera - Guia Rápido de Início

## 🚀 Começar em 5 minutos

### 1️⃣ Abrir o terminal

```bash
cd "c:\Users\Usuario\Desktop\SOFASCORE DUS GURI"
```

### 2️⃣ Instalar dependências (primeira vez apenas)

```bash
pip install -r requirements.txt
```

### 3️⃣ Executar a aplicação

```bash
python run.py
```

### 4️⃣ Acessar no navegador

```
http://localhost:5000
```

---

## 📋 Primeira Configuração

### Criar uma Temporada

1. Clique em **Temporadas** no menu
2. Clique em **+ Nova Temporada**
3. Preencha:
   - Ano: 2026
   - Nome: Temporada 2026
   - Marque "Ativar esta temporada"
4. Clique em **Criar Temporada**

### Adicionar Jogadores

1. Clique em **Jogadores**
2. Clique em **+ Novo Jogador**
3. Preencha os dados:
   - Nome: (ex: João Silva)
   - Posição: (Goleiro, Defesa, Meia, Atacante)
   - Número da camisa: (ex: 10)
   - Avatar: (opcional)
4. Clique em **Cadastrar Jogador**

> Repita para todos os amigos que jogam!

### Criar sua Primeira Partida

1. Clique em **Partidas**
2. Clique em **+ Nova Partida**
3. Preencha:
   - Data: (escolha a data)
   - Local: (ex: Campo Municipal)
   - Temporada: Temporada 2026
   - Nome Time A: (ex: Time Vermelho)
   - Nome Time B: (ex: Time Azul)
4. Clique em **Criar Partida**

### Escalar Jogadores

1. Abra a partida que criou
2. Vá para a aba "**Time A**"
3. Selecione um jogador no dropdown
4. Clique em **Adicionar**
5. Repita para mais jogadores
6. Faça o mesmo para o Time B

### Registrar Gols

1. Abra a partida
2. Vá para a aba "**Gols**"
3. Selecione:
   - Time: (qual time marcou)
   - Artilheiro: (quem fez o gol)
   - Minuto: (opcional)
4. Clique em **Registrar Gol**
5. Opcionalmente, adicione a assistência

### Atribuir Notas

1. Abra a partida
2. Vá para a aba do time
3. Para cada jogador, digite a nota (0-10)
4. Clique **OK**

### Upload de Vídeos

1. Abra a partida
2. Vá para a aba "**Lances**"
3. Clique em "Upload de Vídeo"
4. Selecione o arquivo MP4
5. Preencha título, tipo e descrição
6. Clique em **Upload de Vídeo**

---

## 📊 Ver Estatísticas

1. Clique em **Estatísticas** no menu
2. Escolha uma métrica:
   - **🏆 Artilheiros** - Quem mais fez gols
   - **🅰️ Assistências** - Quem mais assistiu
   - **⭐ Notas Médias** - Quem teve melhor performance
3. Opcionalmente, filtre por temporada

---

## ⚙️ Dicas Práticas

### 🎯 Cores dos Times
- Escolha cores bem diferentes para identificar facilmente
- Ex: Vermelho vs Azul, Verde vs Laranja

### 📹 Vídeos
- Formatos aceitos: MP4 (recomendado), WebM, AVI, MKV
- Tamanho máximo: 500MB
- Dica: Comprima vídeos longos antes de enviar

### 👤 Avatares
- Use fotos quadradas (melhor visualização)
- Formatos: PNG, JPG, GIF, WebP
- Será exibido em círculo no perfil

### ⭐ Sistema de Notas
- 0-3: Fraco (vermelho)
- 4-6: Médio (amarelo)
- 7-10: Excelente (verde)

---

## 🛠️ Problemas Comuns

### A aplicação não inicia
```bash
# Verifique se as dependências estão instaladas
pip install -r requirements.txt

# Tente novamente
python run.py
```

### Não consigo fazer upload
- Verificar se existe a pasta `app/static/uploads/avatars/`
- Verificar se existe a pasta `app/static/uploads/videos/`
- Criar manualmente se não existir

### Banco de dados corrompido
```bash
# Delete o banco de dados (ele será recriado)
del instance\sofascore.db

# Reinicie a aplicação
python run.py
```

---

## 📱 Acessar de outro computador na rede

Se quiser que outros vejam a aplicação em outro PC:

1. Abra `run.py`
2. Mude a linha final para:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5000)
   ```
3. Reinicie: `python run.py`
4. Outros PCs acessam: `http://SEU_IP:5000`

Encontre seu IP com: `ipconfig` (Windows)

---

## 🎉 Bom jogo!

Aproveite para registrar cada partida com seus amigos e acompanhar as estatísticas!

Dúvidas? Consulte o **README.md** para mais informações.
