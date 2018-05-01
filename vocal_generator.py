#!/usr/bin/env python2

words = ['reset']
dialogs = []

# Main program logic follows:
if __name__ == '__main__':
    for word in words:
        f = open('vocab/en-us/'+word+'.voc', "w+")
        f.write(word)
        f.close()
    for dialog in dialogs:
        f = open('dialog/en-us/'+dialog+'.dialog', "w+")
        f.write(str.replace(dialog, ".", " "))
        f.close()
