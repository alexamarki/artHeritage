import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session as sn

SqlAlchemyBase = orm.declarative_base()

__factory = None


def global_init(db):
    global __factory

    if __factory:
        return
    if not db.strip():
        raise Exception("Database file missing :/")

    sqlEngCreator = f'sqlite:///{db.strip()}?check_same_thread=False'
    eng = sa.create_engine(sqlEngCreator, echo=False)
    __factory = orm.sessionmaker(bind=eng)

    from . import __all_models
    SqlAlchemyBase.metadata.create_all(bind=eng)


def create_session() -> sn:
    global __factory
    return __factory()
