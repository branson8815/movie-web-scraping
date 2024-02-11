import scrapy
from movies.items import MoviesItem


class TheaterSpider(scrapy.Spider):
    name = "theater_spider"
    allowed_domains = ["www.rottentomatoes.com"]
    start_urls = ["https://www.rottentomatoes.com/browse/movies_in_theaters/"]

    def parse(self, response):
        movies = response.css("tile-dynamic")
        for movie in movies:

            title = movie.css("span.p--small::text").get()
            critics_score = movie.css("::attr(criticsscore)").get()
            audience_score = movie.css("::attr(criticsscore)").get()

            yield MoviesItem(
                title=title.strip() if title else None,
                audience_rating=audience_score.strip() if title else None,
                critic_rating=critics_score.strip() if title else None,
            )

            # load_more = response.css(
            #     "button[data-qa='dlp-load-more-button']::text"
            # ).get()

            # if load_more != None:
            #     response.url += "?page=2"
            #     self.parse()


class HomeMovieSpider(scrapy.Spider):
    name = "home_movie_spider"
    allowed_domains = ["www.rottentomatoes.com"]
    start_urls = ["https://www.rottentomatoes.com/browse/movies_at_home/"]

    def parse(self, response):
        movies = response.css("tile-dynamic")
        for movie in movies:

            title = movie.css("span.p--small::text").get()
            critics_score = movie.css("::attr(criticsscore)").get()
            audience_score = movie.css("::attr(criticsscore)").get()

            yield MoviesItem(
                title=title.strip() if title else None,
                audience_rating=audience_score.strip() if audience_score else None,
                critic_rating=critics_score.strip() if critics_score else None,
            )

        page_number = 2  # Assuming the initial page is 1
        load_more_url = (
            f"https://www.rottentomatoes.com/browse/movies_at_home?page={page_number}"
        )
        yield scrapy.Request(load_more_url, callback=self.parse_additional_content)

    def parse_additional_content(self, response):
        # Parse additional movie items loaded after clicking "Load more"
        movies = response.css("tile-dynamic")
        for movie in movies:

            title = movie.css("span.p--small::text").get()
            critics_score = movie.css("::attr(criticsscore)").get()
            audience_score = movie.css("::attr(criticsscore)").get()

            yield MoviesItem(
                title=title.strip() if title else None,
                audience_rating=audience_score.strip() if audience_score else None,
                critic_rating=critics_score.strip() if critics_score else None,
            )
