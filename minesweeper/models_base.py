from sqlalchemy import (
    Column,
    ForeignKey,
    )
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


def foreign_key_column(name, type_, target, nullable=False):
    """ Creates a ForeignKey column. """
    fk = ForeignKey(target)
    if name:
        return Column(name, type_, fk, nullable=nullable)
    return Column(type_, fk, nullable=nullable)
