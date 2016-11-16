#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.factory import create_app
from api.utils.config import DevelopmentConfig

if __name__ == '__main__':
    app = create_app(DevelopmentConfig)
    app.run(port=5000, host="0.0.0.0", use_reloader=True)
