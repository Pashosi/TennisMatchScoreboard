import os

from jinja2 import Template

import config


class NewMatchHandler:

    def __call__(self):
        with open(os.path.join(config.BASE_DIR, "view", "templates", "new-match.html"), 'rb') as file:
            content_before = file.read().decode('utf-8')

            request_uri = os.path.join(config.BASE_DIR, "view", "templates", "new-match.html")



            temlate = Template(content_before)

            content_afer = temlate.render(
                request_uri=request_uri,
            )
            return content_afer
