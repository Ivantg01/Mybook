#Based on https://github.com/techwithtim/Flask-Web-App-Tutorial
#video https://www.youtube.com/watch?v=dam0GPOAvVI
#Based on https://github.com/alexroel/blog-flask
#video https://www.youtube.com/watch?app=desktop&v=JTAY5_LO0Ug
from flask import send_from_directory
from website import create_app

app = create_app()

#Definimos la ruta donde visualizar las caratulas
@app.route('/.bookfiles/<path:filename>')
def download_file(filename):
    return send_from_directory(app.root_path+"/../bookfiles/", filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

