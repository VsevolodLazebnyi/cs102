def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for i in plaintext:
        if i.isupper():
            n = ord(i) - ord("A")
            n = (n + shift) % 26 + ord("A")
            ciphertext += chr(n)
        elif i.islower():
            n = ord(i) - ord("a")
            n = (n + shift) % 26 + ord("a")
            ciphertext += chr(n)
        else:
            ciphertext += i
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for i in ciphertext:
        if i.isupper():
            n = ord(i) - ord("A")
            n = (n - shift) % 26 + ord("A")
            plaintext += chr(n)
        elif i.islower():
            n = ord(i) - ord("a")
            n = (n - shift) % 26 + ord("a")
            plaintext += chr(n)
        else:
            plaintext += i
    return plaintext
