import sys, os, base64, getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import boto3
from simple_term_menu import TerminalMenu

# python3 -m pip install cryptography
# python3 -m pip install boto3
# python3 -m pip install simple-term-menu


file_path = os.path.realpath(__file__)
cred_file = f"{os.path.dirname(file_path)}/.aws-credentials.crypt"
salt_file = f"{os.path.dirname(file_path)}/.aws-credentials.salt"

data = ""
salt = ""
with open(cred_file, "r") as text_file:
    data = text_file.read().replace("\n","")

with open(salt_file, "rb") as text_file:
    salt = text_file.read()

if data == "":
    print("No .aws-credentials.crypt file found. Create one first!")
    sys.exit(1)

if salt == "":
    print("No .aws-credentials.salt file found. Create one first!")
    sys.exit(1)

print("Type in your password for encrypted credentials:")
password = getpass.getpass()

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=390000,
)
key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
fernet = Fernet(key)

decrypt = fernet.decrypt(data.encode()).decode()

iam_client = boto3.client(
    "iam",
    aws_access_key_id=decrypt.split(" ")[0],
    aws_secret_access_key=decrypt.split(" ")[1]
    )
roles = iam_client.list_roles()
role_list = roles['Roles']
def display_name(role_entry):
    return f"{role_entry['RoleName']} + ({role_entry['Arn']})"
terminal_menu = TerminalMenu(map(display_name, role_list))
choice_index = terminal_menu.show()

selected_role_arn = role_list[choice_index]["Arn"]
print(f"selected arn: {selected_role_arn}")


print("creating new session with role")
sts_client = boto3.client(
    "sts",
    aws_access_key_id=decrypt.split(" ")[0],
    aws_secret_access_key=decrypt.split(" ")[1]
    )
assumed_role = sts_client.assume_role(
    RoleArn=selected_role_arn,
    RoleSessionName="TemporaryDeveloperSession"
)
credentials = assumed_role["Credentials"]

aws_region = "eu-central-1"
aws_access_key_id = credentials['AccessKeyId']
aws_secret_access_key=credentials['SecretAccessKey']
aws_session_token=credentials['SessionToken']

print("setting region ...")
os.system(f"aws configure set region {aws_region}")
print("setting aws_access_key_id ...")
os.system(f"aws configure set aws_access_key_id {aws_access_key_id}")
print("setting region ...")
os.system(f"aws configure set aws_secret_access_key {aws_secret_access_key}")
print("setting aws_session_token ...")
os.system(f"aws configure set aws_session_token {aws_session_token}")

print("Successfully assumed role. Credentials are valid for 12h")