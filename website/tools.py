from ebooklib import epub


#Procesa la tabla de contenidos de un eBook y devuelve diccionario con los capitulos:
# key= href to chapter y value= title of chapter
# elements es el elemento EbookLib.toc
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