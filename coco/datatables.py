from clld.web.datatables.base import Col, DataTable, LinkCol
from clld_morphology_plugin import models
from coco import models


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
            LinkCol(
                self,
                "language",
                get_obj=lambda i: i.counterpart.language,
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
            LinkCol(
                self,
                "language",
                get_obj=lambda i: i.counterpart.language,
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
                get_obj=lambda i: i.counterpart,
            ),
            LinkCol(
                self,
                "language",
                # model_col=models.Morph.name,
                get_obj=lambda i: i.counterpart.language,
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
