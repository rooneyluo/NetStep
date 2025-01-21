from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from db.config import DB_CONFIG

DATABASE_URL = f"postgresql+asyncpg://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# SQLAlchemy Base and Engine
Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=True, pool_size=5, max_overflow=10)

# create a session class
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Dependency
async def get_db():
    async with SessionLocal() as session:
        yield session
