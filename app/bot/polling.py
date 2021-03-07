import asyncio

from .base import init_dp, on_startup, on_shutdown



def run_polling():
    dp = init_dp()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(on_startup(dp))
        loop.create_task(dp.start_polling())
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        dp.stop_polling()
        loop.run_until_complete(on_shutdown(dp))
        loop.run_until_complete(dp.bot.session.close())



async def _on_startup_web(app):
    dp = app['dp']
    await on_startup(dp)
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling())


async def _on_shutdown_web(app):
    dp = app['dp']
    dp.stop_polling()
    await dp.bot.session.close()


def setup_web_polling(app):
    dp = init_dp()
    app['dp'] = dp
    app.on_startup.append(_on_startup_web)
    app.on_shutdown.append(_on_shutdown_web)