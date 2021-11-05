import scrapy
from demo1.items import Demo1Item


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    # allowed_domains = ['quotes.toscrape.com']
    # start_urls = ['http://quotes.toscrape.com/']

    def start_requests(self):  #生成初始请求
        url = ['https://quotes.toscrape.com/page/{}/'.format(i) for i in range(2,10)]
        for i in url:
            yield scrapy.Request(method='GET', url=i, callback=self.page)


    def page(self, response):
        for li in response.xpath('//div[@class="quote"]'):
            item = Demo1Item()
            item['text'] = li.xpath('./span[1]/text()').get()
            item['author'] = li.xpath('./span/small/text()').get()
            item['tags'] = li.xpath('./div/meta/@content').get()
            yield item

if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings
    process = CrawlerProcess(get_project_settings())
    process.crawl('quotes')  # start one spider
    process.start()  # the script will block here until the crawling is finished
