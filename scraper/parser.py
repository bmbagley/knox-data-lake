from bs4 import BeautifulSoup


class HtmlParser(object):
    """"""

    def __init__(self, page):
        self.page = page
        self.input_dict = {'parcel_id': 'pnlPropertyInfo'}
        self.data_dict = {}

    def parser(self):
        soup = BeautifulSoup(self.page, 'html.parser')
        print(soup.find('div', attrs={'id': 'pnlPropertyInfo'}))
        for k, v in self.input_dict.items():
            print(soup.find('td', text=v).find_next_sibling('td').text)
            self.data_dict[k] = soup.find('td', attrs={'id': v})
            soup.find('div', attrs={'id': 'pnlPropertyInfo'})
        return self.data_dict


