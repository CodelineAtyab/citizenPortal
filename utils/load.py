import json
import traceback

RESULT_FILE_PATH = "./data/merged_result.json"

def execute(merged_result_list: list) -> None:
  """
  Load the results to a .json file.
  
  :param merged_result_list: List of dict with merged results.
  :type merged_result_list: list
  """
  try:
    with open(RESULT_FILE_PATH, "w") as result_file:
      json.dump(merged_result_list, result_file, indent=2)
  except FileNotFoundError:
    print(f"Unable to write merged result to file: {RESULT_FILE_PATH}")
  except Exception:
    print("Something went wrong!", traceback.format_exc())
