import hashlib

def rot47(s):
    x = []
    for i in range(len(s)):
        j = ord(s[i])
        if j >= 33 and j <= 126:
            x.append(chr(33 + ((j - 33 + 47) % 94)))
        else:
            x.append(s[i])
    return "".join(x)

secret = "A:4@r%uL5b3F88bC05C`Gb0hf4bfg2N"
print(rot47(secret))