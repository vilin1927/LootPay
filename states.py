from aiogram.fsm.state import State, StatesGroup

class QualificationStates(StatesGroup):
    waiting_for_q1 = State()
    waiting_for_q2 = State()
    waiting_for_q3 = State() 