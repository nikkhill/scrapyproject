import scrapy
import datetime
from scrapytutorial.items import DmozItem

from scrapytutorial.items import AmzReviewItem

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            item = DmozItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('text()').extract()
            yield item

class DmozSpider2(scrapy.Spider):
    name = "dmoz2"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/",
    ]

    def parse(self, response):
        for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        for sel in response.xpath('//ul/li'):
            item = DmozItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('text()').extract()
            yield item

    # def parse_articles_follow_next_page(self, response):
       #  for article in response.xpath("//article"):
       #      item = ArticleItem()

       #      # extract article data here

       #      yield item

       #  next_page = response.css("ul.navigation > li.next-page > a::attr('href')")
       #  if next_page:
       #      url = response.urljoin(next_page[0].extract())
       #      yield Request(url, self.parse_articles_follow_next_page)

class AmzReviewSpider(scrapy.Spider):
    name = "amzs"
    allowed_domains = ["amazon.in"]
    start_urls = ["http://www.amazon.in/product-reviews/B00F84QJUI"]
    
    dtn = datetime.datetime.now()
    #datetime.datetime.strptime("7 July 2015", '%d %B %Y')

    #def parse(self, response):
        #self.parse_articles_follow_next_page(response)

    def parse(self, response):
        #datetime.datetime.now()
        # extract article data here
        for s in response.xpath("//table[@id='productReviews']/tr/td[@width='90%']/div"):
            datestring = s.xpath("./div/span/nobr/text()")[0].extract()
            dtp = datetime.datetime.strptime(datestring, '%d %B %Y')
            delta = (self.dtn-dtp).days
            if delta < 90:
                item = AmzReviewItem()
                item['date'] = datestring
                item['body'] = ''.join(s.xpath("./div[@class='reviewText']/text()").extract())
                item['author'] =  s.xpath("./div/div/div/a/span/text()")[0].extract()
                item['rating'] = s.xpath("./div/span/span/span/text()")[0].extract()
                item['title'] =  s.xpath("./div/span/b/text()")[0].extract()
                            
                yield item
            else:
                print "Review "+ datestring + " delta:" + str(delta)

        next_page = response.xpath("//span[@class='paging']/a")[-1]
        if next_page:
            if next_page.xpath("./text()")[0].extract() == u'Next \u203a':
                url = response.urljoin(next_page.xpath('./@href')[0].extract())
                print "\nNexTTTTT"
                yield scrapy.Request(url, self.parse)




