from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Float,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models import IdNameDescriptionMixin
from clld.db.models.common import Language, Value

from gelato.interfaces import ILanguoid


@implementer(interfaces.ILanguage)
class Measurement(CustomModelMixin, Value):
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    value = Column(Float)


@implementer(ILanguoid)
class Languoid(Base, IdNameDescriptionMixin):
    family_id = Column(Unicode)
    family_name = Column(Unicode)


@implementer(interfaces.ILanguage)
class Sample(CustomModelMixin, Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    languoid_pk = Column(Integer, ForeignKey('languoid.pk'))
    languoid = relationship(Languoid, backref='samples')
    samplesize = Column(Integer)
    region = Column(Unicode)
    location = Column(Unicode)
    source = Column(Unicode)

    def __json__(self, req):
        res = super(Sample, self).__json__(req)
        res['languoid'] = self.languoid.__json__(req)
        return res
