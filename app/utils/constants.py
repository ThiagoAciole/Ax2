# === 🧩 Informações gerais ===
APP_NAME = "AX2"
APP_TITLE = "AX2 – Gerenciador de Jogos PS2"
DEFAULT_LABEL = "AX2"
DEFAULT_SECTION_TITLE = "Jogos"
ICON_NAME = "icon.ico"

# === ⚙️ Mensagens de status ===
STATUS_PREPARING = "Preparando ambiente..."
STATUS_LOADING = "Carregando..."
STATUS_DOWNLOADING = "Baixando DuckStation..."
STATUS_EXTRACTING = "Extraindo arquivos..."
STATUS_READY = "Axis instalado e pronto!"
STATUS_UPDATING_LIST = "🔄 Atualizando lista de jogos..."
STATUS_UPDATE_SUCCESS = "✅ Lista de jogos atualizada com sucesso!"
STATUS_UPDATE_ERROR = "❌ Falha ao atualizar lista de jogos."

# === 🎮 Mensagens relacionadas a jogos ===
GAME_START_INFO = "[INFO] Jogo iniciado. Pressione ESC ou L1+X para sair."
GAME_START_ERROR = "Falha ao iniciar o jogo:\n{erro}"
GAME_NOT_FOUND = "O jogo '{arquivo}' não foi encontrado em /roms."
EMU_NOT_FOUND = "DuckStation não encontrado na pasta /game."
GAME_DELETE_CONFIRM = "Deseja realmente excluir '{jogo}'?\nA ROM e a capa serão removidas."
GAME_DELETE_SUCCESS = "O jogo '{jogo}' foi excluído com sucesso."
GAME_DELETE_ERROR = "Erro ao excluir o jogo:\n{erro}"

# === 🖼️ Mensagens sobre capas ===
COVER_SELECT_TITLE = "Selecionar nova capa para {jogo}"
COVER_UPDATED = "Capa de '{jogo}' alterada com sucesso!"
COVER_UPDATE_ERROR = "Falha ao alterar capa:\n{erro}"

# === 📂 Mensagens sobre arquivos e downloads ===
FILE_NOT_FOUND = "O arquivo '{nome}' não foi encontrado."
INVALID_JSON = "O arquivo games.json está em formato inválido."
JSON_LOAD_ERROR = "Erro ao carregar o arquivo games.json:\n{erro}"
DOWNLOAD_FAILED = "Falha no download: {erro}"
DOWNLOAD_GAME_SUCCESS = "✅ Instalação concluída: {jogo}"
DOWNLOAD_GAME_ERROR = "❌ Falha ao instalar {jogo}"

# === 🔍 Interface e busca ===
NO_GAMES_FOUND = "Nenhum jogo encontrado!"
SEARCH_PLACEHOLDER = "Buscar jogos..."
UPDATE_SUCCESS_LOG = "✅ Lista atualizada com sucesso!"
UPDATE_ERROR_LOG = "❌ Falha ao atualizar lista."

# === 🧠 Mensagens de log e avisos ===
WARN_COPY_DEFAULT = "[AVISO] Falha ao copiar arquivos padrão: {erro}"
INFO_CONTROLLER_DETECTED = "[INFO] Controle detectado: {nome}"
WARN_NO_CONTROLLER = "[AVISO] Nenhum controle detectado. Apenas ESC funcionará."
INFO_COMBO_EXIT = "[INFO] L1 + X pressionados por 1s — encerrando o jogo..."
