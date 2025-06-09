import requests
from biodumpy.input import Input

class BALEARICA(Input):
    """
    BALEARICA module for retrieving taxonomic, occurrence, and genetic information
    from the balearica API.

    Parameters
    ----------
    bulk : bool, optional
        If True, enables batch processing and delays file writing until all results are collected.
    taxonomy : bool, optional
        If True, enables taxonomic information download.
    occurrences : bool, optional
        If True, include occurrence records for the queried taxon.
    genetics : bool, optional
        If True, include genetic sequence data for the queried taxon.
    """

    def __init__(
        self,
        bulk: bool = True,
        taxonomy: bool = False,
        occurrences: bool = False,
        genetics: bool = False
    ):
        super().__init__(sleep=0.5, output_format="json", bulk=bulk)
        self.occurrences = occurrences
        self.genetics = genetics
        self.taxonomy = taxonomy

    def _download(self, query, **kwargs) -> list:
        url = f"https://balearica.uib.es/api/v1/taxonomy/search?name={query}&exact=true"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if not data:
                return [{"query": query, "result": None}]

            entry = data[0]

            taxon_id = entry.get("id")
            name = entry.get("name")

            result = {
                "id": taxon_id,
                "name": name,
                "taxonRank": entry.get("taxonRank"),
                "authorship": entry.get("scientificNameAuthorship"),
                "accepted": entry.get("accepted"),
                "acceptedModifier": entry.get("acceptedModifier")
            }

            if self.taxonomy:
                result["taxonomy"] = self._get_taxonomy(name)

            if self.occurrences:
                result["occurrences"] = self._get_occurrences(taxon_id)

            if self.genetics:
                result["genetics"] = self._get_genetics(taxon_id)

            return [result]

        except Exception as e:
            return [{"query": query, "error": str(e)}]

    def _get_taxonomy(self, name):

        url = f'https://balearica.uib.es/api/v1/taxonomy/list?name={name}&exact=true'

        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return [{"error": str(e)}]

    def _get_occurrences(self, taxon_id: int) -> list:

        url = f"https://balearica.uib.es/api/v1/occurrences/list?taxonomy={taxon_id}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return [{"error": str(e)}]

    def _get_genetics(self, taxon_id: int) -> list:

        url = f"https://balearica.uib.es/api/v1/genetics/sequence/list?taxonomy={taxon_id}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            result = response.json()
            return result.get("data", [])
        except Exception as e:
            return [{"error": str(e)}]
