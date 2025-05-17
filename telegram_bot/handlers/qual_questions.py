from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from ..states import QualificationStates

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

# Create keyboard for platform selection
platform_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Steam", callback_data="platform_steam"),
            InlineKeyboardButton(text="Epic Games", callback_data="platform_epic"),
        ],
        [
            InlineKeyboardButton(text="Консоли", callback_data="platform_console"),
            InlineKeyboardButton(text="Не играю", callback_data="platform_none"),
        ]
    ]
)

# Create keyboard for game type selection
game_type_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Онлайн", callback_data="game_online"),
            InlineKeyboardButton(text="Оффлайн", callback_data="game_offline"),
        ],
        [
            InlineKeyboardButton(text="Не играю", callback_data="game_none"),
        ]
    ]
)

# Create keyboard for payment preference
payment_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Платные игры", callback_data="payment_paid"),
            InlineKeyboardButton(text="Бесплатные игры", callback_data="payment_free"),
        ],
        [
            InlineKeyboardButton(text="И те, и другие", callback_data="payment_both"),
        ]
    ]
)

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Handle the /start command and show welcome message"""
    welcome_text = (
        "Привет, это LootPay!\n"
        "Бот для быстрого и надёжного пополнения Steam‑кошелька 🚀\n\n"
        "Легко пополняй Steam за 15 минут с удобной оплатой, честным курсом и без риска быть обманутым ⏱️\n\n"
        "• Минимальная и прозрачная комиссия, без скрытых наценок\n"
        "• Гарантия возврата при сбоях\n"
        "• Поддержка 24/7\n"
        "• Скоро: кэшбэк за повторные пополнения\n\n"
        "Автоматическое зачисление средств на аккаунт от 100 ₽ любыми РФ‑картами или через СБП.\n\n"
        "Поддержка бота — @lootpay_support_bot.\n\n"
        "Наслаждайся играми в Steam вместе с LootPay! 🎮"
    )
    await message.answer(welcome_text, reply_markup=welcome_keyboard)

@router.callback_query(F.data == "start_qualification")
async def start_qualification(callback: CallbackQuery, state: FSMContext):
    """Start the qualification process when user clicks 'Начать пополнение'"""
    await callback.message.edit_text(
        "Где ты играешь чаще всего?",
        reply_markup=platform_keyboard
    )
    await state.set_state(QualificationStates.waiting_for_platform)

@router.callback_query(QualificationStates.waiting_for_platform)
async def process_platform(callback: CallbackQuery, state: FSMContext):
    """Process user's gaming platform response"""
    platform = callback.data.split('_')[1]
    
    if platform != "steam":
        await callback.message.edit_text("Наш бот только для пользователей Steam. Удачи!")
        await state.clear()
        return
    
    await callback.message.edit_text(
        "Какие игры ты предпочитаешь?",
        reply_markup=game_type_keyboard
    )
    await state.set_state(QualificationStates.waiting_for_game_type)

@router.callback_query(QualificationStates.waiting_for_game_type)
async def process_game_type(callback: CallbackQuery, state: FSMContext):
    """Process user's game type preference"""
    await callback.message.edit_text(
        "Ты покупаешь платные игры или играешь только в бесплатные?",
        reply_markup=payment_keyboard
    )
    await state.set_state(QualificationStates.waiting_for_payment_preference)

@router.callback_query(QualificationStates.waiting_for_payment_preference)
async def process_payment_preference(callback: CallbackQuery, state: FSMContext):
    """Process user's payment preference"""
    payment_type = callback.data.split('_')[1]
    
    if payment_type == "free":
        await callback.message.edit_text("Этот бот полезен только тем, кто покупает платные игры. Удачи!")
    else:
        await callback.message.edit_text("Круто, ты наш человек! Скоро начнём.")
    
    await state.clear() 