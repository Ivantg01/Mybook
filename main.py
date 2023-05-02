#### Imports
from flask import send_from_directory
from website import create_app
from gconfig import gconfig

#### Variables
app = create_app()   #create the flask app

#### Route to display book covers
@app.route('/cover/<path:filename>')
def download_file(filename):
    return send_from_directory(gconfig.BOOK_PATH, filename, as_attachment=True)

#Start the flask app
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001)




