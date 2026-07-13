import unittest


import json
import shutil
import tempfile
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import app as blog_app


class BlogAppTestCase(unittest.TestCase):
    def setUp(self):
        self.original_base_dir = blog_app.BASE_DIR
        self.temp_dir = Path(tempfile.mkdtemp())

        data_dir = self.temp_dir / "dictionary"
        data_dir.mkdir(parents=True, exist_ok=True)
        self.data_file = data_dir / "data.json"

        self.initial_posts = [
            {"id": 1, "author": "John Doe", "title": "First Post", "content": "First post content."},
            {"id": 2, "author": "Jane Doe", "title": "Second Post", "content": "Second post content."},
        ]
        with self.data_file.open("w", encoding="utf-8") as file:
            json.dump(self.initial_posts, file, indent=2)

        blog_app.BASE_DIR = self.temp_dir
        blog_app.app.testing = True
        self.client = blog_app.app.test_client()

    def tearDown(self):
        blog_app.BASE_DIR = self.original_base_dir
        shutil.rmtree(self.temp_dir)

    def test_index_page_loads_blog_posts(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("First Post", html)
        self.assertIn("Second Post", html)

    def test_fetch_post_by_id_returns_expected_post(self):
        post = blog_app.fetch_post_by_id(1)
        self.assertIsNotNone(post)
        self.assertEqual(post["title"], "First Post")

    def test_update_get_page_renders_form(self):
        response = self.client.get("/update/1")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("Update Blog Post", html)
        self.assertIn('action="/update/1"', html)

    def test_update_post_updates_file_and_redirects(self):
        payload = {
            "title": "Updated Title",
            "author": "Updated Author",
            "content": "Updated content text.",
        }
        response = self.client.post("/update/1", data=payload)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/", response.headers["Location"])

        with self.data_file.open(encoding="utf-8") as file:
            posts = json.load(file)

        updated_post = next(post for post in posts if post["id"] == 1)
        self.assertEqual(updated_post["title"], "Updated Title")
        self.assertEqual(updated_post["author"], "Updated Author")
        self.assertEqual(updated_post["content"], "Updated content text.")

    def test_delete_removes_selected_post(self):
        response = self.client.get("/delete/2")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/", response.headers["Location"])

        with self.data_file.open(encoding="utf-8") as file:
            posts = json.load(file)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]["id"], 1)

    def test_update_not_found_returns_404(self):
        response = self.client.get("/update/999")
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
