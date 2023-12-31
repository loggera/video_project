#!/usr/bin/env python3

import subprocess
import sys
import os
from vosk import Model, KaldiRecognizer, SetLogLevel

SAMPLE_RATE = 16000

SetLogLevel(0)
if not os.path.exists('model'):
    print('没有找到model')
    exit(1)
model = Model("model")
rec = KaldiRecognizer(model, SAMPLE_RATE)

with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i",
                       sys.argv[1],
                       "-ar", str(SAMPLE_RATE), "-ac", "1", "-f", "s16le", "-"],
                      stdout=subprocess.PIPE) as process:
    while True:
        data = process.stdout.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            print(rec.Result())
        else:
            print(rec.PartialResult())

    print(rec.FinalResult())
