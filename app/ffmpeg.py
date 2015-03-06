#!/usr/local/bin/python3
from operator import methodcaller

import re


def reader(f):
    while True:
        data = f.read(10)
        if not data:
            raise StopIteration

        yield data


def line_reader(f):
    last_line = ''

    for read in reader(f):
        last_line += read.decode('ascii')
        lines = re.split(r'[\r\n]', last_line)

        last_line = lines.pop()
        yield from lines


def ffmpeg_stderr_reader(stderr):
    for line in filter(methodcaller('startswith', 'frame='), line_reader(stderr)):
    # for line in stderr.splitlines():
        yield dict(re.findall('([a-z]+)\s*=\s*(\S+)', line))

