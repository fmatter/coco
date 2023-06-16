from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin, PolymorphicBaseMixin
from clld.db.models import common, IdNameDescriptionMixin
from clld_morphology_plugin.models import Morph, Wordform, Form, Stem
from coco.interfaces import ICognateset
import sqlalchemy as sa

#-----------------------------------------------------------------------------
# specialized common mapper classes
#-----------------------------------------------------------------------------



@implementer(ICognateset)
class Cognateset(Base, PolymorphicBaseMixin, IdNameDescriptionMixin):
    meaning = sa.Column(sa.String)
    @property
    def reflexes(self):
        res = []
        for field in ["forms"]:
            print(getattr(self, field))
            res.extend(self[field])
        return res
    

class FormCognate(Base):
    cognateset_pk = sa.Column(sa.Integer, sa.ForeignKey("cognateset.pk"))
    cognateset = sa.orm.relationship(Cognateset, backref="forms")
    counterpart_pk = sa.Column(sa.Integer, sa.ForeignKey("form.pk"))
    counterpart = sa.orm.relationship(Form, backref="cognates")
    doubt = sa.Column(sa.Boolean, default=False)
    alignment = sa.Column(sa.Unicode)

class MorphCognate(Base):
    cognateset_pk = sa.Column(sa.Integer, sa.ForeignKey("cognateset.pk"))
    cognateset = sa.orm.relationship(Cognateset, backref="morphs")
    counterpart_pk = sa.Column(sa.Integer, sa.ForeignKey("morph.pk"))
    counterpart = sa.orm.relationship(Morph, backref="cognates")
    doubt = sa.Column(sa.Boolean, default=False)
    alignment = sa.Column(sa.Unicode)

class StemCognate(Base):
    cognateset_pk = sa.Column(sa.Integer, sa.ForeignKey("cognateset.pk"))
    cognateset = sa.orm.relationship(Cognateset, backref="stems")
    counterpart_pk = sa.Column(sa.Integer, sa.ForeignKey("stem.pk"))
    counterpart = sa.orm.relationship(Stem, backref="cognates")
    doubt = sa.Column(sa.Boolean, default=False)
    alignment = sa.Column(sa.Unicode)