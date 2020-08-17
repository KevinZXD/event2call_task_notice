import importlib
import os
from argparse import ArgumentParser

from sanic import Sanic

from views import EventView, MockEventView

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

setting_file_name = os.environ.get("SANIC_SETTINGS", 'settings')
settings_path = os.path.join(BASE_DIR, "conf/{}.py".format(setting_file_name))
settings_model = importlib.import_module("conf.{}".format(setting_file_name))

sanic_app = Sanic(name="task_notice", log_config=settings_model.LOGGING)
sanic_app.config.from_pyfile(settings_path)
sanic_app.add_route(EventView.as_view(), '/api/task_notice/')
sanic_app.add_route(MockEventView.as_view(), '/mock/api/task_notice/')

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", default=8585, help="port", type=int)
    parser.add_argument("--host", default="0.0.0.0", help="ip address")
    options = parser.parse_args()
    sanic_app.run(host=options.host, port=options.port)
