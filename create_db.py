from sqlalchemy_config import Base, engine

Base.metadata.create_all(engine)
