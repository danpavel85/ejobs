# -*- coding: utf-8 -*-
import scrapy
import dateparser


class EjobsSpider(scrapy.Spider):
    name = 'ejobs'
    allowed_domains = ['ejobs.ro']
    start_urls = ['https://www.ejobs.ro/locuri-de-munca/bucuresti/full-time/pagina1/sort-publish/']

    def parse(self, response):
        # with open('page.html', 'wb') as html_file:
        #     html_file.write(response.body)
        jobs = response.xpath("//li[@class='jobitem listview']")
        for job in jobs:
            job_date = job.xpath("(.//div[contains(@class, 'jobitem-date')]/span/text())[1]").get()
            job_date_formated = dateparser.parse(job_date)
            yield {
                'id': job.xpath(".//div[contains(@class, 'jobitem-actions')]/a/@data-id").get(),
                'jname': job.xpath(".//a[@class='title dataLayerItemLink']/text()").get(),
                'company': job.xpath(".//span[@class='company-name']/text()").get(),
                # 'location': job.xpath(".//span[@class='location-text']/text()").get(),
                'jdate': job_date_formated
            }
        
        current_page  = 1
        total_page_number = int(response.xpath("//li[@class='last']/a/@data-page").get())
        while current_page <= total_page_number:
            current_page = current_page + 1
            next_page_url = 'https://www.ejobs.ro/locuri-de-munca/bucuresti/full-time/pagina{}/sort-publish/'.format(current_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)


