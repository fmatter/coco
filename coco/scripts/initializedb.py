from pathlib import Path
import itertools
import collections

from clldutils.misc import nfilter
from clldutils.color import qualitative_colors
from clld.cliutil import Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from pycldf import Dataset
from clld.lib import bibtex


import coco
from coco import models
from karipona.transliterate import ipaify
import pandas as pd
import karipona
from tqdm import tqdm
from indicogram.scripts.initializedb import process_cldf


def main(args):
    data = Data()
    dataset = data.add(
        common.Dataset,
        "coco",
        id="coco",
        name="coco",  # all the dc:X data should be in your CLDF dataset
        domain="coco.org",
        # license=cldf.properties.get("dc:license", None),
        # jsondata=get_license_data(cldf.properties.get("dc:license", None), small=False),
        publisher_name="",
        publisher_place="",
        publisher_url="",
    )

    def get_link(rec, field, datafield=None):
        if not datafield:
            datafield = field.replace("_ID", "")
        if field in rec and rec[field]:
            if isinstance(rec[field], list):
                return [data[datafield][x] for x in rec[field]]
            return data[datafield].get(rec[field])
        return None

    process_cldf(data, dataset, args.cldf)
    for cogset in args.cldf.iter_rows("CognatesetTable"):
        data.add(
            models.Cognateset,
            cogset["ID"],
            id=cogset["ID"],
            description=cogset["Description"],
            contribution=get_link(cogset, "Contribution_ID"),
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
            if cog.get("Stem_ID"):
                data.add(
                    models.StemCognate,
                    cog["ID"],
                    counterpart=data["Stem"][cog["Stem_ID"]],
                    cognateset=data["Cognateset"][cog["Cognateset_ID"]],
                    alignment=" ".join(cog["Alignment"]),
                    contribution=get_link(cog, "Contribution_ID"),
                )


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
