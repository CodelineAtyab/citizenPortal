import extract
import transform
import load


def run_pipeline():
  postfix_msg = "Phase End. Beginning next phase ..."

  # Step 1
  result = extract.execute()
  print(f"Extraction {postfix_msg}")

  # Step 2
  result = transform.execute(*result)
  print(f"Transformation {postfix_msg}")

  # Step 3
  result = load.execute(result)
  print(f"Load Phase {postfix_msg}")

  print("Pipeline Complete.")

if __name__ == "__main__":
  run_pipeline()
