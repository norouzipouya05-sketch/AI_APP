from app.db.session import async_session_maker

async def get_db():
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception as er:
            await session.rollback()
            raise
        finally:
            await session.close()