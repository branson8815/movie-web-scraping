import scrapy
from movies.items import MoviesItem


class TheaterSpider(scrapy.Spider):
    name = "theater_spider"
    allowed_domains = ["www.rottentomatoes.com"]
    start_urls = ["https://www.rottentomatoes.com/browse/movies_in_theaters/"]

    def parse(self, response):
        movies = response.css(".js-tile-link")
        for movie in movies:

            title = movie.css("span.p--small::text").get()
            critics_score = movie.css(
                "score-pairs-deprecated::attr(criticsscore)"
            ).get()
            audience_score = movie.css(
                "score-pairs-deprecated::attr(audiencescore)"
            ).get()
            more_info_path = movie.css("a.js-tile-link::attr(href)").get()
            if more_info_path:
                # Construct absolute URL for the movie details page
                full_url = f"https://www.rottentomatoes.com{more_info_path}"
                yield scrapy.Request(
                    full_url,
                    callback=self.parse_additional_content,
                    meta={
                        "title": title,
                        "audience_score": audience_score,
                        "critics_score": critics_score,
                    },
                )

    def parse_additional_content(self, response):
        """
        Here is our callback function as long as there are more pages available to load
        """
        title = response.meta.get("title")
        critics_score = response.meta.get("critics_score")
        audience_score = response.meta.get("audience_score")
        genre = response.css("span.genre::text").get()
        release_date = response.css(
            "span[data-qa=movie-info-item-value] time::text"
        ).get()

        yield MoviesItem(
            title=title if title else None,
            audience_rating=audience_score if audience_score else None,
            critic_rating=critics_score if critics_score else None,
            genre=genre,
            release_date=release_date,
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
        movies = response.css(".js-tile-link")
        for movie in movies:

            title = movie.css("span.p--small::text").get()
            critics_score = movie.css(
                "score-pairs-deprecated::attr(criticsscore)"
            ).get()
            audience_score = movie.css(
                "score-pairs-deprecated::attr(audiencescore)"
            ).get()
            yield MoviesItem(
                title=title.strip() if title else None,
                audience_rating=audience_score.strip() if audience_score else None,
                critic_rating=critics_score.strip() if critics_score else None,
            )

        next_page = response.css(".btn.btn-secondary.next-page::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_additional_content)

    def parse_additional_content(self, response):
        """
        Here is our callback function as long as there are more pages available to load
        """
        movies = response.css(".js-tile-link")
        for movie in movies:

            title = movie.css("span.p--small::text").get()
            critics_score = movie.css(
                "score-pairs-deprecated::attr(criticsscore)"
            ).get()
            audience_score = movie.css(
                "score-pairs-deprecated::attr(audiencescore)"
            ).get()

            yield MoviesItem(
                title=title if title else None,
                audience_rating=audience_score if audience_score else None,
                critic_rating=critics_score if critics_score else None,
            )
