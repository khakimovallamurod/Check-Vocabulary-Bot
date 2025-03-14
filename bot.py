from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,CallbackQueryHandler
from config import get_token
import handlers


def main():
    TOKEN = get_token()

    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', handlers.start))
    dp.add_handler(MessageHandler(Filters.text('Bosh sahifa 🏠'), handlers.start))
    dp.add_handler(MessageHandler(Filters.text('🔓 Open Test Start'), handlers.models))
    dp.add_handler(MessageHandler(Filters.text('🗒 View All Tests'), handlers.view_all_vocabulry))
    dp.add_handler(MessageHandler(Filters.text("☎️Contact"), handlers.contact))
    
    dp.add_handler(CallbackQueryHandler(handlers.one_model, pattern="model:"))
    dp.add_handler(CallbackQueryHandler(handlers.view_one_list_get, pattern="view:"))
    dp.add_handler(CallbackQueryHandler(handlers.answer_callback, pattern='answer:'))
    dp.add_handler(CallbackQueryHandler(handlers.one_model_yopiqtest, pattern="model_yopiq:"))
    dp.add_handler(MessageHandler(Filters.text, handlers.answer_image))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()