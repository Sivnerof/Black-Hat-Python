import sys
import socket
import threading

# List comprehension used to store a string of all printable ASCII characters in range 0-256 or a period if it is not printable.
# len(repr(chr(i))) is used to get the length of the string representation of every character.
# repr(chr(191)) returns "'¿'", excluding the double quotes, the length is 3.
# repr(chr(30)) returns "'\\x1e'", exluding the double quotes, the length is 7 so in the code '.' is used to replace it.
HEX_FILTER = ''.join(
    [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])

def hexdump(src, length=16, show=True):
    # If a byte string was passed as src it is returned as a decoded string
    if isinstance(src, bytes):
        src = src.decode()
    results = list()
    # Increments through the data in 16 byte steps (default) or the length user chose
    for i in range(0, len(src), length):
        # Grabs 16 byte word (default) and converts it to string
        word = str(src[i:i+length])
        # The HEX_FILTER  string is used as the translation table for the translate method.
        # The result is a printable "word" where characters are represented as is and non-printable's are shown as periods.
        printable = word.translate(HEX_FILTER)
        # List comprehension is used to convert the Unicode code point for every character in word into hexadecimal.
        # ord(c) returns the Unicode code point of the character
        # :02X specifies to format this as two hexadecimal characters and apply 0's as padding if needed.
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        # Multiplied by 3 to account for the two characters plus a space.
        hexwidth = length*3
        # {i:04x} Byte index represented in hexadecimal
        # {hexa:<{hexwidth}} Hex representation of word
        # {printable} Actual word
        results.append(f'{i:04x}  {hexa:<{hexwidth}}  {printable}')
    if show:
        for line in results:
            print(line)
    else:
        return results
