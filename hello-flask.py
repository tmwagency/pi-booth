from flask import Flask, render_template
from app import user

app = Flask(__name__)

@app.route('/')
@app.route('index')
def index():
    
    return "<b>Hello World</b>" + user.hello() + "<h1>" + str(user.return_users()) + "</h1>"
    print "the line is" + user.hello()
    


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
