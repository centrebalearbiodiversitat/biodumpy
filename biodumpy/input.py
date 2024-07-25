class Input:
	def __init__(self, output_format="json", bulk=False):
		super().__init__()
		self.output_format = output_format
		self.bulk = bulk

	def download(self, **kwargs) -> list:
		raise NotImplementedError()
