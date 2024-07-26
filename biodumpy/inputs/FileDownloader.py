from biodumpy import Input
import requests


class FileDownloader(Input):
	def __init__(self, output_format="pdf"):
		super().__init__(output_format=output_format, bulk=False)

	def download(self, query, url, **kwargs):
		try:
			return requests.get(url, timeout=20).content
		except:
			return b""
