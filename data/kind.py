import sqlalchemy
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from sqlalchemy_serializer import SerializerMixin
import sqlalchemy.ext.declarative as dec

from .db_session import SqlAlchemyBase
   

class Kind(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'kinds'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, 
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    works = orm.relation("Works", back_populates='kind')