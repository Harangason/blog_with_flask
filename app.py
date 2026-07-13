import json
from flask import Flask

app = Flask(__name__)

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

class DataLoader:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path
        self.data = {}

    def load_data(self):
        with open(self.data_file_path, 'r') as file:
            self.data = json.load(file)
            return self.data

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




def repository_data_loader(data_file_path):
    data_loader = DataLoader(data_file_path)
    return data_loader.load_data()



@app.route('/')
def hello_world():
    return 'Hello, World!'



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
