import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    allowed_domains = ["www.imdb.com"]
    start_urls = ['https://www.imdb.com/title/tt0386676/']

    def parse(self, response):
        credit_url = response.url + "fullcredits/"
        yield scrapy.Request(credit_url, callback = self.parse_full_credits)

    def parse_full_credits(self, response):
        url_boxes = response.css("td.primary_photo + td").css("a")
        actor_urls = ["https://www.imdb.com" + url_box.attrib["href"] for url_box in url_boxes]

        for actor_url in actor_urls: 
            yield scrapy.Request(actor_url, callback = self.parse_actor_page)

    def parse_actor_page(self, response):
        actor_name = response.css("span.itemprop::text")[0].get()
        movie_box = response.css("div.filmo-category-section")[0]
        movie_or_TV_name = movie_box.css("b a::text").getall()
        
        yield {
            "actor" : actor_name, 
            "movie_or_TV_name" : movie_or_TV_name
        }

