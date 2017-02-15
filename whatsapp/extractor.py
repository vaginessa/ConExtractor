# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup


def concatenate(contact):
    contact = contact.split()
    return "".join(contact)


def main(html):
    contact_list = []
    soup = BeautifulSoup(html, "lxml")
    for i in soup.find_all('span'):
        if i.get('class') == ['emojitext', 'ellipsify'] and i.get("title") is not None:
            contact_list.append(concatenate(i.get_text()))
    return contact_list

