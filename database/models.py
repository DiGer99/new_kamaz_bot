from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import BigInteger, String, Boolean, Integer, ForeignKey


engine = create_async_engine(url="sqlite+aiosqlite:///db_users.sqlite3")
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase): pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(50))
    bool_remind = mapped_column(Boolean, default=False)


class Schedule(Base):
    __tablename__ = "schedule"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_schedule: Mapped[str] = mapped_column(String(3990))


async def db_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
