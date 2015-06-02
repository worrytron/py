import hashlib
from Tkinter import Tk

def copyHashToClipboard():
    h = hashlib.sha256()
    hash_str = raw_input('String to be hashed: ')

    c = Tk()
    c.withdraw()
    c.clipboard_clear()

    h.update(hash_str)
    h.digest()

    c.clipboard_append(h.hexdigest())

    print "Copied hash (( " + repr(h.hexdigest()) + " )) to clipboard."

if __name__ == '__main__':
    copyHashToClipboard()