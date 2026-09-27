import logging
import json
import os
from pathlib import Path
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Persistent referral database
DB_FILE = "referral_db.json"

def load_referral_db():
    if Path(DB_FILE).exists():
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_referral_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

referral_db = load_referral_db()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "User"

    if context.args:
        referrer_id = context.args[0]
        if referrer_id != str(user_id):
            referral_db[referrer_id] = referral_db.get(referrer_id, 0) + 1
            save_referral_db(referral_db)
            logging.info(f"User {user_id} was referred by {referrer_id}")

    bot_username = (await context.bot.get_me()).username
    personal_ref_link = f"https://t.me/{bot_username}?start={user_id}"
    user_ref_count = referral_db.get(str(user_id), 0)

    welcome_text = (
        f"👋 Welcome, @{username}!\n\n"
        f"Paste any token link to analyze project viability.\n\n"
        f"🔗 *Your Referral Link:* `{personal_ref_link}`\n"
        f"👥 *Total Referrals:* {user_ref_count}"
    )

    await update.message.reply_text(welcome_text, parse_mode="Markdown")


def analyze_token_viability(text_input: str) -> str:
    if "http://" not in text_input and "https://" not in text_input:
        return "⚠️ Please paste a valid link for analysis."

    analysis_report = (
        "🔍 *Project Viability Analysis*\n"
        "-----------------------------------\n"
        f"📌 *Target Input:* `{text_input[:40]}...`\n"
        "💧 *Liquidity Check:* Pass (Mock Data)\n"
        "🛡️ *Scam/Honeypot Risk:* Low (Mock Check)\n"
        "📊 *Viability Score:* 8/10\n\n"
        "💡 *Note:* Always DYOR before committing funds."
    )
    
    return analysis_report


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    report = analyze_token_viability(user_message)
    await update.message.reply_text(report, parse_mode="Markdown")


def main():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable not set")
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
