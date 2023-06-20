from sqlalchemy.orm import joinedload
from clld.web import datatables
from clld.web.datatables.base import LinkCol, Col, LinkToMapCol
from clld.web.datatables.base import DataTable
from clld_morphology_plugin import models

from coco import models


def includeme(config):
    """register custom datatables"""


class Cognatesets(DataTable):
    def col_defs(self):
        return [LinkCol(self, "name"), Col(self, "description")]


class MorphCognates(DataTable):
    def col_defs(self):
        return [
            LinkCol(
                self,
                "counterpart",
                # model_col=models.Morph.name,
                get_obj=lambda i: i.counterpart,
            ),
            Col(
                self,
                "description",
                model_col=models.Morph.description,
                get_obj=lambda i: i.counterpart,
            ),
        ]


class StemCognates(DataTable):
    def col_defs(self):
        return [
            LinkCol(
                self,
                "counterpart",
                # model_col=models.Stem.name,
                get_obj=lambda i: i.counterpart,
            ),
            Col(
                self,
                "description",
                model_col=models.Stem.description,
                get_obj=lambda i: i.counterpart,
            ),
        ]


class FormCognates(DataTable):
    def col_defs(self):
        return [
            LinkCol(
                self,
                "counterpart",
                # model_col=models.Form.name,
                get_obj=lambda i: i.counterpart,
            ),
            Col(
                self,
                "description",
                model_col=models.Form.description,
                get_obj=lambda i: i.counterpart,
            ),
        ]


def includeme(config):
    config.register_datatable("cognatesets", Cognatesets)
    config.register_datatable("morphcognates", MorphCognates)
    config.register_datatable("stemcognates", StemCognates)
    config.register_datatable("formcognates", FormCognates)
