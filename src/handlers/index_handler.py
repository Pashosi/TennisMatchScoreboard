import os

from jinja2 import Template

import config


class IndexHandler:

    def __call__(self):
        with open(os.path.join(config.BASE_DIR, "view", "templates", "index.html"), 'rb') as file:
            content_before = file.read().decode('utf-8')

            request_uri = os.path.join(config.BASE_DIR, "view", "templates", "index.html")

            template = Template(content_before)

            content_after = template.render(
                request_uri=request_uri,
            )
            return content_after
