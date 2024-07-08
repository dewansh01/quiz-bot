
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to Django session.
    '''
    # Validate the answer
    if not isinstance(answer, str) or not answer.strip():
        return False, "Invalid answer. Please provide a non-empty string."

    # Store the answer in the session
    if 'answers' not in session:
        session['answers'] = {}
    session['answers'][str(current_question_id)] = answer
    session.modified = True

    return True, ""



def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''

    return "dummy question", -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    if 'answers' not in session:
        return "No answers recorded."

    user_answers = session['answers']
    total_questions = len(PYTHON_QUESTION_LIST)
    correct_answers = 0

    for index, question in enumerate(PYTHON_QUESTION_LIST):
        question_id = str(index + 1)  # Assuming question IDs are 1-based indices
        correct_answer = question['answer']
        user_answer = user_answers.get(question_id, "")

        if user_answer.strip().lower() == correct_answer.strip().lower():
            correct_answers += 1

    score = correct_answers / total_questions * 100
    result_message = f"You answered {correct_answers} out of {total_questions} questions correctly. Your score is {score:.2f}%."

    return result_message
