import io

import soundfile
from flask import Flask, request
from pycwgen.morse import stream_morse_code
import time

app = Flask(__name__)


@app.route('/cw.ogg')
def generate_cw():
    text = request.args['text']
    wpm = int(request.args.get('wpm', 12))
    tone = int(request.args.get('tone', 600))

    headers = {'Content-type': 'audio/ogg'}

    if request.method == 'HEAD':
        return '', 200, headers

    zero = time.time()

    options = {
        'format': 'OGG',
        'subtype': 'VORBIS',
        'samplerate': 44100,
        'channels': 1,
    }

    output = io.BytesIO()
    with soundfile.SoundFile(output, 'w', **options) as fp:
        stream_morse_code(fp, text, wpm=wpm, tone=tone)
    end = time.time()

    print('Audio generated in {:.3g} seconds'.format(end-zero))

    return output.getvalue(), 200, headers
