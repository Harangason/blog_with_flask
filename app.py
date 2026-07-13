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

@app.route('/')
def hello_world():
    return 'Hello, World!'



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)