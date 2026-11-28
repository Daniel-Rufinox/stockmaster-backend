
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Usa PostgreSQL quando DATABASE_URL estiver configurada.
# Caso contrário, mantém SQLite para desenvolvimento local.

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./stockmaster.db")

# Compatibilidade com URLs antigas do PostgreSQL.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql://",
        1
    )

# Configurações específicas de cada banco.
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}

    # Exige conexão SSL com o PostgreSQL.
    if "sslmode=" not in DATABASE_URL:
        separador = "&" if "?" in DATABASE_URL else "?"
        DATABASE_URL += separador + "sslmode=require"

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
