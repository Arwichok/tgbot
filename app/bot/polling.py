import asyncio

from .base import init_dp, on_shutdown, on_startup


def run_polling():
    dp = init_dp()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(_on_startup_polling(dp))
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        loop.run_until_complete(_on_shutdown_polling(dp))


async def _on_startup_polling(dp):
    await on_startup(dp)
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling())


async def _on_shutdown_polling(dp):
    dp.stop_polling()
    await on_shutdown(dp)
    await dp.bot.session.close()


def setup_web_polling(app):
    dp = init_dp()

    async def _up(_): await _on_startup_polling(dp)
    async def _down(_): await _on_shutdown_polling(dp)

    app.on_startup.append(_up)
    app.on_shutdown.append(_down)
