import collections
import itertools
from pathlib import Path

from clld.cliutil import Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib import bibtex
from clldutils.color import qualitative_colors
from clldutils.misc import nfilter
from indicogram.scripts.initializedb import get_license_data, process_cldf
from pycldf import Dataset, Sources
from tqdm import tqdm

import coco
from coco import models


def main(args):
    data = Data()
    dataset = data.add(
        common.Dataset,
        args.cldf.properties.get("dc:id", "new"),
        id=args.cldf.properties.get("dc:id", "new"),
        name=args.cldf.properties.get("dc:title", None),
        domain=args.cldf.properties.get("dc:url", None),
        license=args.cldf.properties.get("dc:license", None),
        jsondata=get_license_data(
            args.cldf.properties.get("dc:license", None), small=False
        ),
        publisher_name="",
        publisher_place="",
        publisher_url="",
        description=args.cldf.properties.get("dc:title", ""),
    )

    def get_link(rec, field, datafield=None):
        if not datafield:
            datafield = field.replace("_ID", "")
        if field in rec and rec[field]:
            if isinstance(rec[field], list):
                return [data[datafield][x] for x in rec[field]]
            return data[datafield].get(rec[field])
        return None

    def get_source(entity):
        if entity["Source"]:
            bibkey, pages = Sources.parse(entity["Source"][0])
            return data["Source"][bibkey]
        return None

    process_cldf(data, dataset, args.cldf)
    for cogset in args.cldf.iter_rows("CognatesetTable"):
        new_cogset = data.add(
            models.Cognateset,
            cogset["ID"],
            id=cogset["ID"],
            description=cogset["Description"],
            contribution=get_link(cogset, "Contribution_ID"),
            source=get_source(cogset),
        )

    if "cognates.csv" in [str(x.url) for x in args.cldf.tables]:
        for cog in args.cldf.iter_rows("CognateTable"):
            if cog["Form_ID"]:
                data.add(
                    models.FormCognate,
                    cog["ID"],
                    counterpart=data["Form"][cog["Form_ID"]],
                    cognateset=data["Cognateset"][cog["Cognateset_ID"]],
                    alignment=" ".join(cog["Alignment"]),
                    contribution=get_link(cog, "Contribution_ID"),
                )
            if cog.get("Morph_ID"):
                data.add(
                    models.MorphCognate,
                    cog["ID"],
                    counterpart=data["Morph"][cog["Morph_ID"]],
                    cognateset=data["Cognateset"][cog["Cognateset_ID"]],
                    alignment=" ".join(cog["Alignment"]),
                    contribution=get_link(cog, "Contribution_ID"),
                )

    if "complexcognatesets.csv" in [str(x.url) for x in args.cldf.tables]:
        for cogset in args.cldf.iter_rows("complexcognatesets.csv"):
            data.add(
                models.ComplexCognateset,
                cogset["ID"],
                id=cogset["ID"],
                description=cogset["Description"],
            )

    cpx_dic = {"Stem_ID": models.StemCognate, "Morph_ID": models.ComplexMorphCognate, "Form_ID": models.ComplexFormCognate}
    if "complexcognates.csv" in [str(x.url) for x in args.cldf.tables]:
        for cog in args.cldf.iter_rows("complexcognates.csv"):
            for key, model in cpx_dic.items():
                if cog[key]:
                    data.add(
                        model,
                        cog["ID"],
                        counterpart=get_link(cog, key),
                        cognateset=data["ComplexCognateset"][cog["Cognateset_ID"]],
                        alignment=" ".join(cog["Alignment"]),
                    )
            # if cog["Morph_ID"]:
            #     data.add(
            #         models.ComplexMorphCognate,
            #         cog["ID"],
            #         counterpart=data["Morph"][cog["Morph_ID"]],
            #         cognateset=data["ComplexCognateset"][cog["Cognateset_ID"]],
            #         alignment=" ".join(cog["Alignment"]),
            #     )
            # if cog["Form_ID"]:
            #     data.add(
            #         models.ComplexFormCognate,
            #         cog["ID"],
            #         counterpart=data["Form"][cog["Form_ID"]],
            #         cognateset=data["ComplexCognateset"][cog["Cognateset_ID"]],
            #         alignment=" ".join(cog["Alignment"]),
            #     )

    media = {}
    for med in args.cldf.iter_rows("MediaTable"):
        media[med["ID"]] = med

    for tree in args.cldf.iter_rows("TreeTable"):
        data.add(
            models.Tree,
            tree["ID"],
            id=tree["ID"],
            newick=media[tree["Media_ID"]]["Download_URL"].path.split(",", 1)[1],
        )


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
