import json

with open('db/atomy_category.json') as f:
  data = json.load(f)
  print(data["date"])
  for i, c in enumerate(data["category"]):
    file = open(f'db/atomy_category/atomy_category_{i}.json', 'w', encoding='utf-8')
    with_date_data = {"date": data["date"], "body": c}
    json.dump(with_date_data, file, indent=2)
