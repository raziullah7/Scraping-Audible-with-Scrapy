import scrapy


class AudibleSpider(scrapy.Spider):
    name = "audible"
    allowed_domains = ["www.audible.com"]
    # start_urls = ["https://www.audible.com/search"]
    
    def start_requests(self):
        yield scrapy.Request(url='https://www.audible.com/search', callback=self.parse, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})

    def parse(self, response):
        product_container = response.xpath("//div[@class='adbl-impression-container ']/div/span/ul/li")
        
        for product in product_container:
            book_author = product.xpath(".//li[contains(@class, 'authorLabel')]/span/a/text()").getall()
            book_length = product.xpath(".//li[contains(@class, 'runtimeLabel')]/span/text()").get()
            book_title = product.xpath(".//h3[contains(@class, 'bc-heading')]/a/text()").get()
            
            yield {
                'title': book_title,
                'author(s)': book_author,
                'length': book_length,
                'User-Agent': response.request.headers['User-Agent'],
            }

        pagination = response.xpath("//ul[contains(@class, 'pagingElements')]/li")
        next_page_url = pagination.xpath(".//span[contains(@class, 'nextButton')]/a/@href").get()
        
        if next_page_url:
            yield response.follow(url=next_page_url, callback=self.parse, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
