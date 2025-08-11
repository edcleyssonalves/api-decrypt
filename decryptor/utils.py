import base64
import requests
import uuid
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

INFO_KEYS = {
    "image": b"WhatsApp Image Keys",
    "video": b"WhatsApp Video Keys",
    "audio": b"WhatsApp Audio Keys",
    "document": b"WhatsApp Document Keys"
}

def descriptografar_midia(media_url: str, media_key_b64: str, tipo_midia: str) -> tuple[bytes, str]:
    """
    Descriptografa mídia do WhatsApp (.enc) e retorna conteúdo em bytes e extensão do arquivo.
    """
    if tipo_midia not in INFO_KEYS:
        raise ValueError(f"Tipo de mídia inválido: {tipo_midia}")

    response = requests.get(media_url)
    if response.status_code != 200:
        raise Exception(f"Erro ao baixar mídia: HTTP {response.status_code}")
    encrypted_data = response.content

    extra_bytes = len(encrypted_data) % 16
    if extra_bytes != 0:
        encrypted_data = encrypted_data[:-extra_bytes]

    media_key = base64.b64decode(media_key_b64)
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=112,
        salt=None,
        info=INFO_KEYS[tipo_midia],
        backend=default_backend()
    )
    expanded_key = hkdf.derive(media_key)
    iv = expanded_key[0:16]
    cipher_key = expanded_key[16:48]

    cipher = Cipher(algorithms.AES(cipher_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    extensao = ".pdf" if tipo_midia == "document" else ".jpg"
    return unpadded_data, extensao
