
import os
import binascii

def replicate(path):
    #
    # Replicate a file given the path of the current file.  Opens current file
    # and new file and reads all lines into new file.
    #
    with open(get_new_filename(path), "w") as newfile, open(path) as program:
        for line in program:
            newfile.write(line)


def get_new_filename(old_name):
    #
    # Gets a new filename given a filename to work off of.  Splits the old name
    # by periods, then adds a random hex string right before the filetype
    # ending.  Given 'files.py', a valid output would be 'files-2b57f5.py'.
    #
    # The function also checks for collisions and adds another random string to
    # the end if necessary.
    #
    # http://stackoverflow.com/a/2782293
    #
    broken_name = old_name.split('.')
    while True:
        ending = '-' + str(binascii.b2a_hex(os.urandom(3))).replace('\'', '')
        broken_name[-2] = broken_name[-2] + ending
        name = '.'.join(broken_name)
        if not os.path.exists(name):
            break
    return name


if __name__ == '__main__':
    replicate(__file__)

# sed
import tempfile
import shutil
import os

newfile = tempfile.mkstemp()
oldfile = 'stack.txt'

f = open(oldfile)
n = open(newfile,'w')

for i in f:
        if i.find('Banana') == -1:
                n.write(i)
                continue

        # Last row
        if i.find('\n') == -1:
                i += 'ToothPaste'
        else:
                i = i.rstrip('\n')
                i += 'ToothPaste\n'

        n.write(i) 

f.close()
n.close()

os.remove(oldfile)
shutil.move(newfile,oldfile)