import sys
sys.path.append('..')
sys.path.append('../..')
sys.path.append('../../pdfnumpages')
import pdfaddtext
pdfaddtext.pdfaddtext('blank.pdf', dest='out.pdf', s='999')
