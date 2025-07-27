# Create your states in this folder.
from telebot.handler_backends import State, StatesGroup
from catalogues.button_texts import SolutionButtons

class ComplainStates(StatesGroup):
    """
    Group of states for registering
    """
    dialogue_process_state = State()
    dialogue_process_state.name = 'dialogue_process_state'

    suggestion_state = State()
    suggestion_state.name = "suggestion_state"

    issue_description_state = State()
    issue_description_state.name = 'issue_description_state'

    full_refund_state = State()
    full_refund_state.name = SolutionButtons.REFUND_BTN

    part_refund_state = State()
    part_refund_state.name = SolutionButtons.PARTLY_REFUND_BTN

    contact_staff_state = State()
    contact_staff_state.name = SolutionButtons.STAFF_CONTACT_BTN