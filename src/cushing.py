import flickrapi
import os
import json
from tqdm import tqdm


class FlickrConnection:
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        self.connect = self._connect()

    def _connect(self):
        try:
            return flickrapi.FlickrAPI(self.key, self.secret, format='parsed-json')
        except Exception as e:
            raise ConnectionError(f"Error connecting to Flickr API: {e}")


class CushingImage:
    def __init__(self, photo_id, connection, output="output"):
        self.photo_id = photo_id
        self.connection = connection
        self.output = output

    def get_info(self):
        all_metadata = self.connection.photos.getInfo(photo_id=self.photo_id)
        descriptive_key_values = all_metadata['photo']['description']['_content'].split('\n')
        all_metadata['photo']['descriptive_metadata'] = {}
        for item in descriptive_key_values:
            no_bold = item.replace('<b>', '').replace('</b>', '')
            key, *values = no_bold.split(":")
            final_value = ':'.join(values).strip()
            if key != "":
                all_metadata['photo']['descriptive_metadata'][key] = final_value
        return all_metadata

    def get_exif(self):
        return self.connection.photos.getExif(photo_id=self.photo_id)

    def get_comments(self):
        return self.connection.photos.comments.getList(photo_id=self.photo_id)

    def get_sizes(self):
        return self.connection.photos.getSizes(photo_id=self.photo_id)

    def get_all(self):
        return {
            'metadata': self.get_info(),
            'exif': self.get_exif(),
            'comments': self.get_comments(),
            'sizes': self.get_sizes()
        }

    def get_all_as_json(self):
        return json.dumps(self.get_all(), indent=4)

    def write_to_file(self):
        with open(f"{self.output}/{self.photo_id}.json", 'w') as f:
            f.write(self.get_all_as_json())


class FindImages:
    def __init__(self, user_id, connection):
        self.user_id = user_id
        self.connection = connection

    def get_pages(self, until, per_page=500, start=3):
        total_items = (until - start + 1) * per_page
        with tqdm(total=total_items, desc="Processing items") as pbar:
            while start <= until:
                response = self.connection.photos.search(user_id=self.user_id, page=start, per_page=per_page)
                for photo in response['photos']['photo']:
                    data = CushingImage(photo_id=photo['id'], connection=self.connection)
                    data.write_to_file()
                    pbar.update(1)
                start += 1
        return


def main():
    flickr_key = os.getenv('FLICKR_KEY')
    flickr_secret = os.getenv('FLICKR_SECRET')

    if not flickr_key or not flickr_secret:
        raise ValueError("FLICKR_KEY and FLICKR_SECRET environment variables must be set")

    connection = FlickrConnection(flickr_key, flickr_secret).connect
    x = FindImages(user_id="29072716@N04", connection=connection)
    x.get_pages(start=16, until=25)


if __name__ == '__main__':
    main()
