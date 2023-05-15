import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
import speech_recognition as sr
import random
import time
import pyaudio
import pyttsx3


def recognition_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("'recognizer' must be 'Recognizer' instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("'microphone' must be 'Microphone' instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        responce = {
            "success": True,
            "error": None,
            "transcription": None
        }

        try:
            responce["transcription"] = recognizer.recognize_google(audio)
        except sr.RequestError:
            responce["success"] = False
            responce["error"] = "API unavailable"
        except sr.UnknownValueError:
            responce["error"] = "Unable to recognize speech" \

        return  responce

while True:
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    print(rate)
    engine.setProperty('rate', 150)

    volume = engine.getProperty('volume')
    print(volume)
    engine.setProperty('volume', 1)

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    instruction = ("Choice one options:\n"
          "game\n"
          "object detector\n")
    print(instruction)
    engine.say(instruction)
    engine.runAndWait()
    print("Speak!")
    engine.say("Speak!")
    engine.runAndWait()

    for i in range(100):
        guess = recognition_speech_from_mic(recognizer, microphone)
        if guess["transcription"]:
            print('transcription')
            break
        if not guess["success"]:
            print('done')
            break
        print("I didn't catch that. What did you say?\n")
        engine.say("I didn't catch that. What did you say?")
        engine.runAndWait()

    if guess["error"]:
        print("ERROR: {}".format(guess["error"]))
        break
    print("You said: {}".format(guess["transcription"]))
    engine.say("You said: {}".format(guess["transcription"]))
    engine.runAndWait()

    command = guess["transcription"].lower()
    print(command)

    if command == "detector":
        check = True
        video = cv2.VideoCapture(0)
        labels = []
        while check:
            ret, frame = video.read()
            bbox, label, conf = cv.detect_common_objects(frame)
            output_image = draw_bbox(frame, bbox, label, conf)

            cv2.imshow("Object Detection", output_image)

            for item in label:
                if item in labels:
                    pass
                else:
                    labels.append(item)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        i = 0
        new_sentence = []
        for label in labels:
            if i == 0:
                new_sentence.append(f"I found a {label}, ")
            else:
                new_sentence.append(f"and, a {label}")
            i += 1
        message = " ".join(new_sentence)
        print(message)
        engine.say(message)
        engine.runAndWait()
        #cv2.destroyWindow("Object detector")
        check = False



    elif command == "game":
        WORDS = ["apple", "banana", "grape", "orange", "mango", "lemon"]
        NUM_GUESSES = 5
        PROMPT_LIMIT = 8

        word = random.choice(WORDS)

        instruction = (
            "I'm thinking of one of the words:\n"
            "{words}\n"
            "You have {n} tries to guess which one.\n"
        ).format(words=', '.join(WORDS), n=NUM_GUESSES)

        print(instruction)
        engine.say(instruction)
        engine.runAndWait()
        time.sleep(0.5)

        for i in range(NUM_GUESSES):
            for i in range(PROMPT_LIMIT):
                print('Guess {}. Speak!'.format(i + 1))
                engine.say('Guess {}. Speak!'.format(i + 1))
                engine.runAndWait()
                guess = recognition_speech_from_mic(recognizer, microphone)
                if guess["transcription"]:
                    break
                if not guess["success"]:
                    break
                print("I didn't catch that. What did you say?\n")
                engine.say("I didn't catch that. What did you say?")
                engine.runAndWait()

            if guess["error"]:
                print("ERROR: {}".format(guess["error"]))
                break
            print("You said: {}".format(guess["transcription"]))
            engine.say("You said: {}".format(guess["transcription"]))
            engine.runAndWait()

            guess_is_correct = guess["transcription"].lower() == word.lower()
            user_has_more_attempts = i < NUM_GUESSES - 1

            if guess_is_correct:
                print("Correct! You win!".format(word))
                engine.say("Corrent. You win.")
                engine.runAndWait()
                break
            elif user_has_more_attempts:
                print("Incorect. Try again.\n")
                engine.say("Incorect. Try again.")
                engine.runAndWait()
            else:
                print("Sorry, you lose!\nI was thinking of '{}'.".format(word))
                engine.say("Sorry, you lose!\nI was thinking of '{}'.".format(word))
                engine.runAndWait()
                break