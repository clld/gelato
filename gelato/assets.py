from clld.web.assets import environment
from clldutils.path import Path

import gelato


environment.append_path(
    Path(gelato.__file__).parent.joinpath('static').as_posix(),
    url='/gelato:static/')
environment.load_path = list(reversed(environment.load_path))
