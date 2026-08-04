import random
import string

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation

    password = ""

    for i in range(length):
        password += random.choice(characters)

    return password


print("=" * 35)
print("     PASSWORD GENERATOR")
print("=" * 35)

length = int(input("Enter password length: "))

password = generate_password(length)

print("\nGenerated Password:")
print(password)