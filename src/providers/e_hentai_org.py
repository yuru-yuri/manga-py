from src.provider import Provider
from src.providers.helpers import e_hentai_org
from lxml.html import HtmlElement


class EHentaiOrg(Provider):
    helper = None

    def save_file(self, idx=None, callback=None, url=None, in_arc_name=None):
        url = None
        if isinstance(url, HtmlElement):
            url = self.helper.get_image(url)
        return super().save_file(idx=idx, callback=callback, url=url, in_arc_name=in_arc_name)

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        return str(self._chapter_index())

    def get_main_content(self):
        return self.http_get(self.helper.get_url())

    def get_manga_name(self) -> str:
        url = self.re.search('/g/([^/]+/[^/?]+)', self.get_url())
        return url.group(1).replace('/', '-')

    def prepare_cookies(self):
        self.helper = e_hentai_org.EHentaiOrg(self)

    def get_chapters(self):
        parser = self.document_fromstring(self.get_storage_content())
        max_idx = self.helper.get_pages_count(parser)
        return list(range(max_idx, -1, -1))

    def get_files(self):
        url = self.helper.get_url() + '?p='
        select = '#gdt .gdtm > div > a'

        idx = self.get_current_chapter()
        if idx == 0:
            content = self.get_storage_content()
        else:
            content = self.http_get('{}{}'.format(url, idx))
        return self.document_fromstring(content, select)

    def get_cover(self) -> str:
        return self.helper.get_cover_from_content('#gd1 > div')


main = EHentaiOrg