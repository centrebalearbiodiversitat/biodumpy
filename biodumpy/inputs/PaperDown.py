from datetime import datetime, timedelta
from biodumpy import Input
from lxml import etree
from urllib.parse import urlparse
from selenium import webdriver


class PaperDown(Input):
	def _download(self, query, **kwargs) -> list:
		op = webdriver.ChromeOptions()
		op.add_argument("--headless")

		driver = webdriver.Chrome(options=op)
		driver.set_page_load_timeout(20)

		try:
			driver.get(f"https://doi.org/{query}")

			tic = datetime.now()
			while driver.execute_script("return document.readyState;") != "complete" and datetime.now() - tic < timedelta(seconds=30):
				pass

			dom = etree.HTML(str(driver.page_source))
			pdf_url = set([x for x in dom.xpath("//*/@href") if ".pdf" in x])
			parsed_url = urlparse(driver.current_url)
			domain = parsed_url.netloc

			# driver.quit()

			return list(map(lambda x: {"query": query, "url": f"{domain}/{x[1:]}" if x.startswith("/") else x}, list(pdf_url)))

		except:
			return [{"query": query, "url": "Error"}]
		finally:
			driver.quit()
