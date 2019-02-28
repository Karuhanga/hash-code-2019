def read(file_name='a.txt'):
    file_name = 'inputs/{}'.format(file_name)
    data = []
    with open(file_name, 'r') as file:
        for line in file:
            data.append(line.strip())

    count = int(data.pop(0))
    words = {}
    photos = []
    from algo import Photo, Tag
    for index, photo in enumerate(data):
        photo_data = photo.split(' ')
        tags = photo_data[2:]
        photo = Photo(id=index, type=photo_data[0], tag_count=int(photo_data[1]), tags=tags)
        for word in tags:
            try:
                words[word].add_photo(photo)
            except KeyError:
                words[word] = Tag(word=word)
                words[word].add_photo(photo)
        photos.append(photo)

    return count, photos, words

