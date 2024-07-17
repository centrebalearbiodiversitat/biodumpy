from biodumpy import Biodumpy
from biodumpy.inputs import NCBI, INaturalist, BOLD

bdp = Biodumpy([
	NCBI(mail="hola_ncbi@quetal.com"),
	BOLD(),
	INaturalist(bulk=True)
])
bdp.start(
	[
		{"name": 'Mus musculus', "query": "Mus musculus[Organism]"}
	],
	output_path="downloads2/{date}/{module}/{name}.json"
)
