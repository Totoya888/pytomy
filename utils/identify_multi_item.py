import re

chinese_to_arabic = {
    '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, 
    '六': 6, '七': 7, '八': 8, '九': 9, '十': 10
}

def chinese_to_int(chinese):
    num = 0
    for char in chinese:
        if char in chinese_to_arabic:
            num = num * 10 + chinese_to_arabic[char]
    return num

def identify_multi_item(name):
  multi_item_keywords = re.compile(r'(\d+|[一二三四五六七八九十]+)\s*(盒|件組|箱組|包|套|組|件|入|瓶)')
  match = multi_item_keywords.search(name)
  if match:
    text = ""
    quantity_str = match.group(1)
    quantity = 1
    if quantity_str.isdigit():
      quantity = int(quantity_str)
    else:
      quantity = chinese_to_int(quantity_str)
    text = '偵測到"{}"有{}個'.format(name,quantity)
    # if(quantity > 10):
    #    text = '此商品"{}"有10件以上(不以採計)'.format(name)
    return quantity, text

  return 1, ""