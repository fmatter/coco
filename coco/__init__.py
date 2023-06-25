import collections

from clld.web.icon import MapMarker
from clldutils.svg import data_url, icon, pie
from pyramid.config import Configurator

# we must make sure custom models are known at database initialization!
from coco import interfaces, models
from coco.maps import CognatesetMap


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""

    config = Configurator(settings=settings)
    config.include("clld.web.app")
    config.include("clld_corpus_plugin")
    config.include("clld_morphology_plugin")
    config.include("clld_markdown_plugin")
    config.include("clld_document_plugin")

    config.register_resource(
        "cognateset",
        models.Cognateset,
        interfaces.ICognateset,
        with_index=True,
        with_detail=True,
    )

    config.register_resource(
        "morphcognate",
        models.MorphCognate,
        interfaces.IMorphCognate,
        with_index=True,
    )

    config.register_resource(
        "stemcognate",
        models.StemCognate,
        interfaces.IStemCognate,
        with_index=True,
    )

    config.register_resource(
        "formcognate",
        models.FormCognate,
        interfaces.IFormCognate,
        with_index=True,
    )

    config.register_map("cognateset", CognatesetMap)
    return config.make_wsgi_app()
