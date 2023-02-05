
import speech_recognition as sr
import random
import time


def recognize_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError(f"{recognizer} must be Recognizer instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError(f"{microphone} must be Microphone instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio_data=audio, language="en-EN", show_all=True)\
        ["alternative"][0]["transcript"]
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"
    except TypeError:
        response["error"] = "Unable to recognize speech"
    return response


WORDS = ["apple", "banana", "grape", "orange", "mango", "lemon"]
NUM_GUESSES = 3
PROMPT_LIMIT = 5

recognizer = sr.Recognizer()
microphone = sr.Microphone()

word = random.choice(WORDS)

instructions = f"I'm thinking of one of these words:\n{WORDS}\n"f"You have {NUM_GUESSES} tries to guess which one."


def guessing_game(recognizer, microphone):
    print(instructions)
    time.sleep(3)

    for i in range(NUM_GUESSES):
        for j in range(PROMPT_LIMIT):
            print(f"Guess {i + 1}. Speak!")
            guess = recognize_speech_from_mic(recognizer, microphone)
            if guess["transcription"] and guess["success"] and guess["error"] is None:
                print(f'You said: {guess["transcription"]}')
                break
            elif not guess["success"]:
                break
            print("I didn't catch that. What did you say?")

        if guess["error"]:
            print(f'ERROR: {guess["error"]}')
            break
        guess_is_correct = guess["transcription"].lower() == word.lower()
        user_has_more_attempts = i < NUM_GUESSES - 1

        if guess_is_correct:
            print("Correct! You win!")
            break
        elif user_has_more_attempts:
            print("Incorrect. Try again.\n")
        else:
            print(f"Sorry, you lose!\nI was thinking of {word}.")
            break




