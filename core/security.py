from passlib.context import CryptContext
import bcrypt


CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verificar_senha(senha: str, hash_senha: str) -> bool:

    try:
      return CRIPTO.verify(senha, hash_senha)

    except Exception:
      return False
   
def gerar_hash_senha(senha: str) -> str:
   
    senha_bytes = senha.encode('utf-8')

    salt = bcrypt.gensalt()

    hash_bytes = bcrypt.hashpw(senha_bytes, salt)

    return hash_bytes.decode('utf-8')
