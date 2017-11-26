#!/bin/bash

export FLASK_APP="cadetapi:create_app()"
export FLASK_DEBUG=1
flask run
