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

    word_list = list(plaintext)
    new_word = []

    for i in range(len(word_list)):
        if (word_list[i]).isalpha():
            if (word_list[i]).islower():
                n = ord(word_list[i]) + shift
                if n > ord("z"):
                    n = n - (ord("z") - ord("a") + 1)
                elif n < ord("a"):
                    n = n + (ord("z") - ord("a") + 1)
                new_word.append(chr(n))
            elif (word_list[i]).isupper():
                n = ord(word_list[i]) + shift
                if n > ord("Z"):
                    n = n - (ord("Z") - ord("A") + 1)
                elif n < ord("A"):
                    n = n + (ord("Z") - ord("A") + 1)
                new_word.append(chr(n))
        else:
            new_word.append(word_list[i])
    word_str = ""
    for j in range(len(new_word)):
        word_str = word_str + str(new_word[j])
    ciphertext = word_str
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

    word_list = list(ciphertext)
    new_word = []

    for i in range(len(word_list)):
        if (word_list[i]).isalpha():
            if (word_list[i]).islower():
                n = ord(word_list[i]) - shift
                if n > ord("z"):
                    n = n - (ord("z") - ord("a") + 1)
                elif n < ord("a"):
                    n = n + (ord("z") - ord("a") + 1)
                new_word.append(chr(n))
            elif (word_list[i]).isupper():
                n = ord(word_list[i]) - shift
                if n > ord("Z"):
                    n = n - (ord("Z") - ord("A") + 1)
                elif n < ord("A"):
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
