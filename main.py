from biodumpy import Biodumpy
from biodumpy.inputs import PaperDown
import pandas as pd

df = pd.read_csv('Martes_martes.csv')

taxa = list(df['DOI'].dropna())

bdp = Biodumpy([
	PaperDown(bulk=True),
])
bdp.start(
	taxa,
	output_path="downloads/{date}/{module}/{name}"
)
