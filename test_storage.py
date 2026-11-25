import os
import tempfile
import unittest
from io import BytesIO
from types import SimpleNamespace
from unittest.mock import patch

from flask import Flask
from werkzeug.datastructures import FileStorage

from app.storage import delete_upload, media_url, save_upload


class MediaStorageTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.app = Flask(__name__)
        self.app.config.update(
            MEDIA_STORAGE='local',
            UPLOAD_FOLDER=self.temp_dir.name,
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_local_upload_round_trips_avatar_and_video_paths(self):
        with self.app.test_request_context():
            avatar = FileStorage(stream=BytesIO(b'image'), filename='player photo.jpg')
            avatar_reference = save_upload(avatar, 'avatars')
            self.assertTrue(avatar_reference.startswith('uploads/avatars/'))
            self.assertTrue(os.path.isfile(os.path.join(
                self.temp_dir.name,
                *avatar_reference[len('uploads/'):].split('/'),
            )))
            self.assertEqual(
                media_url(avatar_reference),
                f'/static/{avatar_reference}',
            )

            video = FileStorage(stream=BytesIO(b'video'), filename='match clip.mp4')
            video_reference = save_upload(video, 'videos')
            self.assertTrue(video_reference.startswith('videos/'))
            self.assertEqual(media_url(video_reference), f'/static/uploads/{video_reference}')
            delete_upload(video_reference)
            self.assertFalse(os.path.exists(os.path.join(
                self.temp_dir.name,
                *video_reference.split('/'),
            )))

    def test_blob_upload_and_delete_use_the_sdk_with_public_access(self):
        uploaded_arguments = []
        deleted = []

        def put_blob(*args, **kwargs):
            uploaded_arguments.append((args, kwargs))
            return SimpleNamespace(url='https://blob.example/avatar.jpg')

        def delete_blob(reference):
            deleted.append(reference)

        blob_client = SimpleNamespace(put_blob=put_blob, delete_blob=delete_blob)
        self.app.config['MEDIA_STORAGE'] = 'vercel_blob'
        with self.app.test_request_context(), patch('app.storage._blob_client', return_value=blob_client):
            upload = FileStorage(stream=BytesIO(b'image'), filename='avatar.jpg', content_type='image/jpeg')
            reference = save_upload(upload, 'avatars')

            self.assertEqual(reference, 'https://blob.example/avatar.jpg')
            self.assertEqual(uploaded_arguments[0][1]['access'], 'public')
            self.assertEqual(uploaded_arguments[0][1]['content_length'], 5)
            self.assertEqual(media_url(reference), reference)
            delete_upload(reference)
            self.assertEqual(deleted, [reference])

    def test_local_delete_rejects_paths_outside_upload_root(self):
        with self.app.app_context(), self.assertRaises(ValueError):
            delete_upload('../outside.txt')


if __name__ == '__main__':
    unittest.main()
