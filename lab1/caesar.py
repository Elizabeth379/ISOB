def caesar_cipher_encrypt(text, shift):
    encrypted_text = ''
    for char in text:
        if char.isalpha():
            shifted = ord(char) + (shift % 26)
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            encrypted_text += chr(shifted)
        else:
            encrypted_text += char
    return encrypted_text



def caesar_cipher_decrypt(encrypted_text, shift):
    return caesar_cipher_encrypt(encrypted_text, -shift)


def encrypt_file_caesar(input_file, output_file, shift):
    with open(input_file, 'r') as file:
        text = file.read()
    encrypted_text = caesar_cipher_encrypt(text, shift)
    with open(output_file, 'w') as file:
        file.write(encrypted_text)


def decrypt_file_caesar(input_file, output_file, shift):
    with open(input_file, 'r') as file:
        encrypted_text = file.read()
    decrypted_text = caesar_cipher_decrypt(encrypted_text, shift)
    with open(output_file, 'w') as file:
        file.write(decrypted_text)

# Шифр Цезаря
input_file = 'files/input.txt'
output_file = 'files/encrypted_caesar.txt'

while True:
    shift = input("Enter shift for Caesar: ")
    try:
        shift=int(shift)
        break
    except ValueError:
        print("Error: enter correct number")

encrypt_file_caesar(input_file, output_file, shift)

decrypt_file_caesar(output_file, 'files/decrypted_caesar.txt', shift)

print("Done!")
