from aiogram.fsm.state import State, StatesGroup

class QualificationStates(StatesGroup):
    """States for the user qualification process"""
    waiting_for_q1 = State()  # Waiting for answer about Steam spending
    waiting_for_q2 = State()  # Waiting for answer about other services
    waiting_for_q3 = State()  # Waiting for answer about USD payments 