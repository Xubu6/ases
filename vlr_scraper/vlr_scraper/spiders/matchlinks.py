import scrapy

### --- SCRAPER FOR ALL COMPLETED MATCH LINKS ON VLR.GG --- ###

class MatchLinkSpider(scrapy.Spider):
    name = "match_links"
    base_url = "https://www.vlr.gg/matches/results"

    start_urls = [
        "https://www.vlr.gg/matches/results/?page=1"
    ]

    def parse(self, response):
        cur_page = int(response.url.split("=")[-1])
        max_page = int(response.css('div.action-container-pages').css('a.btn::text')[-1].get())

        # skip first wf-card (not match info, nav bar info)
        for card in response.css('div.wf-card')[1:]: 
            for match in card.css('div.wf-card'): 
                links = match.css('a::attr(href)').getall() 
                for link in links:
                    yield {
                        "match_link": link
                    }
                
        if cur_page < max_page:
            cur_page += 1;
            next_page = self.base_url + '/?page=' + str(cur_page);
            print('Next URL to be scraped: ' + next_page)
            yield scrapy.Request(next_page, callback=self.parse)

