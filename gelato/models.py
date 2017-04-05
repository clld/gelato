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
from clld.db.models.common import Language, Value


@implementer(interfaces.ILanguage)
class Measurement(CustomModelMixin, Value):
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    value = Column(Float)


@implementer(interfaces.ILanguage)
class Sample(CustomModelMixin, Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    samplesize = Column(Integer)
    region = Column(Unicode)
    location = Column(Unicode)
    source = Column(Unicode)
    lang_glottocode = Column(Unicode)
    lang_name = Column(Unicode)
