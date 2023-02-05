
from pydub import AudioSegment, exceptions
import fleep


def audio_converter(audio_file, output_format):
    try:
        with open(audio_file, "rb") as file:
            info = fleep.get(file.read(128))

        if info.type_matches("audio"):
            if not info.extension_matches(output_format):
                if output_format == "aac":
                    print(f"{output_format} is not a supported output format")
                else:
                    try:
                        output = ""
                        for index in range(len(audio_file) - 4):
                            output += audio_file[index]
                        sound = AudioSegment.from_file(audio_file, format=f"{info.extension[0]}")
                        sound.export(out_f=f"{output}.{output_format}", format=output_format)
                        return f"{output}.wav"
                    except exceptions.CouldntEncodeError:
                        print(f"{output_format} is not a supported output format")
            else:
                return f"{audio_file}"
        else:
            print(f"{audio_file} is not an audio file.")
    except FileNotFoundError:
        print(f"File not found: No such file as {audio_file}")
    except AssertionError:
        print(f"Given file must be an audio file.")
