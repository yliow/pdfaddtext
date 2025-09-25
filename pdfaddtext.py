"""
Takes a pdf file and add text to it on every page at the given position

https://tex.stackexchange.com/questions/105589/insert-pdf-file-in-latex-document

For pdfaddtext2 and pdfaddtext3, pdfnumpages is needed.


TODO:
most general
pdfaddtext(
    outfilename,
    texts -- list of (pdf, pageno, position, text)    
)
"""

import os
import sys
sys.path.append('../pdfnumpages')
from pdfnumpages import pdfnumpages
from latextool_basic import *

# Value for position parameter:
# Note that (0,0) is lower left corner.
# For page number on lower right, use '20.5, 1'

LOWER_LEFT = '5,1' # ?

UPPER_LEFT = '5.5,27' # ?
UPPER_RIGHT = '15,27' # ?

#LOWER_LEFT = '1.1,1'    # position on pdf page for lower left page number
LOWER_RIGHT = '20.5,1'  # position on pdf page for lower right page number

# Why are the positions different for pdfaddtext2?????
MULTIPAGE = {}
MULTIPAGE['LOWER_LEFT'] = '-4, -22.5'
MULTIPAGE['LOWER_RIGHT'] = '15, -22.5'


def tikz_text(position, s):
    return r'''\begin{tikzpicture}[overlay,remember picture,shift={(current page.south west)}]
\node at (%(position)s) {%(s)s};
\end{tikzpicture}
    ''' % {'position':position, 's':s}

def tikz_rect(position, s, width='2cm', height='0.5cm', fill='white'):
    return r'''
    \node (rect) at (%(position)s) [draw,thick,minimum width=2cm,minimum height=2cm, fill=%(fill)s] {%(s)s};
''' % {'position':position, 's':s, 'fill':fill}

def pdfaddtextnew(dest=None, # example: "out". Will give "out.tex" and "out.pdf"
                  texts=None):
    # texts -- list of (pdf filename, pageno, position, text)    
    body = ''
    for (pdf, pageno, position, s) in texts:
        tikz = tikz_text(position, s)
        page = r'\includepdf[pages=%(pages)s,fitpaper=true,pagecommand={%(tikz)s}]{%(pdf)s}' % \
               {'pages':pageno, 'position':position, 's':s, 'pdf':pdf, 'tikz':tikz}
        body += page + '\n'

    latex = r'''
\documentclass{article}
\pagestyle{empty}
\usepackage{tikz}
\usepackage{pdfpages}
\begin{document}

%s

\end{document}
''' % body
        
    open('tmp.tex', 'w').write(latex)
    os.system('pdflatex tmp.tex >/dev/null')
    os.system('pdflatex tmp.tex >/dev/null')
    os.system('mv "tmp.pdf" "%s.pdf"' % dest)
    print("see %s.pdf" % dest)
    return "%s.pdf" % dest



def pdfaddtext(pdf='',    # pdf filename
               s='',      # Text to add to pdf
               dest=None, # example: "out". Will give "out.tex" and "out.pdf"
               position=None, 
               lower_left=False,
               lower_right=True,
               pages='-',
               clean=True):

    if not position:
        if lower_left:
            position = LOWER_LEFT
        elif lower_right:
            position = LOWER_RIGHT

    if not pdf.endswith('.pdf'):
        raise ValueError("ERROR: %s does not end with .pdf" % pdf)
    if not os.path.exists(pdf):
        raise ValueError("ERROR: %s not found" % pdf)

    if dest == None:
        dest = pdf.replace('.pdf', '')
    if dest.endswith('.pdf'):
        print("WARNING:", dest, "ends with .pdf")

    latex = r'''
\documentclass{article}
\pagestyle{empty}
\usepackage{tikz}
\usepackage{pdfpages}
\begin{document}

\newcommand\superposition[1]{
  \begin{tikzpicture}[overlay,remember picture,
    shift={(current page.south west)}]
    \node at (%(position)s) {%(s)s};
  \end{tikzpicture}
}

\includepdf[pages=%(pages)s,fitpaper=true,pagecommand={\superposition}]{%(pdf)s}

\end{document}
''' % {'pages':pages, 'position':position, 's':s, 'pdf':pdf}




    t = r'\includepdf[pages=%(pages)s,fitpaper=true,pagecommand={\superposition}]{%(pdf)s}'

    
    open('tmp.tex', 'w').write(latex)
    os.system('pdflatex tmp.tex >/dev/null')
    os.system('pdflatex tmp.tex >/dev/null')
    os.system('mv "tmp.pdf" "%s.pdf"' % dest)
    print("see %s.pdf" % dest)
    #if clean:
    #    os.system('rm %s.tex' % dest)
    #os.system('rm -f *.log *.aux *.out *.idx tmp.tex')
    return "%s.pdf" % dest


def pdfaddtext2(pdf='',    # pdf filename
                texts={}, # Text to add to pdf
                dest=None, # example: "out". Will give "out.tex" and "out.pdf"
                ):
    """
    This version is for multipages

    texts is a dictionary of pageno -> (position, latex string)

    This version need total number of pages
    """

    numpages = pdfnumpages(pdf)
    
    if not pdf.endswith('.pdf'):
        raise ValueError("ERROR: %s does not end with .pdf" % pdf)
    if not os.path.exists(pdf):
        raise ValueError("ERROR: %s not found" % pdf)

    if dest == None:
        dest = pdf.replace('.pdf', '')
    if dest.endswith('.pdf'):
        print("WARNING:", dest, "ends with .pdf")

    latex = r'''
\documentclass{article}
\pagestyle{empty}
\usepackage{tikz}
\usepackage{pdfpages}
\begin{document}

\newcommand\superposition[1]{}
    
%s
    
\end{document}
''' 

    body = ''
    d = {}
    d['pdf'] = pdf
    for pageno in range(1, numpages + 1):
        d['pageno'] = pageno
        if pageno in texts.keys():
            position,text = texts[pageno]
            d['position'] = position
            d['text'] = text
            s = r'''
            \renewcommand\superposition[1]{
            \begin{tikzpicture}[overlay,remember picture,
            shift={(current page.south west)}]
            \node at (%(position)s) {%(text)s};
            \end{tikzpicture}
            }
            \includepdf[pages=%(pageno)s,
                        fitpaper=true,
            pagecommand={\superposition}]{%(pdf)s}''' % d
        else:
            s = r'''
            \includepdf[pages=%(pageno)s,
                        fitpaper=true,
            pagecommand={}]{%(pdf)s}''' % d
        body += s

    latex = latex % body
    #print latex
    f = open('tmp.tex', 'w')
    f.write(latex)
    f.close()
    
    os.system('pdflatex tmp.tex 1>/dev/null')
    os.system('mv "tmp.pdf" "%s.pdf"' % dest)
    #if clean:
    #    os.system('rm %s.tex' % dest)
    os.system('rm -f *.log *.aux *.out *.idx tmp.tex')
    return "%s.pdf" % dest


def pdfaddtext3(pdf='',    # pdf filename
                pageno=1,
                position='LEFT', # 'LEFT' or 'RIGHT'. Placement of 1st pageno.
                dest=None, # example: "out". Will give "out.tex" and "out.pdf"
                ):
    texts = {}
    if position == 'LEFT':
        position_is_left = True
    else:
        position_is_left = False
    numpages = pdfnumpages(pdf)
    for i in range(1, numpages + 1):
        if position_is_left:
            texts[i] = (MULTIPAGE['LOWER_LEFT'], r'%s' % str(pageno + i - 1))
        else:
            texts[i] = (MULTIPAGE['LOWER_RIGHT'], r'%s' % str(pageno + i - 1))    
        position_is_left = not position_is_left
        
    return pdfaddtext2(pdf=pdf,
                       texts=texts,
                       dest=dest,
    )


if __name__ == '__main__':
    #pdfaddtext('blank.pdf', dest='main2', s='FOO-BAR')
    #pdfaddtext('rach-16-04.pdf', dest='out', position=UPPER_LEFT, s='Rachmaninov Moment Musicaux Op. 16 No. 4')

    pdfaddtextnew(dest='out1', # example: "out". Will give "out.tex" and "out.pdf"
                  texts=[
                      ('rach-16-04.pdf', '1', UPPER_LEFT,  'Rachmaninov Moment Musicaux Op.~16 No.~4 (page 1 of 7)'),
                      ('rach-16-04.pdf', '2', UPPER_RIGHT, 'Rachmaninov Moment Musicaux Op.~16 No.~4 (page 2 of 7)'),
                      ('rach-16-04.pdf', '3', UPPER_LEFT,  'Rachmaninov Moment Musicaux Op.~16 No.~4 (page 3 of 7)'),
                      ('rach-16-04.pdf', '4', UPPER_RIGHT, 'Rachmaninov Moment Musicaux Op.~16 No.~4 (page 4 of 7)'),
                      ('rach-16-04.pdf', '5', UPPER_LEFT,  'Rachmaninov Moment Musicaux Op.~16 No.~4 (page 5 of 7)'),
                      ('rach-16-04.pdf', '6', UPPER_RIGHT, 'Rachmaninov Moment Musicaux Op.~16 No.~4 (page 6 of 7)'),
                      ('rach-16-04.pdf', '7', UPPER_LEFT,  'Rachmaninov Moment Musicaux Op.~16 No.~4 (page 7 of 7)'),
                  ])
