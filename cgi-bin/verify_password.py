#a function to verify either bcrypt or sha256 passwords
import bcrypt
from hashlib import sha256

def verify_password(password,hashedword):
	'''a function to verify either bcrypt or sha256 passwords'''
	if hashedword[:3]=="$2b":
		return bcrypt.checkpw(password.encode(),hashedword.encode())
	else:
		hash=sha256()
		hash.update(password.encode())
		return hash.hexdigest() == hashedword
