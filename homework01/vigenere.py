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

    Alpha_Big = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]
    Alpha_small = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]

    word_list = list(" ".join(map(str, (plaintext.split()))))
    key = list(" ".join(map(str, (keyword.split()))))
    while len(key) < len(word_list):
        key = key + key

    new_word = []
    for i in range(0, len(word_list)):
        if word_list[i] in Alpha_small:
            if key[i] in Alpha_small:
                n = Alpha_small.index(word_list[i]) + (int(Alpha_small.index(key[i])))
                while n >= len(Alpha_small) - 1:
                    n = n - len(Alpha_small)
                while n <= -(len(Alpha_small)):
                    n = n + len(Alpha_small) - 1
                else:
                    pass
                new_word.append(Alpha_small[n])

            elif key[i] in Alpha_Big:
                n = Alpha_small.index(word_list[i]) + (int(Alpha_Big.index(key[i])))
                while n >= len(Alpha_small) - 1:
                    n = n - len(Alpha_small)
                while n <= -(len(Alpha_small)):
                    n = n + len(Alpha_small) - 1
                else:
                    pass
                new_word.append(Alpha_small[n])

        elif word_list[i] in Alpha_Big:
            if key[i] in Alpha_small:
                n = Alpha_Big.index(word_list[i]) + (int(Alpha_small.index(key[i])))
                while n >= len(Alpha_small) - 1:
                    n = n - len(Alpha_small)
                while n <= -(len(Alpha_small)):
                    n = n + len(Alpha_small) - 1
                else:
                    pass
                new_word.append(Alpha_Big[n])

            elif key[i] in Alpha_Big:
                n = Alpha_Big.index(word_list[i]) + (int(Alpha_Big.index(key[i])))
                while n >= len(Alpha_small) - 1:
                    n = n - len(Alpha_small)
                while n <= -(len(Alpha_small)):
                    n = n + len(Alpha_small) - 1
                else:
                    pass
                new_word.append(Alpha_Big[n])
        else:
            new_word.append(word_list[i])
    word_str = ""
    for j in range(0, len(new_word)):
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
    Alpha_Big = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]
    Alpha_small = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]

    word_list = list(" ".join(map(str, (ciphertext.split()))))
    key = list(" ".join(map(str, (keyword.split()))))
    while len(key) < len(word_list):
        key = key + key

    new_word = []
    for i in range(0, len(word_list)):
        if word_list[i] in Alpha_small:
            if key[i] in Alpha_small:
                n = Alpha_small.index(word_list[i]) - (int(Alpha_small.index(key[i])))
                while n >= len(Alpha_small) - 1:
                    n = n - len(Alpha_small)
                while n <= -(len(Alpha_small)):
                    n = n + len(Alpha_small) - 1
                else:
                    pass
                new_word.append(Alpha_small[n])

            elif key[i] in Alpha_Big:
                n = Alpha_small.index(word_list[i]) - (int(Alpha_Big.index(key[i])))
                while n >= len(Alpha_small) - 1:
                    n = n - len(Alpha_small)
                while n <= -(len(Alpha_small)):
                    n = n + len(Alpha_small) - 1
                else:
                    pass
                new_word.append(Alpha_small[n])

        elif word_list[i] in Alpha_Big:
            if key[i] in Alpha_small:
                n = Alpha_Big.index(word_list[i]) - (int(Alpha_small.index(key[i])))
                while n >= len(Alpha_small) - 1:
                    n = n - len(Alpha_small)
                while n <= -(len(Alpha_small)):
                    n = n + len(Alpha_small) - 1
                else:
                    pass
                new_word.append(Alpha_Big[n])

            elif key[i] in Alpha_Big:
                n = Alpha_Big.index(word_list[i]) - (int(Alpha_Big.index(key[i])))
                while n >= len(Alpha_small) - 1:
                    n = n - len(Alpha_small)
                while n <= -(len(Alpha_small)):
                    n = n + len(Alpha_small) - 1
                else:
                    pass
                new_word.append(Alpha_Big[n])
        else:
            new_word.append(word_list[i])
    word_str = ""
    for j in range(0, len(new_word)):
        word_str = word_str + str(new_word[j])
    plaintext = word_str
    return plaintext
