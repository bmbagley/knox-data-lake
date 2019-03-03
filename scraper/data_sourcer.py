from requester import *
from parser import *


base_url = 'https://www.kgis.org/PropertyMapAndDetailsReport/PropertyReport2.aspx'
uri = '?parcelid='
url_id = '081KA004'
req = PageRequester(base_url, uri, url_id)
output_html = req.simple_request()
print(output_html)
parser = HtmlParser(output_html)
val_dict = parser.parser()
print(val_dict)