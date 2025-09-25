import sys, os
sys.path.append('..')
sys.path.append('../../')
sys.path.append('../../pdfnumpages')

from pdfaddtext import *


def addpagenumbers(fs, pageno, position=LOWER_LEFT):
    output = []
    for f in fs:
        #print f
        g = os.path.split(f)[-1].replace('.pdf', '')
        x = pdfaddtext(f, dest='outdir/%s' % g, s='%s' % pageno,
                       position=position)
        output.append(x)
        pageno += 1
        if position == LOWER_LEFT:
            position = LOWER_RIGHT
        else:
            position = LOWER_LEFT
    return output

os.system('rm -rf outdir; mkdir outdir')
import glob
fs = glob.glob('indir/pg*.pdf')
print fs
output = addpagenumbers(fs=fs, pageno=500, position=LOWER_LEFT)
print (output)
os.system('rm -rf tmp.aux tmp.log tmp.tex')
