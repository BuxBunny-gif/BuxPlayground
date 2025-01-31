from flask import Flask, render_template
import os

#template_dir = os.path.abspath('webFiles\\templates')

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), "webFiles", "templates"))
print(app.template_folder)
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)