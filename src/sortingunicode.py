import icu 
collator = icu.Collator.createInstance(icu.Locale('pt_BR.UTF-8'))
fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
sorted_fruits = sorted(fruits, key=collator.getSortKey)
print(sorted_fruits)