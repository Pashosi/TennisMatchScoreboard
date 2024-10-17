from jinja2 import Template

from src import config


class IndexHandler:

    def __call__(self):
        with open(f'{config.paths_list["templates_files"]}{config.paths_list["index"]}', 'rb') as file:
            content_before = file.read().decode('utf-8')

            request_uri = f'{config.paths_list["templates_files"]}' \
                          f'{config.paths_list["index"]}'

            template = Template(content_before)

            content_after = template.render(
                request_uri=request_uri,
            )
            return content_after
