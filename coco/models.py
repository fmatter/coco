import sqlalchemy as sa
from clld import interfaces
from clld.db.meta import Base, CustomModelMixin, PolymorphicBaseMixin
from clld.db.models import HasSourceMixin, IdNameDescriptionMixin, common
from clld.db.models.common import Contribution
from clld_morphology_plugin.models import Form, Morph, Stem, Wordform
from sqlalchemy import (Boolean, Column, ForeignKey, Integer, String, Unicode,
                        UniqueConstraint)
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref, relationship
from zope.interface import implementer

from coco.interfaces import (ICognateset, IFormCognate, IMorphCognate,
                             IStemCognate, ITree)

# -----------------------------------------------------------------------------
# specialized common mapper classes
# -----------------------------------------------------------------------------


@implementer(ICognateset)
class Cognateset(Base, PolymorphicBaseMixin, IdNameDescriptionMixin, HasSourceMixin):
    @property
    def reflexes(self):
        res = []
        for field in ["forms", "morphs", "stems"]:
            res.extend(getattr(self, field))
        return res

    contribution_pk = Column(Integer, ForeignKey("contribution.pk"))
    contribution = relationship(Contribution, backref="cognatesets")


@implementer(IFormCognate)
class FormCognate(Base):
    cognateset_pk = sa.Column(sa.Integer, sa.ForeignKey("cognateset.pk"))
    cognateset = sa.orm.relationship(Cognateset, backref="forms")
    counterpart_pk = sa.Column(sa.Integer, sa.ForeignKey("form.pk"))
    counterpart = sa.orm.relationship(Form, backref="cognates")
    doubt = sa.Column(sa.Boolean, default=False)
    alignment = sa.Column(sa.Unicode)

    contribution_pk = Column(Integer, ForeignKey("contribution.pk"))
    contribution = relationship(Contribution, backref="formcognates")


@implementer(IMorphCognate)
class MorphCognate(Base):
    cognateset_pk = sa.Column(sa.Integer, sa.ForeignKey("cognateset.pk"))
    cognateset = sa.orm.relationship(Cognateset, backref="morphs")
    counterpart_pk = sa.Column(sa.Integer, sa.ForeignKey("morph.pk"))
    counterpart = sa.orm.relationship(Morph, backref="cognates")
    doubt = sa.Column(sa.Boolean, default=False)
    alignment = sa.Column(sa.Unicode)

    contribution_pk = Column(Integer, ForeignKey("contribution.pk"))
    contribution = relationship(Contribution, backref="morphcognates")


@implementer(IStemCognate)
class StemCognate(Base):
    cognateset_pk = sa.Column(sa.Integer, sa.ForeignKey("cognateset.pk"))
    cognateset = sa.orm.relationship(Cognateset, backref="stems")
    counterpart_pk = sa.Column(sa.Integer, sa.ForeignKey("stem.pk"))
    counterpart = sa.orm.relationship(Stem, backref="cognates")
    doubt = sa.Column(sa.Boolean, default=False)
    alignment = sa.Column(sa.Unicode)

    contribution_pk = Column(Integer, ForeignKey("contribution.pk"))
    contribution = relationship(Contribution, backref="stemcognates")


@implementer(ITree)
class Tree(Base, PolymorphicBaseMixin, IdNameDescriptionMixin):
    newick = Column(Unicode)
