import json
from flask import Flask, Response, redirect, render_template, request, send_from_directory, url_for
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent

class User:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def get_full_name(self) -> str:
        """Returns the full name of the user."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return ""

class Blog:
    def __init__(self, content):
        self.content = content

    def get_content(self) -> str:
        return self.content

class Title:
    def __init__(self, title):
        self.title = title

    def get_title(self) -> str:
        return self.title

class BlogPost:
    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author

class UnifyIDs:
    def __init__(self, data):
        self.data = data
        self.unique_ids = set()
        self.id_counter = 1

    def generate_unique_ids(self):
        for item in self.data:
            if "id" not in item:
                item["id"] = self.id_counter
                self.id_counter += 1

class DataLoader:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path
        self.data = {}

    def load_data(self):
        try:
            with open(self.data_file_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
                return self.data
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = []
            return self.data

def repository_data_loader(data_file_path):
    data_loader = DataLoader(data_file_path)
    return data_loader.load_data()

class DataWriter:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path
        self.data = {}

    def define_data_structure(self, data=None):
        post_schema = [
            {
                "id": 1,
                "author": "John Doe",
                "title": "First Post",
                "content": "This is my first post.",
                "likes": 0,
            }
        ]

        if data is None:
            self.data = post_schema
            return self.data

        if not isinstance(data, (dict, list)):
            raise ValueError("Data must be a dictionary or a list of dictionaries.")

        if isinstance(data, dict):
            data = [data]

        if not data:
            self.data = post_schema
            return self.data

        required_keys = {"id", "author", "title", "content"}
        if any(not isinstance(item, dict) or not required_keys.issubset(item) for item in data):
            raise ValueError(
                "Each post must be a dictionary with keys: id, author, title, content."
            )
        for item in data:
            item.setdefault("likes", 0)

        self.data = data
        return self.data

    def write_data(self, data):
        if isinstance(data, tuple):
            data = list(data)
        if isinstance(data, BlogPost):
            data = data.__dict__
        payload = self.define_data_structure(data)
        with open(self.data_file_path, 'w', encoding='utf-8') as file:
            json.dump(payload, file, indent=2)
            return True
        return False


def get_posts():
    blog_posts = repository_data_loader(str(BASE_DIR / "dictionary" / "data.json"))
    if isinstance(blog_posts, dict):
        return [blog_posts]
    if not isinstance(blog_posts, list):
        return []
    return blog_posts


def _post_id(post):
    try:
        return int(post.get("id"))
    except (AttributeError, TypeError, ValueError):
        return None


def fetch_post_by_id(post_id):
    for post in get_posts():
        if _post_id(post) == post_id:
            return post
    return None


@app.route('/')
def index():
    blog_posts = get_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form.get('author', 'John Doe')
        blog_posts = get_posts()
        if isinstance(blog_posts, dict):
            blog_posts = [blog_posts]

        existing_ids = [
            int(post.get("id"))
            for post in blog_posts
            if isinstance(post, dict) and str(post.get("id")).isdigit()
        ]
        next_id = max(existing_ids, default=0) + 1

        blog_post = {
            "id": next_id,
            "title": title,
            "author": author,
            "content": content,
            "likes": 0,
        }
        blog_posts.append(blog_post)
        data_writer = DataWriter(str(BASE_DIR / "dictionary" / "data.json"))
        data_writer.write_data(blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    data_file = str(BASE_DIR / "dictionary" / "data.json")
    blog_posts = get_posts()

    filtered_posts = [
        post
        for post in blog_posts
        if _post_id(post) != post_id
    ]

    data_writer = DataWriter(data_file)
    data_writer.write_data(filtered_posts)
    return redirect(url_for("index"))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        data_file = str(BASE_DIR / "dictionary" / "data.json")
        blog_posts = get_posts()
        for stored_post in blog_posts:
            if _post_id(stored_post) == post_id:
                stored_post["title"] = request.form.get("title", stored_post.get("title"))
                stored_post["author"] = request.form.get("author", stored_post.get("author"))
                stored_post["content"] = request.form.get("content", stored_post.get("content"))
                break

        data_writer = DataWriter(data_file)
        data_writer.write_data(blog_posts)
        return redirect(url_for("index"))

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)

@app.route('/favicon.ico')
def favicon():
    favicon_path = BASE_DIR / "static" / "favicon.ico"
    if not favicon_path.exists():
        return Response(status=204)
    return send_from_directory(BASE_DIR / "static", "favicon.ico")


@app.route('/like/<int:id>')
def like_post(id):
    post_id = id
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    blog_posts = get_posts()
    for stored_post in blog_posts:
        if _post_id(stored_post) == post_id:
            current_likes = stored_post.get("likes", 0)
            try:
                current_likes = int(current_likes)
            except (TypeError, ValueError):
                current_likes = 0
            stored_post["likes"] = current_likes + 1
            break

    data_writer = DataWriter(str(BASE_DIR / "dictionary" / "data.json"))
    data_writer.write_data(blog_posts)
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
