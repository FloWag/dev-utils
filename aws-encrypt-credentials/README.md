# Tool to Login to AWS CLI securely (no permanent unencrypted credentials on your machine)

## How it works
1. Create AWS User with following permissions: STSAssumeRole, IAMListRoles
2. Create Role with permissions for your development purposes (you could name it DeveloperRole)
3. Allow AWS User (you created in step 1) to assume the Role
4. Retrieve AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
5. Save them encrypted using `encrypt-aws-credentials.sh` and a self chosen password

Each time you want to use AWS CLI, you can use `aws-login.sh`. It will automatically decrypt the credentials with your password and login your AWS CLI with temporary (12h valid) credentials by assuming the role from step 2.

## Requirements
- Python 3
- AWS CLI
```
python3 -m pip install cryptography
python3 -m pip install boto3
python3 -m pip install simple-term-menu
```