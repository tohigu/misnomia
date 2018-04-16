#!/usr/bin/env python2

words = ['file','reset','configuration','request','load','registry','target','override','execution']
dialogs = ['target.override.error','start.join.execution','end.delete.protocol']

# Main program logic follows:
if __name__ == '__main__':
    for word in words:
        f= open('vocab/en-us/'+word+'.voc',"w+")
        f.write(word)
        f.close()
    for dialog in dialogs:
        f= open('dialog/en-us/'+dialog+'.dialog',"w+")
        f.write(str.replace(dialog,"."," "))
        f.close()
