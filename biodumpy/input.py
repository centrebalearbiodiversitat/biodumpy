
class Input:
	def __init__(self, bulk=False):
		super().__init__()
		self.bulk = bulk

	def download(self, **kwargs) -> list:
		raise NotImplementedError()
