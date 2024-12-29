# MODELS = {
#     'category': Category,
#     'genre': Genre,
#     'users': User,
#     'titles': Title,
#     'review': Review,
#     'comments': Comment,
#     'genre_title': GenreTitle
# }

# MODELS = [
#     {'category': Category},
#     {'genre': Genre},
#     {'users': User},
#     {'titles': Title},
#     {'review': Review},
#     {'comments': Comment},
#     # 'genre_title': GenreTitle
# ]

# MODELS = {
#     'category': 1,
#     'genre': 2,
#     'users': 3,
#     'titles': 4,
#     'review': 5,
#     'comments': 6,
#     'genre_title': 7
# }

# MODELS = [
#     {'category': 1},
#     {'genre': 2},
#     {'users': 3},
#     {'titles': 4},
#     {'review': 5},
#     {'comments': 6},
#     # 'genre_title': GenreTitle
# ]

# for key, value in MODELS.items():
#     print(f'key={key}, value={value}', end='\n')

import os
print(os.listdir('static/data/'))
