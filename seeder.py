import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), "server"))
load_dotenv(os.path.join(os.path.dirname(__file__), "server", ".env"))

from server.database.repository import log_message
log_message("5561982062789", "Tudo certo! Chat Monitor ativado!", sender="user")
print("✅ Banco alimentado com .env sucesso")
