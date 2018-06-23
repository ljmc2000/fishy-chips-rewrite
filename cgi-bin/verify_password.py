import bcrypt
from hashlib import sha256

def verify_password(password,hashedword):
	if hashedword[:3]=="$2b":
		return bcrypt.checkpw(password.encode(),hashedword.encode())
	else:
		hash=sha256()
		hash.update(password.encode())
		return hash.hexdigest() == hashedword
