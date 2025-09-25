(TeX-add-style-hook "pdfaddtext"
 (lambda ()
    (TeX-run-style-hooks
     "pdfpages"
     "myblankpreamble")))

