def vigenere_cipher_encrypt(plain_text, key):
    encrypted_text = ''
    key_length = len(key)
    for i, char in enumerate(plain_text):
        if char.isalpha():
            key_shift = ord(key[i % key_length].lower()) - ord('a')
            if char.islower():
                shifted = (ord(char) - ord('a') + key_shift) % 26 + ord('a')
            elif char.isupper():
                shifted = (ord(char) - ord('A') + key_shift) % 26 + ord('A')
            encrypted_text += chr(shifted)
        else:
            encrypted_text += char
    return encrypted_text


def vigenere_cipher_decrypt(encrypted_text, key):
    decrypted_text = ''
    key_length = len(key)
    for i, char in enumerate(encrypted_text):
        if char.isalpha():
            key_shift = ord(key[i % key_length].lower()) - ord('a')
            if char.islower():
                shifted = (ord(char) - ord('a') - key_shift) % 26 + ord('a')
            elif char.isupper():
                shifted = (ord(char) - ord('A') - key_shift) % 26 + ord('A')
            decrypted_text += chr(shifted)
        else:
            decrypted_text += char
    return decrypted_text


def encrypt_file_vigenere(input_file, output_file, key):
    with open(input_file, 'r') as file:
        text = file.read()
    encrypted_text = vigenere_cipher_encrypt(text, key)
    with open(output_file, 'w') as file:
        file.write(encrypted_text)


def decrypt_file_vigenere(input_file, output_file, key):
    with open(input_file, 'r') as file:
        encrypted_text = file.read()
    decrypted_text = vigenere_cipher_decrypt(encrypted_text, key)
    with open(output_file, 'w') as file:
        file.write(decrypted_text)


# Шифр Виженера
input_file = 'files/input.txt'
output_file = 'files/encrypted_vigenere.txt'
key = input("Enter key for Vigenere: ")

encrypt_file_vigenere(input_file, output_file, key)

decrypt_file_vigenere(output_file, 'files/decrypted_vigenere.txt', key)

print("Done")
