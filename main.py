# from telethon.sync import TelegramClient
# from telethon.sessions import StringSession
#
# # Replace these with your own values
# api_id = 27619703
# api_hash = '729df188d4ad0bc79adc7aa440315d05'
#
# print("Enter your phone number:")
# phone_number = input().strip()
#
# with TelegramClient(StringSession(), api_id, api_hash) as client:
#     client.start(phone=phone_number)
#     session_string = client.session.save()
#     print(f'Session string: {session_string}')


from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from datetime import datetime
import os
import speech_recognition as sr
from pydub import AudioSegment
from keep_alive import keep_alive

api_id = 23564987
api_hash = 'a3a5bf88d985dbf6b39ecb8a8283b33b'
string_session = '1ApWapzMBu4Kp9_ZfxQwxH6-G6bkludaCTH_X7ZDdCY2k8ORH-nGI5Em5j34AHYj_bpcrkUzhuWW_4v8cY15sXZ7JOdF6sLTOd2UsGUeKCAq_gllQEalH3GwrrFRh5oSGulFX-eaAmUUL7XM67sfV0Y41Rc9CQ9UlI8AZeao58PIhKW-yBaAOUYdXQaShShP6-FOuNy9ieh8TrUqmvQssF6xPbTo1qXcQVlmd0AzwF8vOQ2S27dTcQL9ShWjvVck9okzd0YHFF36FewnDZ6yBSV2Q6czJV4vSu7IELof-G0WxZcd83MaayZL0iyTxZGomGXVsboxhGpun-XtZotcfERnrEm8rT-k='

client = TelegramClient(StringSession(string_session), api_id, api_hash)

# Dictionary to keep track of greeted users and their last greeting date
greeted_users = {}

banned_words = ['kot', 'mol', 'garang', 'tom', 'kalanga', 'maymunsan', 'axmoq', 'jinni', 'fuck', 'it', 'eshak', 'ahmoq']

@client.on(events.NewMessage())
async def text_handler(event):
    if event.is_private or event.is_channel:
        user_id = event.sender_id
        current_date = datetime.now().date()

        # Check if the user has been greeted before today
        last_greeted = greeted_users.get(user_id)
        if last_greeted is None or last_greeted < current_date:
            await event.respond('Assalomu alaykum. Men xusanboy tomonidan yasalgan avto javob beraman. Habaringizni yuboring', buttons=[Button.text('salom')])
            greeted_users[user_id] = current_date

        message_text = event.message.message.lower()
        if event.message.text.lower().startswith('/v:( '):
            new_word = event.message.text[len('/v:( '):].strip().lower()
            if new_word:
                if new_word in banned_words:
                    banned_words.remove(new_word)
                    await event.respond(f'Taqiqlangan so\'z "{new_word}" muafaqiyatli o\'chirildi')
                else:
                    await event.respond(f'Tanlangan so\'z "{new_word}" yo\'q')
            else:
                await event.respond('O\'chirish uchun so\'z kiritilmadi')

        if any(banned_word in message_text for banned_word in banned_words):
            await event.respond('Yomon so\'z gapirmasdan gaplashaylik, iltimos')

        if event.message.text.lower().startswith('/v:) '):
            new_word = event.message.text[len('/v:) '):].strip().lower()
            if new_word and new_word not in banned_words:
                banned_words.append(new_word)
                await event.respond(f'Taqiqlangan so\'z "{new_word}" muafiqiyatli qoshildi')
            elif new_word in banned_words:
                await event.respond(f'Tanlangan so\'z "{new_word}" allaqachon yozilgan')
            else:
                await event.respond('Qo\'shishga berilgan so\'z yo\'q')

def convert_ogg_to_wav(file_path):
    wav_path = file_path.replace('.ogg', '.wav')
    audio = AudioSegment.from_ogg(file_path)
    audio.export(wav_path, format='wav')
    return wav_path

# Speech Recognition function
def recognize_speech(file_path):
    recognizer = sr.Recognizer()
    wav_path = convert_ogg_to_wav(file_path)
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)
        try:
            # Using Google Web Speech API (free but limited)
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand the audio."
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

# Event handler for new voice messages
@client.on(events.NewMessage(func=lambda e: e.message.voice))
async def voice_handler(event):
    # Download the voice message
    voice_message_path = await event.download_media()
    # Recognize the speech from the voice message
    text = recognize_speech(voice_message_path)
    # Send the recognized text back to the user
    await event.reply(text)
    # Clean up the downloaded files
    os.remove(voice_message_path)
    wav_path = voice_message_path.replace('.ogg', '.wav')
    if os.path.exists(wav_path):
        os.remove(wav_path)

with client:
    client.start()  # Start the client without requiring user input
    keep_alive()
    print("Client is running...")
    client.run_until_disconnected()
