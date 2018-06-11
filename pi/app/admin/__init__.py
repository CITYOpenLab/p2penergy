###########
# imports #
###########

from flask import Blueprint

# create blueprint
bp = Blueprint("admin", __name__, url_prefix="/admin", static_folder="static",
               static_url_path="/admin/static", template_folder="templates")

# import routes
from . import routes
