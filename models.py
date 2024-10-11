import sqlalchemy

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column(
        name="id", type_=sqlalchemy.BigInteger, primary_key=True, autoincrement=True
    ),
    sqlalchemy.Column(
        name="userid",
        type_=sqlalchemy.BigInteger,
        unique=True,
    ),
    sqlalchemy.Column(
        name="first_name", type_=sqlalchemy.String(length=255), index=True
    ),
    sqlalchemy.Column(
        name="last_name", type_=sqlalchemy.String(length=255), index=True, nullable=True
    ),
    sqlalchemy.Column(
        name="username", type_=sqlalchemy.String(length=255), index=True, nullable=True
    ),
    sqlalchemy.Column(name="updated_at", type_=sqlalchemy.DateTime, nullable=True),
    sqlalchemy.Column(name="created_at", type_=sqlalchemy.DateTime),
)

videos = sqlalchemy.Table(
    "videos",
    metadata,
    sqlalchemy.Column(
        name="id", type_=sqlalchemy.BigInteger, primary_key=True, autoincrement=True
    ),
    sqlalchemy.Column(name="video_id", type_=sqlalchemy.BigInteger, unique=True),
    sqlalchemy.Column(name="file_id", type_=sqlalchemy.String(length=255), index=True),
    sqlalchemy.Column(
        name="file_unique_id", type_=sqlalchemy.String(length=255), index=True
    ),
    sqlalchemy.Column(name="updated_at", type_=sqlalchemy.DateTime, nullable=True),
    sqlalchemy.Column(name="created_at", type_=sqlalchemy.DateTime),
)
