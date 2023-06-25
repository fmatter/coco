import os

from paste.deploy import loadapp
from waitress import serve
import shutil
if __name__ == "__main__":
    shutil.copy("development_tmpl.ini", "development.ini")
    port = int(os.environ.get("PORT", 5000))
    app = loadapp('config:development.ini', relative_to='.')

    serve(app, host='0.0.0.0', port=port)