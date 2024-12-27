PARAMETRS = [
    {'genre__slug': 'genre'},
    {'category__slug': 'category'},
    {'name': 'name'},
    {'year': 'year'}
]


for parametr in PARAMETRS:
    print(type(list(parametr.values())[0]))
    print(**parametr)
