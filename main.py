import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from gtts import gTTS
import os
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

class Language(StatesGroup):
    choosing_language = State()

user_languages = {}

available_languages = ['en', 'de', 'ru']
language_names = {'en': 'English', 'de': 'Deutsch', 'ru': 'Русский'}

def get_user_language(user_id):
    return user_languages.get(user_id, 'en')

translations = {
    'en': {
        'start_message': "Hello! Use /language to select a language.",
        'language_selection': "Please, choose the language / Пожалуйста, выберите язык:",
        'language_set': "Language set to {}.",
        'invalid_language': "Invalid language selection. Please choose again.",
        'send_text': "Send me the text and I will voice it into an audio file.",
        'no_text': "Please send me the text.",
        'tts_error': "Sorry, I can't process this text. Please try a different text or language.",
        'audio_error': "Sorry, there was an error sending the audio file."
    },
    'de': {
        'start_message': "Hallo! Verwenden Sie /language, um eine Sprache auszuwählen.",
        'language_selection': "Bitte wählen Sie die Sprache / Пожалуйста, выберите язык:",
        'language_set': "Sprache wurde auf {} eingestellt.",
        'invalid_language': "Ungültige Sprachauswahl. Bitte wählen Sie erneut.",
        'send_text': "Senden Sie mir den Text und ich werde ihn in eine Audiodatei umwandeln.",
        'no_text': "Bitte senden Sie mir den Text.",
        'tts_error': "Entschuldigung, ich kann diesen Text nicht verarbeiten. Bitte versuchen Sie einen anderen Text oder eine andere Sprache.",
        'audio_error': "Entschuldigung, beim Senden der Audiodatei ist ein Fehler aufgetreten."
    },
    'ru': {
        'start_message': "Привет! Используйте /language для выбора языка.",
        'language_selection': "Пожалуйста, выберите язык:",
        'language_set': "Язык установлен на {}.",
        'invalid_language': "Неверный выбор языка. Пожалуйста, выберите еще раз.",
        'send_text': "Отправьте мне текст, и я озвучу его в аудиофайл.",
        'no_text': "Пожалуйста, отправьте мне текст.",
        'tts_error': "Извините, я не могу обработать этот текст. Попробуйте другой текст или язык.",
        'audio_error': "Извините, произошла ошибка при отправке аудиофайла."
    }
}

@dp.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_language = get_user_language(user_id)
    if user_id not in user_languages:
        user_languages[user_id] = 'en'

    await message.answer(translations[user_language]['start_message'])

@dp.message(Command("language"))
async def language_command_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_language = get_user_language(user_id)
    await state.set_state(Language.choosing_language)

    buttons = [
        [types.InlineKeyboardButton(text=lang_name, callback_data=f"lang_{lang_code}")]
        for lang_code, lang_name in language_names.items()
    ]
    keyboard_inline = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer(translations[user_language]['language_selection'], reply_markup=keyboard_inline)

@dp.callback_query(Language.choosing_language)
async def process_language_selection(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    selected_language = callback_query.data.split('_')[1]

    if selected_language in available_languages:
        user_languages[user_id] = selected_language
        await callback_query.message.edit_text(text=translations[selected_language]['language_set'].format(language_names[selected_language]))
        await state.clear()
        await bot.send_message(user_id, translations[selected_language]['send_text'])

    else:
        await callback_query.message.answer(translations[user_language]['invalid_language'])
        return
    await state.clear()
    await callback_query.answer()

@dp.message()
async def text_to_speech(message: types.Message):
    user_id = message.from_user.id
    user_language = get_user_language(user_id)
    text = message.text

    if not text:
        await message.answer(translations[user_language]['no_text'])
        return

    try:
        tts = gTTS(text=text, lang=user_language)
        file_path = "output.mp3"
        tts.save(file_path)
    except ValueError as e:
        print(f"Error creating TTS: {e}")
        await message.answer(translations[user_language]['tts_error'])
        return

    try:
        with open(file_path, "rb") as audio_file:
            await message.answer_voice(voice=types.BufferedInputFile(audio_file.read(), filename="output.mp3"))
    except Exception as e:
        print(f"Error sending audio: {e}")
        await message.answer(translations[user_language]['audio_error'])
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
