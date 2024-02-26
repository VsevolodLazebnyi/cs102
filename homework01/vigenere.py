def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    key = keyword * (len(plaintext) // len(keyword) + 1)

    for i, _ in enumerate(plaintext):
        if plaintext[i].isalpha():
            if plaintext[i].islower():
                n = (ord(plaintext[i]) + ord(key[i]) - 2 * ord("a")) % 26
                n += ord("a")
                ciphertext += chr(n)
            elif (plaintext[i]).isupper():
                n = (ord(plaintext[i]) + ord(key[i])) % 26
                n += ord("A")
                ciphertext += chr(n)
        else:
            ciphertext += plaintext[i]
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    key = keyword * (len(ciphertext) // len(keyword) + 1)

    for i, _ in enumerate(ciphertext):
        if ciphertext[i].isalpha():
            n = (ord(ciphertext[i]) - ord(key[i]) + (ord("z") - ord("a") + 1)) % 26
            if ciphertext[i].islower():
                n += ord("a")
                plaintext += chr(n)
            elif (ciphertext[i]).isupper():
                n += ord("A")
                plaintext += chr(n)
        else:
            plaintext += ciphertext[i]
    return plaintext


# done
