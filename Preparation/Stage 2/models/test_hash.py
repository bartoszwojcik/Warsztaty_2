#! python3

from models import hasher

salt_1 = hasher.generate_salt()
print(salt_1)

user_password_1 = "dupa123"
user_password_2 = "admin1"

salted_pw_1 = hasher.password_hash(user_password_1, salt_1)
salted_pw_2 = hasher.password_hash(user_password_2, salt_1)

print(hasher.check_password(user_password_1, salted_pw_1))
