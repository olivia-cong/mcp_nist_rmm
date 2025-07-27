from typing import Any, Optional
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("nist_rmm")

# Constants
NIST_API_BASE = "https://data.nist.gov/"

@mcp.tool()
def get_nist_rmm_taxonomy(): 
	"""
	Retrieves the NIST Resource Managment and Metadata (RMM) taxonomy data.
	The API is related to NIST science data dicsovery for public datasets,
	which allows users to explore and access data resources generated from 
	Science, Engineering, and Technology research.
	"""
	try:
		api_url = "https://data.nist.gov/rmm/taxonomy"
		response = httpx.get(api_url)
		response.raise_for_status()
		json_data = response.json()
		field_to_remove = "_id"
	
		for item in json_data:
			if field_to_remove in item:
				del item[field_to_remove]
				del item["label"]
				del item["level"]
		return {"taxonomy": json_data}
	except httpx.RequestError as exc:
		return f"An error occurred while requesting the NIST API: {exc}"
	except httpx.HTTPStatusError as exc:
		return f"Error response {exc.response.status_code} while requesting the NIST API: {exc.response.text}"

@mcp.tool()
def get_search_nist_NERDm_records(searchphrase: str):
	"""
	Searches and retrieves NIST NERDm records by search phrase.

	Args:
		searchphrase: The searchphrase used to query NIST records
		size: Number of results returned (default 100, max 1000)
		start: Starting index for pagination (default: 0)
	
	Returns:
		Filtered search results containing only @id, topic, keyword, landing page, title, and description
	"""
	try:
		api_url = "https://data.nist.gov/rmm/records"
		params = {
			"searchphrase": searchphrase,
		}
		response = httpx.get(api_url, params = params)
		response.raise_for_status()
		json_data = response.json()
		filtered_results = []
		results = json_data.get("ResultData", [])

		for item in results:
			filtered_item = {}

			if "@id" in item:
				filtered_item["@id"] = item["@id"]
			if "topic" in item:
				filtered_item["topic"] = item["topic"]
			if "keyword" in item:
				filtered_item["keyword"] = item["keyword"]
			if "landingPage" in item:
				filtered_item["landingPage"] = item["landingPage"]
			if "title" in item:
				filtered_item["title"] = item["title"]
			if "description" in item:
				filtered_item["description"] = item["description"]

			filtered_results.append(filtered_item)

		return {
			"search_phrase": searchphrase,
			"total_results": json_data.get("ResultCount", 0),
			"returned_results": len(filtered_results),
			"results": filtered_results
		}
	except httpx.RequestError as exc:
		return f"An error occurred while requesting the NIST API: {exc}"
	except httpx.HTTPStatusError as exc:
		return f"Error response {exc.response.status_code} while requesting the NIST API: {exc.response.text}"

@mcp.tool()
def get_nist_rmm_fields():
	"""
	Retrieves the data dictionary for the NIST RMM API.
	This endpoint provides a machine-readable description of all available
	data fields within the NIST Resource Metadata Management (RMM) system,
	detailing all searchable and retrievable fields in the underlying
	NERDm (NIST Enterprise Research Data model) schema.
	"""
	try:
		api_url = "https://data.nist.gov/rmm/records/fields"
		response = httpx.get(api_url)
		response.raise_for_status()
		json_data = response.json()
		return {"fields": json_data}
	except httpx.RequestError as exc:
		return f"An error occurred while requesting the NIST API: {exc}"
	except httpx.HTTPStatusError as exc:
		return f"Error response {exc.response.status_code} while requesting the NIST API: {exc.response.text}"
	
if __name__ == "__main__":
	# Initialize and run the server
	mcp.run(transport='stdio')
