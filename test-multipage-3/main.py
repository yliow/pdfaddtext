import sys, os
sys.path.append('..')
sys.path.append('../../pdfnumpages')
from pdfaddtext import *
from pdfnumpages import *


if __name__ == '__main__':    
    os.system('rm -rf outdir')
    os.system('mkdir outdir')
    pdfaddtext3(pdf='indir/main.pdf',
                dest='outdir/out-pageno-1-left')
    pdfaddtext3(pdf='indir/main.pdf', position='RIGHT',
                dest='outdir/out-pageno-1-right')
    pdfaddtext3(pdf='indir/main.pdf', position='LEFT', pageno=123,
                dest='outdir/out-pageno-123-left')
    pdfaddtext3(pdf='indir/main.pdf', position='RIGHT', pageno=456,
                dest='outdir/out-pageno-456-left')
    
