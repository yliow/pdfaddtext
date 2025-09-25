import sys, os
sys.path.append('..')
sys.path.append('../../pdfnumpages')
from pdfaddtext import *
from pdfnumpages import *


if __name__ == '__main__':

    os.system('rm -rf outdir')
    os.system('mkdir outdir')
    infilename = 'indir/main.pdf'
    outfilename = 'outdir/main.pdf'
    
    texts = {}
    position_is_left = True
    numpages = pdfnumpages(infilename)
    for i in range(1, numpages + 1):
        if position_is_left:
            texts[i] = (MULTIPAGE['LOWER_LEFT'], r'{{LL-%s-LL}}' % str(i))
        else:
            texts[i] = (MULTIPAGE['LOWER_RIGHT'], r'{{RR-%s-RR}}' % str(i))    
        position_is_left = not position_is_left
    
    pdfaddtext2(pdf=infilename,
                texts=texts,
                dest=outfilename.replace('.pdf', ''),
    )
