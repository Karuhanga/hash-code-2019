def write_data(slides, file_name='a.txt'):
    file_name = 'outputs/{}'.format(file_name)
    result = "{}\n".format(len(slides))
    for slide in slides:
        result += ' '.join([str(photo.id) for photo in slide]) + "\n"
    with open(file_name, 'w') as file:
        file.write(result)
