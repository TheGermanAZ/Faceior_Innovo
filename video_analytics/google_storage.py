from gcloud import storage
client = storage.Client()

def push_to_storage(filename):
    bucket = client.get_bucket('hophacks-289306.appspot.com')
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)

