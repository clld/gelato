import pathlib

from clld.web.assets import environment

import gelato


environment.append_path(
    str(pathlib.Path(gelato.__file__).parent.joinpath('static')),
    url='/gelato:static/')
environment.load_path = list(reversed(environment.load_path))
