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
from keep_alive import keep_alive


# api_id = 23564987
api_id = 27619703
# api_hash = 'a3a5bf88d985dbf6b39ecb8a8283b33b'
api_hash = '729df188d4ad0bc79adc7aa440315d05'
# string_session = '1ApWapzMBu4Kp9_ZfxQwxH6-G6bkludaCTH_X7ZDdCY2k8ORH-nGI5Em5j34AHYj_bpcrkUzhuWW_4v8cY15sXZ7JOdF6sLTOd2UsGUeKCAq_gllQEalH3GwrrFRh5oSGulFX-eaAmUUL7XM67sfV0Y41Rc9CQ9UlI8AZeao58PIhKW-yBaAOUYdXQaShShP6-FOuNy9ieh8TrUqmvQssF6xPbTo1qXcQVlmd0AzwF8vOQ2S27dTcQL9ShWjvVck9okzd0YHFF36FewnDZ6yBSV2Q6czJV4vSu7IELof-G0WxZcd83MaayZL0iyTxZGomGXVsboxhGpun-XtZotcfERnrEm8rT-k='  # Replace with your actual string session
string_session = '1BJWap1wBuzRDD-Sz35O0Z0QOpbHZ_-I8isXJIgtrE9DasnvLBs-YacaLHEMmtjqlmuVSK2pEQ7WdSKIRVEGB9O1w7UP9D_OwJGhosUBrzv2FpcbGt9KTZDo7mLAWtaQmwL4fa7aeIJw3N622-dH3MWM4QmyPnm7-WJgRyuPeAGPdbHU51rqi4B9IP7J2Lmn8aa8aat6miTPHbkI8h6Idyfgomtu_0MJxO_Cfjf5ku97p-OD2LrcSjeo4nb-rWsds74_oLhXKoN0aeZD07ssuVqoEXYej0VBK4TTKofTX8o3CvD3xYpM1rOQdp52kqL_t-XS8FjXQl1yLZjp_84MSN70srD3it7E='

client = TelegramClient(StringSession(string_session), api_id, api_hash)

# Dictionary to keep track of greeted users and their last greeting date
greeted_users = {}

banned_words = ['kot', 'mol', 'garang', 'tom', 'kalanga', 'kt', 'axmoq', 'jinni', 'fuck','it','eshak','ahmoq']

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.is_private:
        user_id = event.sender_id
        current_date = datetime.now().date()


        # Check if the user has been greeted before today
        last_greeted = greeted_users.get(user_id)
        if last_greeted is None or last_greeted < current_date:
            await event.respond('Assalomu alaykum. Men xusanboy tomonidan yasalgan avto javob beraman. Habaringizni yuboring', buttons=[Button.text('salom')])
            greeted_users[user_id] = current_date

        message_text = event.message.message.lower()
        if any(banned_word in message_text for banned_word in banned_words):
            await event.respond('Yomon soz gapirmasdan gaplashelik iltimos')

        if event.message.text.lower().startswith('/yomon_soz_qoshish '):
            new_word = event.message.text[len('/yomon_soz_qoshish '):].strip().lower()
            if new_word and new_word not in banned_words:
                banned_words.append(new_word)
                await event.respond(f'Taqiqlangan soz  "{new_word}" muafiqiyatli qoshildi')
            elif new_word in banned_words:
                await event.respond(f'Tanlangan soz "{new_word}" allaqachon yozilgan')
            else:
                await event.respond('qoshishga berilgan soz yo\'q')


with client:
    keep_alive()
    print("Client is running...")
    client.run_until_disconnected()
