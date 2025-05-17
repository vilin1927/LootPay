from aiogram.fsm.state import State, StatesGroup

class QualificationStates(StatesGroup):
    """States for the user qualification process"""
    waiting_for_platform = State()  # Waiting for user to specify their gaming platform
    waiting_for_game_type = State()  # Waiting for user to specify their preferred game type
    waiting_for_payment_preference = State()  # Waiting for user to specify their payment preference 