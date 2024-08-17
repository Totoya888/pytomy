import json

with open('db/atomy_products.json') as f:
  data = json.load(f)
  print(data["date"])
  for i, c in enumerate(data["body"]):
    file = open(f'db/atomy_products/atomy_products_{i}.json', 'w', encoding='utf-8')
    with_date_data = {"date": data["date"], "body": c}
    json.dump(with_date_data, file, indent=2, ensure_ascii=False)
