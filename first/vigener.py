def encrypt(plaintext='abc', keyword='bbb'):
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    abcd = {}
    ABCD = {}
    efgk = {}
    EFGK = {}
    text = []
    mykey = []

    # Создаю словарь (нижний и верхний регистр)
    firstcount = 0
    for i in range(97, 123):
        abcd[chr(i)] = firstcount
        firstcount += 1

    firstcount = 0
    for i in range(65, 91):
        ABCD[chr(i)] = firstcount
        firstcount += 1

    # Создаю второй словарь, чтобы обращаться к ключу по значению (нижний регистр)
    firstcount = 0
    for i in range(97, 123):
        efgk[firstcount] = chr(i)
        firstcount += 1
    firstcount = 26
    for i in range(97, 123):
        efgk[firstcount] = chr(i)
        firstcount += 1

    # Верхний регистр
    firstcount = 0
    for i in range(65, 91):
        EFGK[firstcount] = chr(i)
        firstcount += 1
    firstcount = 26
    for i in range(65, 91):
        EFGK[firstcount] = chr(i)
        firstcount += 1

    # Создаю списки текста и ключей
    for i in plaintext:
        text.append(i)
    while len(text) > len(mykey):
        for i in keyword.lower():
            mykey.append(abcd[i])

    # Шифрую
    i = 0
    myciphertext = []

    for j in text:
        if j.islower() == True:
            g = abcd[text[i]] + mykey[i]  # Сумма значения текста и ключа шифра
            myciphertext.append(efgk[g])
            i += 1
        elif j.isupper() == True:
            g = ABCD[text[i]] + mykey[i]  # Сумма значения текста и ключа шифра
            myciphertext.append(EFGK[g])
            i += 1
        else:
            myciphertext.append(j)

    ciphertext = ''.join(myciphertext)
    return ciphertext


def decrypt(ciphertext, keyword):
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    abcd = {}
    ABCD = {}
    efgk = {}
    EFGK = {}
    text = []
    mykey = []

    # Создаю словарь (нижний и верхний регистр)
    firstcount = 0
    for i in range(97, 123):
        abcd[chr(i)] = firstcount
        firstcount += 1

    firstcount = 0
    for i in range(65, 91):
        ABCD[chr(i)] = firstcount
        firstcount += 1

    # Создаю второй словарь, чтобы обращаться к ключу по значению (нижний регистр)
    firstcount = 0
    for i in range(97, 123):
        efgk[firstcount] = chr(i)
        firstcount += 1
    firstcount = -26
    for i in range(97, 123):
        efgk[firstcount] = chr(i)
        firstcount += 1

    # Верхний регистр
    firstcount = 0
    for i in range(65, 91):
        EFGK[firstcount] = chr(i)
        firstcount += 1
    firstcount = -26
    for i in range(65, 91):
        EFGK[firstcount] = chr(i)
        firstcount += 1

    # Создаю списки текста и ключей
    for i in ciphertext:
        text.append(i)
    while len(text) > len(mykey):
        for i in keyword.lower():
            mykey.append(abcd[i])

    # Шифрую
    i = 0
    myciphertext = []

    for j in text:
        if j.islower() == True:
            g = abcd[text[i]] - mykey[i]  # Сумма значения текста и ключа шифра
            myciphertext.append(efgk[g])
            i += 1
        elif j.isupper() == True:
            g = ABCD[text[i]] - mykey[i]  # Сумма значения текста и ключа шифра
            myciphertext.append(EFGK[g])
            i += 1
        else:
            myciphertext.append(j)

    plaintext = ''.join(myciphertext)
    return plaintext
