import scrapy
import re
from scrapy import Spider, Request
from demo1.items import BiddingItem
import datetime
from demo1.pipelines import to_date
import dateparser



class Exercise(scrapy.Spider):
    name = "exercise"

    def start_requests(self):  #详情页是json
        """初始请求"""
        headers = {
            'Content-Type': ' application/x-www-form-urlencoded'
        }
        url = 'https://hsrj-api.huashengjia100.com/goods-rest/hf/community/listUgcV2'
        bodys = []
        [bodys.append('containVideo=0&pageNo={}&pageSize=10&ugcTag=119&ugcType=3'.format(i)) for i in range(1, 11)]
        for i in bodys:
            yield scrapy.Request(method='POST', url=url, body=i,
                                 callback=self.parse, headers=headers,
                                 dont_filter=True,
                                 )


    def parse(self, response, **kwargs):
        """列表页"""
        for li in response.json()["data"]["ugcInfo"]:
            item = BiddingItem()
            item["id"] = li["ugcId"]
            item["elements"] = li["content"]
            # item["publish_time"] = to_date(li["publishTime"])
            item["publish_time"] = dateparser.parse(str(li["publishTime"]))
            item["title"] = li["productInfoArray"][0]["productTitle"]
            productId = li["productInfoArray"][0]["productId"]
            body = 'goodsId=' + productId
            item["url"] = 'https://hsrj-api.huashengjia100.com/goods-rest/goods/undertakeGoods'
            yield scrapy.Request(method='POST', url=item.get("url"),body=body,
                                 callback=self.parse_page,
                                 meta={'item': item})


    # def parse_id(self,response):
    #     """获取两个id"""
    #     projectType = re.search('projectType\:"(\w+)\"',response.text).group(1)
    #     tenderprojectid = re.search('tenderprojectid\:"(\d+)\"',response.text).group(1)
    #     page_url = 'http://125.74.85.108/f/newtenderproject/flowBidpackage'
    #     page_body = 'tenderprojectid={}&projectType={}'.format(tenderprojectid,projectType)
    #     headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',}
    #     yield scrapy.Request(method='POST', url=page_url, body=page_body, headers=headers,
    #                          callback=self.parse_page,
    #                          meta={'item': response.meta['item']})

    def parse_page(self, response):
        """page"""
        item = response.meta['item']
        # item["elements"] = response.xpath('//div[@class="sAblock"]').get()
        item["source"] = '花生日记'
        yield item


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings
    process = CrawlerProcess(get_project_settings())
    process.crawl('exercise')  # start one spider
    process.start()  # the script will block here until the crawling is finished