from biodumpy import Biodumpy
from biodumpy.inputs import NCBI, COL

bdp = Biodumpy([
	NCBI(mail="hola_ncbi@quetal.com"),
	COL()
])
bdp.start(
	[{"name": 'Alytes muletensis', "query": "Alytes muletensis[Organism]"}],
	output_path="downloads2/{date}/{name}_{module}.json"
)
