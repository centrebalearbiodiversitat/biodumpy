import requests

from biodumpy import Input, BiodumpyException
from biodumpy.utils import rm_dup


class IUCN(Input):
	"""
	Query the IUCN Red List API for information about species.

	Notes
	-----
	This class currently operates only at the species level. It automatically splits genus and species names from the input internally.

	Parameters
	----------
	query : list
		The list of taxa (species names) to query.
	authorization : str
		Your IUCN API key used for authentication.
	assess_details : bool, optional
		If True, downloads detailed assessments for each species, including threats, habitats, conservation actions, and more. Defaults to False.
	latest : bool, optional
		If True, retrieves only the latest assessment for each species. Defaults to False.
	scope : list, optional
		List of IUCN assessment scopes to filter the results (e.g., ['Global', 'Europe']).
		Defaults to ['Global'].

	Examples
	--------
	>>> from biodumpy import Biodumpy
	>>> from biodumpy.inputs import IUCN
	>>> api_key = 'YOUR_API_KEY'  # Insert your API key
	>>> taxa = ['Alytes muletensis', 'Bufotes viridis', 'Hyla meridionalis']  # Taxa list
	>>> regions = ['Global', 'Europe']  # Select the regions
	>>> bdp = Biodumpy([IUCN(authorization=api_key, bulk=True, scope=regions)])
	>>> bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}')
	"""

	def __init__(self, authorization: str = None, assess_details: bool = False, latest: bool = False, scope: list = None, **kwargs):
		super().__init__(**kwargs)
		self.authorization = authorization
		self.assess_details = assess_details
		self.latest = latest
		if scope is None:
			self.scope = ["Global"]
		else:
			self.scope = scope

		iucn_scope = [
			"Global",
			"Europe",
			"Mediterranean",
			"Western Africa",
			"S. Africa FW",
			"Pan-Africa",
			"Central Africa",
			"Northeastern Africa",
			"Eastern Africa",
			"Northern Africa",
			"Gulf of Mexico",
			"Caribbean",
			"Persian Gulf",
			"Arabian Sea",
		]

		if self.output_format != "json":
			raise ValueError("Invalid output_format. Expected 'json'.")

		for scope in self.scope:
			if scope not in iucn_scope:
				raise ValueError(f"Choose an IUCN scope from the following options: {iucn_scope}.")

	def _download(self, query, **kwargs) -> list:
		payload = []

		# Start the function
		taxon = query.split()
		genus = taxon[0]
		species = taxon[1]
		infra_name = None
		subpopulation_name = None

		if len(taxon) > 2:
			while True:
				infra_check = input(f"Is the taxon '{taxon}' a subspecies? Enter 1 (yes) or 0 (no): ")
				if infra_check in ("1", "0"):
					if infra_check == "1":
						infra_name = taxon[2]
					else:
						subpopulation_name = taxon[2]
					break
				print("Please enter only 1 or 0.")

		# General query to obtain the taxon ID
		taxon_info = None
		if infra_name is None and subpopulation_name is None:
			taxon_info = self._icun_request(query_path=f"https://api.iucnredlist.org/api/v4/taxa/scientific_name?genus_name={genus}&species_name={species}")
		if infra_name:
			taxon_info = self._icun_request(query_path=f"https://api.iucnredlist.org/api/v4/taxa/scientific_name?genus_name={genus}&species_name={species}&infra_name={infra_name}")
		elif subpopulation_name:
			taxon_info = self._icun_request(
				query_path=f"https://api.iucnredlist.org/api/v4/taxa/scientific_name?genus_name={genus}&species_name={species}&subpopulation_name={subpopulation_name}"
			)

		# Create filters
		taxon_assessment = taxon_info.get("assessments")

		# Latest: Extract the records with the newest assessment
		if self.latest:
			taxon_assessment[:] = [item for item in taxon_assessment if item.get("latest")]

		# Filter the regions included in the region parameter
		if self.scope:
			# Create a scope-string key with all the scopes, avoiding the dictionary
			for item in taxon_assessment:
				item["scope"] = ";".join([s["description"]["en"] for s in item.get("scopes", [])])

			taxon_assessment[:] = [
				item
				for item in taxon_assessment
				# if any(r in item['scope'] for r in self.scope)
				if any(r == s for s in item["scope"].split(";") for r in self.scope)
			]

		# Remove duplicates
		taxon_assessment = rm_dup(taxon_assessment)

		if self.assess_details:
			assessment_list = []
			for item in taxon_assessment:
				assessment_id = item.get("assessment_id")
				# print(f'Downloading {assessment_id}...')
				assess = self._icun_request(query_path=f"https://api.iucnredlist.org/api/v4/assessment/{assessment_id}")
				assess.pop("taxon", None)  # Drop the taxon key
				assessment_list.append(assess)

			payload.append({"taxon": taxon_info.get("taxon"), "assessment": assessment_list})
		else:
			payload.append({"taxon": taxon_info.get("taxon"), "assessment": taxon_assessment})

		return payload

	def _icun_request(self, query_path):
		response = requests.get(query_path, headers={"Authorization": self.authorization})

		if response.status_code != 200:
			raise BiodumpyException(f"Error {response.status_code}")

		if response.content:
			response = response.json()

			# if len(response) > 0:
			# 	return response

			if response:
				return response
			else:
				raise BiodumpyException("Empty response from IUCN API.")
