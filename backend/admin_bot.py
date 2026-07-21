from telegram.ext import (
    Application,
    CallbackQueryHandler
)

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


async def admin_action(update, context):

    query = update.callback_query

    await query.answer()

    data = query.data


    if data.startswith("approve_"):

        session = data.replace("approve_", "")

        await query.message.reply_text(
            f"✅ APPLICATION APPROVED\n\nSession ID: {session}"
        )


    elif data.startswith("reject_"):

        session = data.replace("reject_", "")

        await query.message.reply_text(
            f"❌ APPLICATION REJECTED\n\nSession ID: {session}"
        )



def main():

    app = Application.builder().token(TOKEN).build()


    app.add_handler(
        CallbackQueryHandler(
            admin_action,
            pattern="^(approve_|reject_)"
        )
    )


    print("Admin bot running...")


    app.run_polling()



if __name__ == "__main__":
    main()