import os
from flask import Flask, request, redirect, url_for
from flask_basicauth import BasicAuth
from werkzeug import secure_filename, formparser
from werkzeug.datastructures import FileStorage

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['rar'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['BASIC_AUTH_USERNAME'] = "nmw"
app.config['BASIC_AUTH_PASSWORD'] = "v5589sgr"


basic_auth = BasicAuth(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/test_is_protected')
@basic_auth.required
def foo():
    return 'test-secret'


@app.route('/', methods=['POST'])
@basic_auth.required
def upload_file():
    if request.method == "POST":
        # def custom_stream_factory(total_content_length, filename, content_type, content_length=None):
        #     import tempfile
        #     tmpfile = tempfile.NamedTemporaryFile(
        #         'wb+', prefix='flaskapp', suffix='.nc')
        #     app.logger.info(
        #         "start receiving file ... filename => " + str(tmpfile.name))
        #     return tmpfile

        # stream, form, files = formparser.parse_form_data(
        #     flask.request.environ, stream_factory=custom_stream_factory)
        # for fil in files.values():
        #     app.logger.info(" ".join(["saved form name", fil.name, "submitted as",
        #                               fil.filename, "to temporary file", fil.stream.name]))
        # Do whatever with stored file at `fil.stream.name`
        # FileStorage(stream).save(os.path.join(
        #    app.config['UPLOAD_FOLDER'], fil.stream.name))
        return 'OK', 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
