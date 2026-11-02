import logging
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# تفعيل سجلات تتبع الأخطاء
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# ضع توكن البوت الذي حصلت عليه من BotFather هنا
TOKEN = "YOUR_BOT_TOKEN_HERE"

# رابط موقعك المرفوع على الإنترنت (أو رابط GitHub Pages / Render)
WEBAPP_URL = "https://your-domain.com/index.html"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # إنشاء زر يفتح التطبيق المصغر الملون بداخل تليجرام مباشرة
    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 فتح شمس تريدر (الأزرار الملونة والشارت)", 
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ],
        [
            InlineKeyboardButton("⚙️ اختيار الوسيط (Quotex)", callback_data="broker"),
            InlineKeyboardButton("📡 حالة الربط", callback_data="status")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🌸 **أهلاً بك في منصة SHAMS NEXUS PRO للتحليل وقراءة الشارت**\n\n"
        "اضغطي على الزر الملون أدناه لفتح لوحة التحكم التفاعلية والأزرار الملونة بالأخضر والأحمر والشارت الحقيقي!",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# استقبال البيانات القادمة من الـ WebApp عند الضغط على إرسال للقناة
async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.effective_message.web_app_data.data
    await update.message.reply_text(f"📥 **تم استقبال بيانات الإشارة من التطبيق المصغر:**\n`{data}`", parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))

    print("البوت يعمل وجاهز لتشغيل الـ Web App...")
    
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    app.run_polling()

if __name__ == "__main__":
    main()