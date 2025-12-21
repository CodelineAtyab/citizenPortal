from helper_functions import fetch_data_if_not_cached


BASE_URL = "https://swapi.tech/api/people"
LATEST_URL = "https://swapi.info/api/people"

BASE_RESULT_FILE_PATH = "./data/base_result.json"
LATEST_RESULT_FILE_PATH = "./data/latest_result.json"


def execute():
  # Get results from the OLD API
  base_result: list = fetch_data_if_not_cached(url_to_fetch=BASE_URL, 
                                                result_file_path=BASE_RESULT_FILE_PATH,
                                                get_relevant_result_callback=lambda inp: inp.get("results", []))

  # Get results from the NEW API
  latest_result: list = fetch_data_if_not_cached(url_to_fetch=LATEST_URL, 
                                                  result_file_path=LATEST_RESULT_FILE_PATH,
                                                  get_relevant_result_callback=lambda inp: inp)

  print(f"Total Person Dicts in BASE: {len(base_result)}")
  print(f"Total Person Dicts in LATEST: {len(latest_result)}")
  return base_result, latest_result