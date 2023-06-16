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

    process_cldf(data, dataset, args.cldf)

    for cogset in args.cldf.iter_rows("CognatesetTable"):
        data.add(
            models.Cognateset,
            cogset["ID"],
            id=cogset["ID"],
            # name=cogset["Form"],
            meaning=cogset["Description"],
        )

    for cog in args.cldf.iter_rows("CognateTable"):
        if cog["Form_ID"]:
            data.add(
                models.Cognate,
                cog["ID"],
                counterpart=data["Form"][cog["Form_ID"]],
                cognateset=data["Cognateset"][cog["Cognateset_ID"]],
                alignment=" ".join(cog["Alignment"]),
            )
        if cog["Morph_ID"]:
            data.add(
                models.Cognate,
                cog["ID"],
                counterpart=data["Morph"][cog["Morph_ID"]],
                cognateset=data["Cognateset"][cog["Cognateset_ID"]],
                alignment=" ".join(cog["Alignment"]),
            )
        if cog["Stem_ID"]:
            data.add(
                models.Cognate,
                cog["ID"],
                counterpart=data["Stem"][cog["Stem_ID"]],
                cognateset=data["Cognateset"][cog["Cognateset_ID"]],
                alignment=" ".join(cog["Alignment"]),
            )


    # dss = []
    # for file in Path("/home/florianm/Dropbox/research/cariban/cldf_datasets/meira_box/").glob("*/*_cldf/cldf/metadata.json"):
    #     dss.append(file)

    # lgs = []
    # for ds in dss:
    #     cldf = Dataset.from_metadata(ds)
    #     print(cldf)
    #     process_cldf(data, dataset, cldf)
    # for lang in tqdm(cldf.iter_rows("LanguageTable")):
    #     if lang["ID"] in lgs:
    #         continue
    #     lgs.append(lang["ID"])
    #     data.add(
    #         common.Language,
    #         lang["ID"],
    #         id=lang["ID"],
    #         name=lang["Name"],
    #         latitude=lang["Latitude"],
    #         longitude=lang["Longitude"],
    #     )

    # for ex in tqdm(cldf.iter_rows("ExampleTable")):
    #     ex["Analyzed_Word"] = ["" if x is None else x for x in ex["Analyzed_Word"]]
    #     ex["Gloss"] = ["" if x is None else x for x in ex["Gloss"]]
    #     new_ex = data.add(
    #         common.Sentence,
    #         ex["ID"],
    #         id=ex["ID"],
    #         name=ex["Primary_Text"],
    #         description=ex["Translated_Text"],
    #         analyzed="\t".join(ex["Analyzed_Word"]),
    #         gloss="\t".join(ex["Gloss"]),
    #         language=data["Language"][ex["Language_ID"]],
    #         comment=ex["Comment"],
    #     )
    # if "Original_Translation" in ex:
    #     new_ex.markup_description = ex["Original_Translation"]
    # if "speakers.csv" in cldf_tables:
    #     data.add(
    #         corpus.SpeakerSentence,
    #         ex["ID"],
    #         sentence=new_ex,
    #         speaker=data["Speaker"][ex["Speaker_ID"]],
    #     )
    # if ex.get("Text_ID", None) is not None:
    #     data.add(
    #         corpus.TextSentence,
    #         ex["ID"],
    #         sentence=new_ex,
    #         text=data["Text"][ex["Text_ID"]],
    #         record_number=ex["Record_Number"],
    #         phrase_number=ex.get("Phrase_Number", None),
    #     )
    # elif len(ex.get("Source", [])) > 0:
    #     bibkey, pages = Sources.parse(ex["Source"][0])
    #     source = data["Source"][bibkey]
    #     DBSession.add(
    #         common.SentenceReference(
    #             sentence=new_ex, source=source, key=source.id, description=pages
    #         )
    #     )
    # if "Media_ID" in ex and ex["Media_ID"]:
    #     common.Sentence_files(
    #         object=new_ex,
    #         id=ex["Media_ID"],
    #         name=ex["Media_ID"],
    #         mime_type="audio/wav",
    #     )
    # elif ex["ID"] in media:
    #     common.Sentence_files(
    #         object=new_ex,
    #         id=ex["ID"],
    #         name=ex["ID"],
    #         mime_type="audio/wav",
    #     )

    # forms = pd.read_csv("../aggregated.csv", keep_default_na=False)
    # forms["IPA"] = forms.apply(
    #     lambda x: ipaify(x["Headword"], profile=x["Language_ID"], warn=False),
    #     axis=1,
    # )
    # bad = forms[forms["IPA"].str.contains("�")]
    # print(bad)
    # good = forms[~(forms["IPA"].str.contains("�"))]
    # lg_data = crh.language_data
    # for lg in set(good["Language_ID"]):
    #     print(lg)
    #     print(lg_data.get(lg))
    #     data.add(
    #         common.Language,
    #         lg,
    #         id=lg,
    #         name=lg_data[lg]["Name"],
    #         latitude=lg_data[lg]["Latitude"],
    #         longitude=lg_data[lg]["Longitude"],
    #     )
    # for form in good.to_dict("records"):
    #     data.add(
    #         common.Unit,
    #         form["ID"],
    #         language=data["Language"][form["Language_ID"]],
    #         name=form["IPA"],
    #         description=form["Meaning"] + f" ({form['Headword']})",
    #     )


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
