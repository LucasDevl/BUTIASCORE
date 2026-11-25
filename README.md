# SofaScore da Galera 🎯⚽

Um aplicativo web inspirado no SofaScore para gerenciar partidas de futebol entre amigos que jogam semanalmente.

## Características

✅ **Gerenciamento de Jogadores**
- Cadastro com foto de perfil
- Posição, número de camisa
- Estatísticas automáticas (gols, assistências, notas)

✅ **Partidas**
- Criação com Times A e B
- Escudos pré-cadastrados do Butiá FC Preto e Branco ou upload de escudos próprios
- Escalação automática ou divisão manual dos times
- Formações de 7 ou 8 jogadores em campo, com banco de reservas
- Ajuste manual de quem ocupa cada posição no campo
- Visão comparativa horizontal das duas escalações da partida
- Registro de gols e assistências
- Placar visual com escudos, autores e minutos dos gols
- Atribuição de notas (0-10)
- Upload de vídeos de lances
- Área de patrocinadores do clube

✅ **Temporadas**
- Organizar partidas por temporadas
- Rankings dinâmicos
- Estatísticas por temporada

✅ **Estatísticas e Rankings**
- Top artilheiros
- Top assistências
- Ranking por nota média
- Filtro por temporada

✅ **Lances em Vídeo**
- Upload de vídeos (mp4)
- Ligação com jogadores
- Classificação (gol, assistência, outro)
- Player HTML5 integrado

## Stack Técnico

- **Backend:** Python com Flask
- **Database:** SQLite local ou PostgreSQL gerenciado (Neon) com SQLAlchemy ORM
- **Frontend:** HTML, CSS, JavaScript puro
- **Upload:** Sistema de arquivos local ou Vercel Blob

## Instalação

### Pré-requisitos
- Python 3.8+
- pip

### Passo 1: Clonar e navegar
```bash
cd "c:\Users\Usuario\Desktop\SOFASCORE DUS GURI"
```

### Passo 2: Criar ambiente virtual (Opcional, mas recomendado)
```bash
python -m venv venv
```

**Ativar o ambiente:**
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

### Passo 3: Instalar dependências
```bash
pip install -r requirements.txt
```

### Passo 4: Criar diretório de instância (se necessário)
```bash
mkdir instance
```

### Passo 5: Executar a aplicação
```bash
python run.py
```

A aplicação estará disponível em: **http://localhost:5000**

## Estrutura do Projeto

```
SOFASCORE DUS GURI/
├── app/
│   ├── __init__.py              # Factory da aplicação
│   ├── models/                  # Modelos SQLAlchemy
│   │   ├── player.py
│   │   ├── season.py
│   │   ├── match.py
│   │   ├── team.py
│   │   ├── goal.py
│   │   ├── assist.py
│   │   ├── video.py
│   │   ├── player_match.py
│   │   ├── player_stats.py
│   │   ├── match_lineup.py
│   │   ├── lineup_slot.py
│   │   └── __init__.py
│   ├── routes/                  # Rotas Flask
│   │   ├── main.py
│   │   ├── players.py
│   │   ├── seasons.py
│   │   ├── matches.py
│   │   ├── stats.py
│   │   └── __init__.py
│   ├── templates/               # Arquivos HTML
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── players/
│   │   ├── matches/
│   │   ├── seasons/
│   │   └── stats/
│   └── static/                  # Assets estáticos
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   └── main.js
│       └── uploads/
│           ├── avatars/
│           └── videos/
├── instance/                    # Banco de dados (criado automaticamente)
├── run.py                       # Entry point
└── requirements.txt             # Dependências
```

## Guia de Uso

### 1. Criar Temporada
1. Navegue para "Temporadas"
2. Clique em "+ Nova Temporada"
3. Preencha os dados (ano, nome, descrição)
4. Marque "Ativar esta temporada" se for usar agora

### 2. Cadastrar Jogadores
1. Vá para "Jogadores"
2. Clique em "+ Novo Jogador"
3. Preencha: Nome, Posição, Número da Camisa, Avatar (opcional)

### 3. Criar Partida
1. Vá para "Partidas"
2. Clique em "+ Nova Partida"
3. Preencha: Data, Local, Temporada
4. Nomeie os dois times e escolha cores

### 4. Escalar Jogadores
1. Na visualização da partida, escolha 7 ou 8 jogadores em campo e uma formação
2. Selecione os jogadores e escolha a divisão automática ou manual entre os times
3. Jogadores além das vagas em campo ficam no banco de reservas
4. Na aba de cada time, clique em uma posição do campo para escolher, trocar ou deixar um jogador no banco

### 5. Registrar Gols
1. Na aba "Gols" da partida
2. Selecione o time, jogador e minuto
3. O placar é atualizado automaticamente
4. Adicione assistência (opcional)

### 6. Atribuir Notas
1. Na aba do time, para cada jogador
2. Digite a nota (0-10)
3. Clique "OK"

### 7. Upload de Vídeos
1. Na aba "Lances"
2. Selecione o vídeo, título, tipo
3. Clique "Upload de Vídeo"

### 8. Ver Estatísticas
1. Vá para "Estatísticas"
2. Selecione uma métrica (gols, assistências, notas)
3. Filtre por temporada se desejar

## Deploy no Vercel

O projeto usa `wsgi.py` como entrypoint Flask. Para manter dados e arquivos entre execuções serverless:

1. Conecte o projeto a um banco Neon PostgreSQL e a um Vercel Blob público.
2. Configure `DATABASE_URL`, `SECRET_KEY` e `MEDIA_STORAGE=vercel_blob`. A conexão do Blob deve disponibilizar `BLOB_STORE_ID` e as credenciais OIDC do projeto, ou `BLOB_READ_WRITE_TOKEN`.
3. Configure `VERCEL_SUPPORT_LARGE_REQUEST_BODY=1` para habilitar requisições de até 20 MiB. Esse recurso beta exige Pro/Enterprise e a memória de performance de 4 GB, definida em **Project Settings → Functions**; `vercel.json` configura a duração máxima da função.
4. Faça o primeiro deploy com o projeto privado e crie o administrador em `/auth/setup` antes de compartilhar o endereço.

O deploy começa com banco vazio. A base SQLite e os arquivos locais não são enviados automaticamente. No Vercel, o corpo total da requisição de upload (arquivo e campos do formulário) precisa caber em 20 MiB; localmente, o limite permanece em 500 MiB.

## Modelos do Banco de Dados

### Player
- id (PK)
- name
- position
- shirt_number
- avatar (caminho da imagem)

### Season
- id (PK)
- year
- name
- description
- is_active

### Match
- id (PK)
- date
- location
- season_id (FK)
- team_a_id (FK)
- team_b_id (FK)
- score_a
- score_b
- status (agendada, em_andamento, finalizada)

### Team
- id (PK)
- name
- color (hexadecimal)
- logo (imagem pré-cadastrada ou enviada)

### PlayerMatch
- id (PK)
- player_id (FK)
- match_id (FK)
- team_id (FK)
- rating (0-10)

### MatchLineup
- match_id (FK, único)
- players_on_field (7 ou 8)
- formation

### LineupSlot
- match_id (FK)
- team_id (FK)
- player_id (FK, único por partida)
- slot_key (posição na formação)

### Goal
- id (PK)
- match_id (FK)
- team_id (FK)
- scorer_id (FK)
- minute

### Assist
- id (PK)
- goal_id (FK)
- match_id (FK)
- assister_id (FK)

### Video
- id (PK)
- match_id (FK)
- player_id (FK, opcional)
- filename
- video_type (gol, assistencia, outro)
- title
- description

## API Endpoints

### Jogadores
- `GET /players/` - Lista todos
- `GET /players/<id>` - Visualizar
- `POST /players/create` - Criar
- `POST /players/<id>/edit` - Editar
- `POST /players/<id>/delete` - Deletar
- `GET /players/api/search?q=...` - Buscar

### Partidas
- `GET /matches/` - Lista todas
- `GET /matches/<id>` - Visualizar
- `POST /matches/create` - Criar
- `POST /matches/<id>/add-player` - Escalar jogador
- `POST /matches/<id>/add-goal` - Registrar gol
- `POST /matches/<id>/add-assist/<goal_id>` - Registrar assistência
- `POST /matches/<id>/rate-player` - Atribuir nota
- `POST /matches/<id>/upload-video` - Upload de vídeo

### Temporadas
- `GET /seasons/` - Lista todas
- `GET /seasons/<id>` - Visualizar
- `POST /seasons/create` - Criar
- `POST /seasons/<id>/activate` - Ativar temporada

### Estatísticas
- `GET /stats/` - Dashboard
- `GET /stats/scorers?season_id=...` - Artilheiros
- `GET /stats/assists?season_id=...` - Assistências
- `GET /stats/ratings?season_id=...` - Notas médias

## Recursos Futuros

- [ ] Autenticação de usuários
- [ ] Estatísticas avançadas (desarmes, passes, etc)
- [ ] Gráficos interativos
- [ ] Sistema de comentários nas partidas
- [ ] Notificações em tempo real
- [ ] App mobile (PWA)
- [ ] Integração com redes sociais
- [ ] Sistema de convites

## Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'flask'"
**Solução:** Instale as dependências: `pip install -r requirements.txt`

### Erro: "Arquivo não encontrado" ao fazer upload
**Solução:** Verifique se o diretório `app/static/uploads/` existe com subpastas `avatars` e `videos`

### Banco de dados não carrega
**Solução:** Remova `instance/sofascore.db` e reinicie a aplicação para recriar

### Vídeos não carregam
**Solução:** Verifique o formato do vídeo (MP4 é recomendado). Localmente, o limite é 500 MiB; no Vercel, o corpo total da requisição está limitado a 20 MiB.

## Contribuindo

Este é um projeto pessoal. Sinta-se livre para fazer fork, modificar e evoluir!

## Licença

MIT License - Use livremente!

## Contato

Desenvolvido com ❤️ para a galera! ⚽

---

**Versão:** 1.0.0  
**Última atualização:** Janeiro 2026
