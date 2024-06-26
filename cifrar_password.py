## Creación de la contraseña cifrada. Esto devuelve una cadena de caracteres. Por ejemlo: b'TkoIF/gh2iWI0H1hTyLIgQOAOjT9LdEhDhzOfUBfBDw='
from Crypto.Cipher import AES
from mys import mys
# Cipher
cipher = AES.new(mys.encode("utf8"), AES.MODE_ECB)
base64.b64encode(cipher.encrypt('lapassword que quieras'.rjust(32)))


# Código para descifrar la contreseña:
password_descifrada = cipher.decrypt(base64.b64decode("TkoIF/gh2iWI0H1hTyLIgQOAOjT9LdEhDhzOfUBfBDw=")).strip().decode("utf-8")
