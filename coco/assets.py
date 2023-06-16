from pathlib import Path

from clld.web.assets import environment

import coco


environment.append_path(
    Path(coco.__file__).parent.joinpath('static').as_posix(),
    url='/coco:static/')
environment.load_path = list(reversed(environment.load_path))
