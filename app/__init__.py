import os
import requests
import requests_cache
from flask import Flask, render_template, request, jsonify
from flask_assets import Environment, Bundle

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config.from_object(os.environ['APP_SETTINGS'])


requests_cache.install_cache('fs_cache', backend='sqlite', expire_after=86400)

assets = Environment(app)

# #: application css bundle
# css_mig = Bundle("less/mig.less",
#                        filters="less", output="css/mig.css",
#                        debug=False)


# #: consolidated css bundle
# css_all = Bundle("css/uikit.css",
#                     "css/mig.css", css_mig,
#                     output="css/mig_bundle.css")


# #: vendor js bundle
# js_ui = Bundle("js/uikit.js",
#                    "js/uikit-icons.js",
#                    "js/jquery-3.4.1.js",
#                    "js/mig-app.js",
#                    output="js/mig-ui.js")

# assets.register('css_all', css_all)
# assets.register('js_ui', js_ui)
assets.manifest = 'cache' if not app.debug else False
assets.cache = not app.debug
assets.debug = app.debug


from app import routes