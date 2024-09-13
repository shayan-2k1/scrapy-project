import scrapy

class ScholarshipSpider(scrapy.Spider):
    name = 'scholarship_data'
    start_urls = ['http://www.collegescholarships.org/financial-aid/?page=1']

    def parse(self, response):
        scholarships = response.css('div.scholarship-list > div.row')

        for scholarship in scholarships:
            item = {
                'Scholarship Name': scholarship.css('h4.text-uppercase a::text').get(),
                'Deadline': scholarship.css('strong::text').get(),
                'Amount': scholarship.css('strong::text').re_first(r'\$(\d+\.?\d*)'),
                'Description': scholarship.css('p::text').get(),
                'Location': scholarship.css('i.fa-map-marker + span.trim::text').get(),
                'Years': scholarship.css('i.fa-graduation-cap + span.trim::text').get(),
                'Link': scholarship.css('h4.text-uppercase a::attr(href)').get(),
            }
            yield item

        # Follow pagination link
        next_page = response.css('ul.pagination li:last-child a::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
