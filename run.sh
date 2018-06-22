#!/usr/bin/env bash
gunicorn -b :$PORT SciLog.wsgi
