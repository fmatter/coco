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
from coco.interfaces import ICognateset, IMorphCognate, IFormCognate, IStemCognate
import sqlalchemy as sa
from clld.db.models.common import Contribution


# -----------------------------------------------------------------------------
# specialized common mapper classes
# -----------------------------------------------------------------------------


@implementer(ICognateset)
class Cognateset(Base, PolymorphicBaseMixin, IdNameDescriptionMixin):
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
