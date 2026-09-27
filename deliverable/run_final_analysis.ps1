# Run from the project root after installing requirements.txt and Pylint.
$ErrorActionPreference = "Stop"

python -m pylint main.py modules tests --output-format=text | Tee-Object deliverable/pylint_final.txt
python -m pylint main.py modules tests --output-format=json > deliverable/pylint_final.json
