import scrapy
import apify
import csv
from scrapy_splash import SplashRequest


class MySpider(scrapy.Spider):
	name = 'apifySpider'

	def start_requests(self):
		with open("urls.csv","r") as r:
			reader = csv.reader(r)
			for line in reader:
				yield SplashRequest(line[0],callback=self.parse,dont_filter=True,args={
					'wait':'0.5',
				})


	def parse(self, response):
		external_links = list(set([i for i in response.xpath('.//a/@href').extract() if 'http' in i and response.url not in i]))

		print(external_links)
		for link in external_links:
			data = response.xpath('.//a[@href="'+str(link)+'"]').extract_first()

			sel = scrapy.Selector(text=data)
			# external_link = sel.xpath('.//a/@href').extract_first()
			image_url = sel.xpath('.//img/@src').extract_first()

			if image_url:
				output = {
					"link":link,
					"image_urk":image_url
				}

				apify.pushData(output)
