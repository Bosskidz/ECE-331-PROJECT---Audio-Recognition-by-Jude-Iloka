import speech_recognition as sr
import audio_converter as ac
import guessing_game as gg

r = sr.Recognizer()
mic = sr.Microphone()


def transcribe_audio_file(audio_file):
    try:
        audio_name = ac.audio_converter(audio_file=audio_file, output_format="wav")
        audio_source = sr.AudioFile(audio_name)
        with audio_source as source:
            r.adjust_for_ambient_noise(source)
            audio = r.record(source)

        transcribed_text = r.recognize_google(audio_data=audio, language="en-EN", show_all=True)["alternative"][0][
            "transcript"]
        return transcribed_text
    except FileNotFoundError:
        print(f"File not found: No such file as {audio_file}")
    except sr.RequestError:
        print("API unavailable")
    except AssertionError:
        print(f"Given file must be an audio file.")


def transcribe_from_microphone():
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        transcribed_text = r.recognize_google(audio_data=audio, language="en-EN", show_all=True)["alternative"][0][
            "transcript"]
        return transcribed_text
    except sr.RequestError:
        print("API unavailable")
    except sr.UnknownValueError:
        print("Unable to recognize speech")
    except TypeError:
        print("Unable to recognize speech")


print("\nWelcome to JudeAudioTool\n")

mode = ""
while mode not in ["1", "2", "3", "4"]:
    mode = input("Choose what mode you want to use.\nEnter:\n1 to convert the format of audio files\n"
                 "2 to transcribe an audio file\n3 to transcribe from microphone\n4 to play the Guessing Game\n>>> ")

if mode == "1":
    audio_file = input("Enter the name of the audio file that you want to convert its format:\n>>> ")
    output_format = input("Enter the output format you want to convert the audio file into:\n>>> ")
    ac.audio_converter(audio_file=audio_file, output_format=output_format)
elif mode == "2":
    audio_file = input("Enter the name of the audio file that you want to transcribe:\n>>> ")
    transcribed_text = transcribe_audio_file(audio_file)
    if transcribed_text is not None:
        print(f"You said:\n{transcribed_text}")
elif mode == "3":
    print("Microphone activated, you can speak now")
    transcribed_text = transcribe_from_microphone()
    if transcribed_text is not None:
        print(f"You said:\n{transcribed_text}")
elif mode == "4":
    gg.guessing_game(r, mic)

print("\nThank you for using JudeAudioTool!")
