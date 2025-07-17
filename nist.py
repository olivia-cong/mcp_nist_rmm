from typing import Any
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

if __name__ == "__main__":
	# Initialize and run the server
	mcp.run(transport='stdio')
