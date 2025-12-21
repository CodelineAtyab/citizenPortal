import os
import json
import traceback

import requests


def fetch_data_if_not_cached(url_to_fetch, result_file_path, get_relevant_result_callback):
  result: list = []
  
  try:
    if not os.path.exists(result_file_path):
      response = requests.get(url_to_fetch)
      print(f"Got the response from: {url_to_fetch}")
      
      # result = response.json().get("results", [])
      result = get_relevant_result_callback(response.json())
      # TODO: Temporary and should be removed once implementation is done.
      with open(result_file_path, "w") as result_file:
        json.dump(result, result_file, indent=2)

    else:
      print(f"Reading from the cached file: {result_file_path}")
      with open(result_file_path, "r") as result_file:
        result = json.load(result_file)
  except Exception:
    print(f"Error in fetching the request. {traceback.format_exc()}")
  
  return result