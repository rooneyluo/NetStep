import asyncio
from db.session import engine, Base

async def create_tables():
    async with engine.begin() as conn:
        print("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully!")

async def drop_tables():
    async with engine.begin() as conn:
        print("Dropping tables...")
        await conn.run_sync(Base.metadata.drop_all)
        print("Tables dropped successfully!")

if __name__ == "__main__":
    asyncio.run(create_tables())
