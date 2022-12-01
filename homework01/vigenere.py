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

    word_list = list(plaintext)
    key = list(keyword)
    while len(key) < len(word_list):
        key = key + key
    new_word = []

    for i in range(len(word_list)):
        if (word_list[i]).isalpha():
            if (word_list[i]).islower():
                n = ord(word_list[i]) + (ord(key[i]) - ord("a"))
                while n > ord("z"):
                    n = n - (ord("z") - ord("a") + 1)
                while n < ord("a"):
                    n = n + (ord("z") - ord("a") + 1)
                new_word.append(chr(n))
            elif (word_list[i]).isupper():
                n = ord(word_list[i]) + (ord(key[i]) - ord("A"))
                while n > ord("Z"):
                    n = n - (ord("Z") - ord("A") + 1)
                while n < ord("A"):
                    n = n + (ord("Z") - ord("A") + 1)
                new_word.append(chr(n))
        else:
            new_word.append(word_list[i])
    word_str = ""
    for j in range(len(new_word)):
        word_str = word_str + str(new_word[j])
    ciphertext = word_str
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

    word_list = list(ciphertext)
    key = list(keyword)
    while len(key) < len(word_list):
        key = key + key
    new_word = []

    for i in range(len(word_list)):
        if (word_list[i]).isalpha():
            if (word_list[i]).islower():
                n = ord(word_list[i]) - (ord(key[i]) - ord("a"))
                while n > ord("z"):
                    n = n - (ord("z") - ord("a") + 1)
                while n < ord("a"):
                    n = n + (ord("z") - ord("a") + 1)
                new_word.append(chr(n))
            elif (word_list[i]).isupper():
                n = ord(word_list[i]) - (ord(key[i]) - ord("A"))
                while n > ord("Z"):
                    n = n - (ord("Z") - ord("A") + 1)
                while n < ord("A"):
                    n = n + (ord("Z") - ord("A") + 1)
                new_word.append(chr(n))
        else:
            new_word.append(word_list[i])
    word_str = ""
    for j in range(len(new_word)):
        word_str = word_str + str(new_word[j])
    plaintext = word_str
    return plaintext


# done
