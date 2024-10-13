from jinja2 import Template

from src import config


class NewMatchHandler:

    def __call__(self):
        with open(f'{config.paths_list["templates_files"]}{config.paths_list["new_match"]}', 'rb') as file:
            content_before = file.read().decode('utf-8')

            request_uri = f'{config.paths_list["templates_files"]}' \
                          f'{config.paths_list["new_match"]}'



            temlate = Template(content_before)

            content_afer = temlate.render(
                request_uri=request_uri,
            )
            return content_afer
