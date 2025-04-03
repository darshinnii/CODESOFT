import random
import string

def get_password_complexity():
    """Prompt user to select password complexity level."""
    print("\nPassword Complexity Levels:")
    print("1. Weak ")
    print("2. Medium")
    print("3. Strong")
    print("4. Custom")
    
    while True:
        try:
            choice = int(input("Select complexity level (1-4): "))
            if 1 <= choice <= 4:
                return choice
            print("Please enter a number between 1 and 4")
        except ValueError:
            print("Please enter a valid number")

def get_custom_complexity():
    """Prompt user for custom character set preferences."""
    print("\nCustom Complexity Options:")
    include_upper = input("Include uppercase letters? (y/n): ").lower() == 'y'
    include_digits = input("Include digits? (y/n): ").lower() == 'y'
    include_special = input("Include special characters? (y/n): ").lower() == 'y'
    return include_upper, include_digits, include_special

def get_password_length():
    """Prompt user for password length with validation."""
    while True:
        try:
            length = int(input("Enter password length (8-20): "))
            if 8 <= length <= 20:
                return length
            print("Password length must be between 8 and 64 characters")
        except ValueError:
            print("Please enter a valid number")

def generate_password(length, complexity):
    """
    Generate a random password based on specified length and complexity.
    
    Parameters:
    - length: int, length of password (8-64)
    - complexity: tuple indicating which character sets to include
    
    Returns:
    - str: generated password
    """
    include_upper, include_digits, include_special = complexity
    
    chars = string.ascii_lowercase
    if include_upper:
        chars += string.ascii_uppercase
    if include_digits:
        chars += string.digits
    if include_special:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

    password = []
    if include_upper:
        password.append(random.choice(string.ascii_uppercase))
    if include_digits:
        password.append(random.choice(string.digits))
    if include_special:
        password.append(random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
    
    remaining = length - len(password)
    password.extend(random.choice(chars) for _ in range(remaining))
    
    random.shuffle(password)
    
    return ''.join(password)

def main():
    print("=== Password Generator ===")
    
    length = get_password_length()
    complexity_choice = get_password_complexity()
    
    if complexity_choice == 1:
        complexity = (False, False, False)  
    elif complexity_choice == 2:
        complexity = (True, True, False)   
    elif complexity_choice == 3:
        complexity = (True, True, True)    
    else:
        complexity = get_custom_complexity()  
    
    password = generate_password(length, complexity)
    print("\nGenerated Password:", password)
    print("Password length:", len(password))

if __name__ == "__main__":
    main()