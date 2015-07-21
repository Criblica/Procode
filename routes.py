from flask import Flask, render_template
  
app = Flask(__name__)
  

"""
    Routes for main menu
"""
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/tutorials')
def tutorials():
    return render_template('tutorials/index.html')
  
@app.route('/about')
def about():
    return render_template('about.html')
  
  
  
"""
    Routes for tutorials
"""

@app.route('/tutorials/python')
def python():
    return render_template('tutorials/python.html')

if __name__ == '__main__':
    app.run(debug=True)