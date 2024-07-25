from typing import Union, Dict, Any, Optional

from biodumpy import Input
import requests


class INaturalist(Input):
	TAXA_URL = "https://api.inaturalist.org/v1/taxa"

	def download(self, query, **kwargs):
		params = {"q": query, "order": "desc", "order_by": "observations_count"}
		response = requests.get(INaturalist.TAXA_URL, params=params)

		photo_details_empty = {"taxon": query, "image_id": None, "license_code": None, "attribution": None}

		photo_license = ["cc0", "cc-by", "cc-by-nc", "cc-by-nc-nd", "cc-by-sa", "cc-by-nd", "cc-by-nc-sa"]

		if response.status_code == 200:
			results = response.json()["results"]
			results_filtered = next(filter(lambda x: x["name"] == query, results), None)

			if results_filtered:
				taxon_id = results_filtered["id"]

				if results_filtered["default_photo"] is not None:
					photo_info = results_filtered["default_photo"] if results_filtered["default_photo"]["license_code"] else None
				else:
					photo_info = None

				if photo_info is None:
					response_id = requests.get(f"{INaturalist.TAXA_URL}/{taxon_id}")

					if response_id.status_code == 200:
						results_id = response_id.json()["results"]
						photo_id = results_id[0]["taxon_photos"]

						photo_details = next(filter(lambda x: x["photo"]["license_code"] in photo_license, photo_id), None)

						if photo_details:
							url_photo = photo_details["photo"]["url"]
							url_photo = url_photo.split("/")[-2] + "/" + url_photo.split("/")[-1]
							photo_details = {
								"taxon": query,
								"image_id": url_photo.replace("square", "medium"),
								"license_code": photo_details["photo"]["license_code"],
								"attribution": photo_details["photo"]["attribution"],
							}
						else:
							photo_details = photo_details_empty

					else:
						photo_details = photo_details_empty
				else:
					url_photo = photo_info["url"]
					url_photo = url_photo.split("/")[-2] + "/" + url_photo.split("/")[-1]
					photo_details = {
						"taxon": query,
						"image_id": url_photo.replace("square", "medium"),
						"license_code": photo_info["license_code"],
						"attribution": photo_info["attribution"],
					}

			else:
				photo_details = photo_details_empty

		else:
			photo_details = photo_details_empty

		return [photo_details]
