#### Imports
from ebooklib import epub

#### Process the table of content of an eBook and return a dictionary with all chapters found
# key= href to chapter y value= title of chapter
# elements is the element EbookLib.toc from ebooklib
def parse_book_toc(elements, parent=0):
    toc={}
    for _elem in elements:
        parent = parent+1    # used later to get parent of an elem

        if isinstance(_elem, tuple):
            toc[_elem[0].href] = _elem[0].title
            subtoc= parse_book_toc(_elem[1], parent)
            toc.update(subtoc)
        elif isinstance(_elem, epub.Section):
            pass
        elif isinstance(_elem, epub.Link):
            if _elem.href not in toc:
                toc[_elem.href] = _elem.title
    return toc