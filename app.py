import json
from flask import Flask

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
        with open(self.data_file_path, 'r') as file:
            self.data = json.load(file)
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

        self.data = data
        return self.data

    def write_data(self, data):
        payload = self.define_data_structure(data)
        with open(self.data_file_path, 'w') as file:
            json.dump(payload, file, indent=2)
            return True
        return False









@app.route('/')
def index():
    blog_posts = repository_data_loader(str(BASE_DIR / "dictionary" / "data.json"))
    if isinstance(blog_posts, dict):
        blog_posts = [blog_posts]
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # adding a new blog post here
        title = request.form['title']
        content = request.form['content']
        blog_post = BlogPost(title, content, "John Doe")
        data_writer = DataWriter(str(BASE_DIR / "dictionary" / "data.json"))
        data_writer.write_data(blog_post)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    data_file = str(BASE_DIR / "dictionary" / "data.json")
    blog_posts = repository_data_loader(data_file)
    if isinstance(blog_posts, dict):
        blog_posts = [blog_posts]

    filtered_posts = [
        post
        for post in blog_posts
        if isinstance(post, dict) and int(post.get("id")) != post_id
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
            if isinstance(stored_post, dict) and int(stored_post.get("id")) == post_id:
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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
