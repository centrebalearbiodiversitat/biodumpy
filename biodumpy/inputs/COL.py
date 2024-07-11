from biodumpy import Input


class COL(Input):
	def download(self, query, **kwargs) -> list:
		return [{'sample_id': query}]
