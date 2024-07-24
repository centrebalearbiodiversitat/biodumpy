from biodumpy import Biodumpy
from biodumpy.inputs import PAPERDOWN
import pandas as pd

df = pd.read_csv('Martes_martes.csv')

taxa = list(df['DOI'].dropna())

bdp = Biodumpy([
	PAPERDOWN(bulk=True),
])
bdp.start(
	taxa,
	output_path="downloads/{date}/{module}/{name}"
)
