import random

print("=" * 40)
print("🎮 Number Guessing Game")
print("=" * 40)

# Fixed number for testing
secret_number = 25

attempts = 0

while True:
    guess = int(input("Enter a number between 1 and 100: "))
    attempts += 1

    if guess < secret_number:
        print("Too Low!")

    elif guess > secret_number:
        print("Too High!")

    else:
        print("\n🎉 Congratulations!")
        print(f"You guessed the number in {attempts} attempt(s).")
        break