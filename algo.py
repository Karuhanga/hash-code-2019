import threading
from operator import itemgetter

from input import read
from output import write_data


class Tag:
    def __init__(self, word):
        self.word = word
        self.associated_photos = []

    def add_photo(self, photo):
        self.associated_photos.append(photo.id)


class Photo:
    def __init__(self, id, type, tag_count, tags):
        self.id = id
        self.type = type
        self.tag_count = tag_count
        self.tags = tags
        self.taken = False


FILE = 'a.txt'


if __name__ == "__main__":
    print("Running on: {}".format(FILE))
    count, photos, tags = read(FILE)
    stats = []
    results = []

    def build_stats(photo1, photos):
        for photo2 in photos:
            print("Double Recursing into photo {}".format(photo2.id))
            if photo1.id == photo2.id:
                continue
            both = list(photo1.tags)
            both.extend(photo2.tags)
            only_1 = set(both).difference(set(photo2.tags))
            only_2 = set(both).difference(set(photo1.tags))
            common = set(both).difference(only_1).difference(only_2)
            best = min(len(only_1), len(only_2), len(common))
            stats.append({
                'photo_1': photo1,
                'photo_2': photo2,
                'best': best
            })

    print("Building stats...")
    threads = []
    for photo1 in photos:
        print("Recursing into photo {}".format(photo1.id))
        thread = threading.Thread(target=build_stats, args=(photo1, photos))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    print("Done.\nSorting.")

    stats.sort(key=itemgetter('best'), reverse=True)

    print("Done.")


    def get_vertical(photos, companion):
        st = list(stats)
        st.reverse()
        for s in st:
            photo = s['photo_1']
            if not photo.taken and photo.type is 'V' and companion.id != photo.id:
                photo.taken = True
                return photo
            photo = s['photo_2']
            if not photo.taken and photo.type is 'V' and companion.id != photo.id:
                photo.taken = True
                return photo

        return False


    for index, stat in enumerate(stats):
        print("stat {} of {}".format(index+1, len(stats)))
        if not stat['photo_1'].taken:
            if not stat['photo_2'].taken:
                if stat['photo_1'].type is 'V':
                    vert = get_vertical(photos, stat['photo_1'])
                    if vert is False:
                        continue
                    stat['photo_1'].taken = True
                    results.append([stat['photo_1'], vert])
                else:
                    stat['photo_1'].taken = True
                    results.append([stat['photo_1']])

                if stat['photo_2'].type is 'V':
                    vert = get_vertical(photos, stat['photo_2'])
                    if vert is False:
                        continue
                    stat['photo_2'].taken = True
                    results.append([stat['photo_2'], vert])
                else:
                    stat['photo_2'].taken = True
                    results.append([stat['photo_2']])
            else:
                if stat['photo_1'].type is 'V':
                    vert = get_vertical(photos, stat['photo_1'])
                    if vert is False:
                        continue
                    stat['photo_1'].taken = True
                    results.append([stat['photo_1'], vert])
                else:
                    stat['photo_1'].taken = True
                    results.append([stat['photo_1']])
        else:
            if not stat['photo_2'].taken:
                if stat['photo_2'].type is 'V':
                    vert = get_vertical(photos, stat['photo_2'])
                    if vert is False:
                        continue
                    stat['photo_2'].taken = True
                    results.append([stat['photo_2'], vert])
                else:
                    stat['photo_2'].taken = True
                    results.append([stat['photo_2']])

    write_data(results, FILE)
