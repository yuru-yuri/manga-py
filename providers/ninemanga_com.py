#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from urllib.parse import urlparse

domainUri = 'http://ninemanga.com'


def get_main_content(url, get=None, post=None):
    return get(url)


def get_volumes(content: str, url=None):
    parser = document_fromstring(content)
    result = parser.cssselect('.chapterbox li a.chapter_list_a')
    if result is None:
        return []
    items = []
    url = urlparse(url)
    url = '{}://{}'.format(url.scheme, url.netloc)
    for i in result:
        u = re.search('(/chapter/.*/\d+)\.html', i.get('href'))
        if u is not None:
            img = u.groups()
            # lifehack
            items.append('{}{}-150-1.html'.format(url, img[0]))
    return items


def get_archive_name(volume, index: int = None):
    return 'vol_{}'.format(index)


def get_images(main_content=None, volume=None, get=None, post=None):
    # fucking guards :[
    content = get(volume, headers={'Referer': volume})
    parser = document_fromstring(content)
    result = parser.cssselect('em a.pic_download')
    if result is None:
        return []
    return [i.get('href') for i in result]


def get_manga_name(url, get=None):
    result = re.match('\.com/manga/(.+)\.html', url)
    if result is None:
        return ''
    result = result.groups()
    if not len(result):
        return ''
    return result[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')