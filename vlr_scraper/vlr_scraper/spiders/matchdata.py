import scrapy

### --- SCRAPER FOR ALL COMPLETED MATCH DATA --- ###

class MatchDataSpider(scrapy.Spider):
    name = "match_data"

    # urls = from match_links.json

    # --- TO-DO --- #