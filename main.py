#Based on https://github.com/techwithtim/Flask-Web-App-Tutorial
#video https://www.youtube.com/watch?v=dam0GPOAvVI
#Based on https://github.com/alexroel/blog-flask
#video https://www.youtube.com/watch?app=desktop&v=JTAY5_LO0Ug

from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)