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

    for i in range(len(plaintext)):
        if (plaintext[i]).isalpha():
            if (plaintext[i]).islower():
                n = ord(plaintext[i]) + (ord(key[i]) - ord("a"))
                while n > ord("z"):
                    n = n - (ord("z") - ord("a") + 1)
                while n < ord("a"):
                    n = n + (ord("z") - ord("a") + 1)
                ciphertext += chr(n)
            elif (plaintext[i]).isupper():
                n = ord(plaintext[i]) + (ord(key[i]) - ord("A"))
                while n > ord("Z"):
                    n = n - (ord("Z") - ord("A") + 1)
                while n < ord("A"):
                    n = n + (ord("Z") - ord("A") + 1)
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

    for i in range(len(ciphertext)):
        if (ciphertext[i]).isalpha():
            if (ciphertext[i]).islower():
                n = ord(ciphertext[i]) - (ord(key[i]) - ord("a"))
                while n > ord("z"):
                    n = n - (ord("z") - ord("a") + 1)
                while n < ord("a"):
                    n = n + (ord("z") - ord("a") + 1)
                plaintext += chr(n)
            elif (ciphertext[i]).isupper():
                n = ord(ciphertext[i]) - (ord(key[i]) - ord("A"))
                while n > ord("Z"):
                    n = n - (ord("Z") - ord("A") + 1)
                while n < ord("A"):
                    n = n + (ord("Z") - ord("A") + 1)
                plaintext += chr(n)
        else:
            plaintext += ciphertext[i]
    return plaintext


# done
