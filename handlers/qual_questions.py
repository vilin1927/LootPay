from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states import QualificationStates

router = Router()

# Create welcome keyboard
welcome_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Начать пополнение", callback_data="start_qualification"),
        ],
        [
            InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/lootpay_support_bot"),
        ]
    ]
)

# Create keyboard for question 1
q1_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🎮 Игры — покупаю новинки и классику", callback_data="q1_games"),
        ],
        [
            InlineKeyboardButton(text="✨ Внутриигровые штуки — скины, кейсы, боевые пропуски", callback_data="q1_items"),
        ],
        [
            InlineKeyboardButton(text="💸 Другое — что-то ещё, не из этого", callback_data="q1_other"),
        ],
        [
            InlineKeyboardButton(text="📴 Вообще не трачу — просто сижу, не покупаю", callback_data="q1_no_spend"),
        ]
    ]
)

# Create keyboard for question 2
q2_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👍 Да, юзаю", callback_data="q2_yes"),
        ],
        [
            InlineKeyboardButton(text="👎 Да, но забросил(а)", callback_data="q2_past"),
        ],
        [
            InlineKeyboardButton(text="❌ Нет", callback_data="q2_no"),
        ]
    ]
)

# Create keyboard for question 3
q3_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да, ок", callback_data="q3_ok"),
        ],
        [
            InlineKeyboardButton(text="🇬🇧 Я из Британии", callback_data="q3_uk"),
        ],
        [
            InlineKeyboardButton(text="❌ Нет, не в тему", callback_data="q3_no"),
        ]
    ]
)

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Handle the /start command and show welcome message"""
    # Clear any existing state
    await state.clear()
    
    welcome_text = (
        "Привет, это 🎮 LootPay\\!\n"
        "Бот для быстрого и надёжного пополнения Steam кошелька\n\n"
        "Знакомо\\? Было\\?\n"
        "⏳ Всего 5 минут, и баланс в Steam пополнен…\n"
        "😤 А вместо этого — долгие ожидания, скрытые наценки и тревога, что средства не дойдут\\. \n\n"
        "✨ С  LootPay такого не будет ✨\n"
        "⋯⋯⋯⋯⋯⋯⋯⋯\n"
        "Пополняй Steam за 15 минут\n"
        "с удобной оплатой, честным курсом и без риска быть обманутым ⏱️\n\n"
        "🔹 Минимальная и прозрачная комиссия — без скрытых наценок  \n"
        "🔹 Гарантия возврата при сбоях  \n"
        "🔹 Поддержка 24/7\n"
        "⋯⋯⋯⋯⋯⋯⋯⋯\n"
        "💳 Автоматическое зачисление от 100 ₽ — любые РФ\\-карты или СБП\n\n"
        "🔸 Как это работает\\?\n"
        "1️⃣ Запусти бота, включи уведомления, введи Steam ID  \n"
        "2️⃣ Выбери сумму и оплати через СБП  \n"
        "3️⃣ Получи уведомление о зачислении 🎉  \n\n"
        "Пополняй без риска и обмана — вместе с 🎮 LootPay\\!"
    )
    await message.answer(welcome_text, reply_markup=welcome_keyboard, parse_mode="MarkdownV2")

@router.callback_query(F.data == "start_qualification")
async def start_qualification(callback: CallbackQuery, state: FSMContext):
    """Start the qualification process when user clicks 'Начать пополнение'"""
    await callback.message.edit_text(
        "На что чаще всего тратишь деньги в Steam?",
        reply_markup=q1_keyboard
    )
    await state.set_state(QualificationStates.waiting_for_q1)

@router.callback_query(QualificationStates.waiting_for_q1)
async def process_q1(callback: CallbackQuery, state: FSMContext):
    """Process answer to question 1"""
    await callback.message.edit_text(
        "Пробовал(а) другие пополнялки?",
        reply_markup=q2_keyboard
    )
    await state.set_state(QualificationStates.waiting_for_q2)

@router.callback_query(QualificationStates.waiting_for_q2)
async def process_q2(callback: CallbackQuery, state: FSMContext):
    """Process answer to question 2"""
    await callback.message.edit_text(
        "Мы делаем пополнение в USD для всех стран (кроме UK) — гуд?",
        reply_markup=q3_keyboard
    )
    await state.set_state(QualificationStates.waiting_for_q3)

@router.callback_query(QualificationStates.waiting_for_q3)
async def process_q3(callback: CallbackQuery, state: FSMContext):
    """Process answer to question 3 and show final message"""
    final_message = (
        "🎉 Круто, ты прошёл опрос!\n\n"
        "🚀 Спасибо, что поделился своими предпочтениями — это поможет нам делать сервис ещё удобнее.\n\n"
        "---\n\n"
        "Введите **никнейм** своего аккаунта в Steam, который будем пополнять.\n"
        "❗️ Никнейм ≠ логин. Узнать свой никнейм можно [здесь](https://telegra.ph/CHasto-zadavaemye-voprosy-pri-pokupke-04-09#%D0%98%D0%BC%D1%8F-%D0%B0%D0%BA%D0%BA%D0%B0%D1%83%D0%BD%D1%82%D0%B0-Steam---%D0%BA%D0%B0%D0%BA-%D0%BD%D0%B0%D0%B9%D1%82%D0%B8-?)"
    )
    await callback.message.edit_text(
        final_message,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    await state.clear() 