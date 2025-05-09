import re

def slugify_rus_to_eng(text: str) -> str:
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        'вя': 'vya', 'ля': 'lya', 'ня': 'nya'
    }
    
    text = text.lower()
    slug = []
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i] + text[i+1] in translit_dict:
            slug.append(translit_dict[text[i] + text[i+1]])
            i += 2
        elif text[i] in translit_dict:
            slug.append(translit_dict[text[i]])
            i += 1
        elif text[i].isalnum():
            slug.append(text[i])
            i += 1
        else:
            slug.append('-')
            i += 1
    
    slug = ''.join(slug)
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug