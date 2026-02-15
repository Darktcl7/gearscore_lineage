import os
from bs4 import BeautifulSoup

file_path = r"D:\Django Project\Alto Project\alto files\lineage2\bow.html"

with open(file_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

print("--- SEARCHING FOR IMAGES ---")
images = soup.find_all('img')
count = 0
for img in images:
    src = img.get('src', '')
    alt = img.get('alt', '')
    if 'bow_files' in src or 'Icon' in src:
        print(f"Img: src={src}, alt={alt}")
        count += 1
        if count > 20: break

# Coba cari elemen yang mungkin berisi nama item, biasanya class-nya ada 'name'
print("\n--- SEARCHING FOR tradeableitems-name ---")
name_elements = soup.find_all(class_=lambda x: x and 'tradeableitems-name' in x)
count = 0
for el in name_elements:
    text = el.get_text(strip=True)
    if text:
        print(f"Element {el.name} class={el.get('class')}: {text}")
        count += 1
        if count > 20: break
