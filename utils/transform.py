from typing import List, Dict, Any

def execute(base_result, latest_result) -> List[Dict[str, Any]]:
  """
  The transformation phase, cleans and merges the data based on a standard schema.
  This function is going to return a result object based on the following JSON schema:

  {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Star Wars Characters List",
    "description": "Schema for a list of Star Wars characters from SWAPI",
    "type": "array",
    "items": {
      "type": "object",
      "required": [
        "name",
        "height",
        "mass",
        "hair_color",
        "skin_color",
        "eye_color",
        "birth_year",
        "gender",
        "homeworld",
        "created",
        "edited",
        "url"
      ],
      "properties": {
        "name":  {
          "type": "string",
          "description": "The name of the character"
        },
        "height": {
          "type": "string",
          "description": "The height of the character in centimeters"
        },
        "mass": {
          "type": "string",
          "description": "The mass of the character in kilograms"
        },
        "hair_color": {
          "type": "string",
          "description": "The hair color of the character"
        },
        "skin_color": {
          "type": "string",
          "description": "The skin color of the character"
        },
        "eye_color": {
          "type": "string",
          "description": "The eye color of the character"
        },
        "birth_year": {
          "type": "string",
          "description": "The birth year of the character"
        },
        "gender": {
          "type": "string",
          "description": "The gender of the character"
        },
        "homeworld": {
          "type": "string",
          "format": "uri",
          "description": "URL to the character's homeworld"
        },
        "created": {
          "type": "string",
          "format": "date-time",
          "description": "ISO 8601 date-time when the resource was created"
        },
        "edited": {
          "type": "string",
          "format": "date-time",
          "description": "ISO 8601 date-time when the resource was last edited"
        },
        "url": {
          "type": "string",
          "format": "uri",
          "description": "The URL of the character resource"
        }
      },
      "additionalProperties": false
    },
    "minItems": 0
  }

  
  :param base_result: Data (List) from OLD Start Wars API
  :param latest_result: Data (List) from OLD Start Wars API
  """
  for base_person, latest_person in zip(base_result, latest_result):
    base_person.update(latest_person)

  print(f"Merging complete.")
  return base_result