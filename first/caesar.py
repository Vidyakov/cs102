def encrypt_caesar(plaintext):
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    myciphertext = []
    for i in plaintext:
        if 97 <= ord(i) <= 119 or 65 <= ord(i) <= 87:
            myciphertext.append(chr(ord(i) + 3))
        elif 120 <= ord(i) <= 123 or 88 <= ord(i) <= 91:
            myciphertext.append(chr(ord(i) - 23))
        else:
            myciphertext.append(i)
    ciphertext = ''.join(myciphertext)
    return ciphertext


def decrypt_caesar(ciphertext):
    """
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    myplaintext = []
    for i in ciphertext:
        if 100 <= ord(i) <= 123 or 68 <= ord(i) <= 91:
            myplaintext.append(chr(ord(i) - 3))
        elif 97 <= ord(i) <= 99 or 65 <= ord(i) <= 67:
            myplaintext.append(chr(ord(i) + 23))
        else:
            myplaintext.append(i)

    plaintext = ''.join(myplaintext)
    return plaintext
