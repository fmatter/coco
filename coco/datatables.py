from sqlalchemy.orm import joinedload
from clld.web import datatables
from clld.web.datatables.base import LinkCol, Col, LinkToMapCol
from clld.web.datatables.base import DataTable

from coco import models


def includeme(config):
    """register custom datatables"""

class Cognatesets(DataTable):
    def col_defs(self):
        return [LinkCol(self, "name"), Col(self, "meaning")]


def includeme(config):
    config.register_datatable("cognatesets", Cognatesets)
