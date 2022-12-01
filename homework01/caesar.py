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
    new_word = []
    for i in range(0, len(word_list)):
        if word_list[i] in Alpha_small:
            n = Alpha_small.index(word_list[i]) + shift
            while n >= len(Alpha_small) - 1:
                n = n - len(Alpha_small)
            while n <= -(len(Alpha_small)):
                n = n + len(Alpha_small) - 1
            else:
                pass
            new_word.append(Alpha_small[n])
        elif word_list[i] in Alpha_Big:
            n = Alpha_Big.index(word_list[i]) + shift
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
    new_word = []
    for i in range(0, len(word_list)):
        if word_list[i] in Alpha_small:
            n = Alpha_small.index(word_list[i]) - shift
            while n >= len(Alpha_small) - 1:
                n = n - len(Alpha_small)

            while n <= -(len(Alpha_small)):
                n = n + len(Alpha_small) - 1
            else:
                pass
            new_word.append(Alpha_small[n])
        elif word_list[i] in Alpha_Big:
            n = Alpha_Big.index(word_list[i]) - shift
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


# done
