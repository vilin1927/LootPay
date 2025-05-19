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
            InlineKeyboardButton(text="🎮 Играми", callback_data="q1_games"),
        ],
        [
            InlineKeyboardButton(text="✨ Внутряшками (скины, пьюрочки, кейсы)", callback_data="q1_items"),
        ],
        [
            InlineKeyboardButton(text="🚫 Ничего не беру", callback_data="q1_nothing"),
        ],
        [
            InlineKeyboardButton(text="📴 Не юзаю Стим", callback_data="q1_no_steam"),
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
        "<b>Привет, это LootPay!</b><br>"
        "Бот для быстрого и надёжного пополнения Steam‑кошелька 🚀<br><br>"
        "<i>Всего 5 минут, и баланс в Steam пополнен...</i><br>"
        "А вместо этого — долгие ожидания, скрытые наценки и тревога, что средства не дойдут. Знакомо?<br><br>"
        "✨ <b>С LootPay такого не будет.</b> ✨<br><br>"
        "<b>Пополняй Steam за 15 минут</b><br>"
        "с удобной оплатой, честным курсом и без риска быть обманутым ⏱️<br><br>"
        "🔹 <b>Минимальная и прозрачная комиссия</b> — без скрытых наценок<br>"
        "🔹 <b>Гарантия возврата</b> при сбоях<br>"
        "🔹 <b>Поддержка 24/7</b><br><br>"
        "💳 <i>Автоматическое зачисление от</i> <b>100 ₽</b><br>"
        "<i>— любые РФ‑карты или СБП</i><br><br>"
        "<hr><br>"
        "<b>Как это работает?</b><br><br>"
        "1️⃣ <i>Запусти бота, включи уведомления, введи Steam ID</i><br>"
        "2️⃣ <i>Выбери сумму и оплати через СБП</i><br>"
        "3️⃣ <i>Получи уведомление о зачислении</i> 🎉<br><br>"
        "<hr><br>"
        "<b>Пополняй без риска и обмана — вместе с LootPay!</b> 🎮"
    )
    await message.answer(welcome_text, reply_markup=welcome_keyboard, parse_mode="HTML")

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
        "🎉 <b>Круто, ты прошёл опрос!</b><br><br>"
        "🚀 Спасибо, что поделился своими предпочтениями — это поможет нам делать сервис ещё удобнее.<br><br>"
        "<hr><br>"
        "Введите <b>никнейм</b> своего аккаунта в Steam, который будем пополнять.<br>"
        "❗️ Никнейм ≠ логин. Узнать свой никнейм можно <a href=\"https://telegra.ph/CHasto-zadavaemye-voprosy-pri-pokupke-04-09#%D0%98%D0%BC%D1%8F-%D0%B0%D0%BA%D0%BA%D0%B0%D1%83%D0%BD%D1%82%D0%B0-Steam---%D0%BA%D0%B0%D0%BA-%D0%BD%D0%B0%D0%B9%D1%82%D0%B8-?\">здесь</a>"
    )
    await callback.message.edit_text(
        final_message,
        parse_mode="HTML",
        disable_web_page_preview=True
    )
    await state.clear() 