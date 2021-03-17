from aiogram import Dispatcher

from .superuser import IsSuperUserFilter


def setup_filters(dp: Dispatcher):

    text_handlers = [dp.message_handlers]

    dp.filters_factory.bind(IsSuperUserFilter, event_handlers=text_handlers)
