from biodumpy import Input
import requests


class FileDownloader(Input):
	def __init__(self, output_format="pdf"):
		super().__init__(output_format="pdf", bulk=False)

	def download(self, query, **kwargs):
		return requests.get(query).content
