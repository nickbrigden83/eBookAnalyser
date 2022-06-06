import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

BLACKLIST = ['[document]', 'noscript', 'header', 'html', 'meta', 'head',
             'input', 'script']


def get_author(book: epub.EpubBook):
    """ returns the author details. If not found, returns empty list"""
    dc_author = book.get_metadata('DC', 'creator')
    if dc_author:
        return dc_author[0][0]
    else:
        return []


def get_title(book: epub.EpubBook):
    dc_title = book.get_metadata('DC', 'title')
    if dc_title:
        return dc_title[0][0]
    else:
        return []


def get_content(book: epub.EpubBook):
    raw_chapters = get_chapters(book)
    chapters = _clean_chapters(raw_chapters)
    return chapters


def get_chapters(book):
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters


def _clean_chapters(content):
    output = []
    for html in content:
        text = _clean_html(html)
        output.append(text)
    return output


def _clean_html(chapter):
    output = ''
    soup = BeautifulSoup(chapter, 'html.parser')
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in BLACKLIST:
            output += '{} '.format(t)
    return output
