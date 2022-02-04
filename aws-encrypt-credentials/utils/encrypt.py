import sys, os, base64, getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# python3 -m pip install cryptography
# python3 -m pip install boto3
# python3 -m pip install simple-term-menu


print("First set a new password:")
password1 = getpass.getpass()
print("Repeat the new password:")
password2 = getpass.getpass()

if password1 != password2:
    print("The two passwords don't match!")
    sys.exit()

salt = os.urandom(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=390000,
)
key = base64.urlsafe_b64encode(kdf.derive(password1.encode()))
fernet = Fernet(key)


print("Type in AWS_ACCESS_KEY_ID")
aws_access_key_id = input()

print("Type in AWS_SECRET_ACCESS_KEY")
aws_secret_access_key = input()

cmd = f"{aws_access_key_id} {aws_secret_access_key}"


cmd = fernet.encrypt(cmd.encode()).decode()

file_path = os.path.realpath(__file__)
new_file = f"{os.path.dirname(file_path)}/.aws-credentials.crypt"
salt_file = f"{os.path.dirname(file_path)}/.aws-credentials.salt"

with open(new_file, "w") as text_file:
    text_file.write(cmd)

with open(salt_file, "wb") as text_file:
    text_file.write(salt)