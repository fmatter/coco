import collections

from clld.interfaces import IDomainElement, IMapMarker, IValue, IValueSet
from clld.web.icon import MapMarker
from clldutils.svg import data_url, icon, pie
from pyramid.config import Configurator

# we must make sure custom models are known at database initialization!
from coco import interfaces, models
from coco.maps import CognatesetMap


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    # settings["clld_markdown_plugin"] = {
    #     "model_map": {
    #         TextTable["url"]: {
    #             "route": "text",
    #             "model": Text,
    #             "decorate": lambda x: f"'{x}'",
    #         },
    #         "phonemes.csv": {
    #             "route": "phoneme",
    #             "model": models.Phoneme,
    #             "decorate": lambda x: f"/{x}/",
    #         },
    #         "chapters.csv": {
    #             "route": "document",
    #             "model": Document,
    #         },
    #         POSTable["url"]: {"route": "pos", "model": POS},
    #     },
    #     "renderer_map": {
    #         "FormTable": render_lfts,
    #         MorphTable["url"]: render_lfts,
    #         MorphemeTable["url"]: render_lfts,
    #         WordformTable["url"]: render_lfts,
    #         LexemeTable["url"]: render_lfts,
    #     },
    #     "extensions": [],
    # }

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
    # config.register_resource(
    #     "phoneme", models.Phoneme, interfaces.IPhoneme, with_index=True
    # )

    # config.add_page("description")
    # config.add_page("corpus")
    # config.add_page("morphosyntax")
    # config.add_page("lexicon")

    return config.make_wsgi_app()
