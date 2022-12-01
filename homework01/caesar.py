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
        if i.isalpha():
            if i.islower():
                n = ord(i) + (shift % (ord("z") - ord("a") + 1))
                if n > ord("z"):
                    n = n - (ord("z") - ord("a") + 1)
                elif n < ord("a"):
                    n = n + (ord("z") - ord("a") + 1)
                ciphertext += chr(n)
            else:
                n = ord(i) + (shift % (ord("z") - ord("a") + 1))
                if n > ord("Z"):
                    n = n - (ord("Z") - ord("A") + 1)
                elif n < ord("A"):
                    n = n + (ord("Z") - ord("A") + 1)
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
        if i.isalpha():
            if i.islower():
                n = ord(i) - (shift % (ord("z") - ord("a") + 1))
                if n > ord("z"):
                    n = n - (ord("z") - ord("a") + 1)
                elif n < ord("a"):
                    n = n + (ord("z") - ord("a") + 1)
                plaintext += chr(n)
            else:
                n = ord(i) - (shift % (ord("z") - ord("a") + 1))
                if n > ord("Z"):
                    n = n - (ord("Z") - ord("A") + 1)
                elif n < ord("A"):
                    n = n + (ord("Z") - ord("A") + 1)
                plaintext += chr(n)
        else:
            plaintext += i
    return plaintext


# done
