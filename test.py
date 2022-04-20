from requests import get, post, delete


# ['title'],
# ['genre_id'],
# ['content'],
# ['user_id'],
# ['is_private']

print(post('http://localhost:5000/api/works',
           json={'title': 'Драма',
                 'description': 'тут описание',
                 'content': 'Текст3',
                 'genre_id': 1,
                 'user_id': 1,
                 'is_private': False}).json())

# print(delete('http://localhost:5000/api/works/2'))


# print(get('http://localhost:5000/api/works/3').json())
