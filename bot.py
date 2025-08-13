import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


TOKEN = "8430075192:AAHhGOer9AdJwZV7Hck2ocqfrZl4fzkaodk"
FORM_URL = "https://forms.amocrm.ru/rwmdxmv"
questions = [
    {
        "text": "Какой навык будет нужен 80% профессий в 2030 году?",
        "options": ["Программирование", "Плавание", "Вождение автомобиля"],
        "correct": 0,
        "comment": "📌 Даже врачи и дизайнеры будут работать с кодом или автоматизацией.",
        "image": "https://disk.yandex.ru/i/bSrHqGCaa8Dq7Q"
    },
    {
        "text": "С какого возраста дети могут успешно изучать основы программирования?",
        "options": ["5–6 лет", "10 лет", "15 лет"],
        "correct": 0,
        "comment": "📌 В этом возрасте проще освоить алгоритмическое мышление через игры.",
        "image": "https://sun9-77.userapi.com/s/v1/if2/lkrmlrU-B0DFzPlICkjUyiMX7XwX9SCgeQfYZOYW-L6MuugafIM6DvtWFe563eqRfGAUOWLBMn8-YytggTFzOJWp.jpg?quality=95&as=32x21,48x32,72x48,108x72,160x107,240x160,360x240,480x320,540x360,640x426,720x480,1080x720,1280x853&from=bu&cs=1280x0"
    },
    {
        "text": "Какая из этих игр помогает детям создавать собственные миры?",
        "options": ["Roblox", "Minecraft", "Обе"],
        "correct": 2,
        "comment": "📌 И Roblox, и Minecraft учат проектировать миры и логику событий.",
        "image": "https://avatars.mds.yandex.net/i?id=4e6585a6f3d0a77b2bac1ed96c8a0b93_l-5259124-images-thumbs&n=13"
    },
    {
        "text": "🧩 Логическая задачка: Нужно собрать все монетки за минимальное количество команд. Какое количество команд у Вас получилось? Команды есть: В - Вперед на один шаг, П - поворот на право, Л - Поворот на лево, Ц - повторить N раз (Пример использования команд указан на картинке)",
        "options": ["16 команд", "12 команд", "4 команды"],
        "correct": 2,
        "comment": "📌 Вкладывать можно цикл в цикл. Цх4, Цх3,В, Л",
        "image": "https://disk.yandex.ru/i/Dr4ECoPeBpVFWg"
    },
    {
        "text": "Если ребёнок создаёт мультфильмы или сайты, он тренирует…",
        "options": ["Только компьютерные навыки", "Креативность и проектное мышление", "Память"],
        "correct": 1,
        "comment": "📌 Это помогает в любой сфере жизни.",
        "image": "https://disk.yandex.ru/i/f1BGEbvL1aH95w"
    }
]

user_data = {}

def progress_bar(current, total):
    return "▮" * current + "▯" * (total - current) + f"  {current}/{total}"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user_data[message.from_user.id] = {"score": 0, "q_index": 0}
    await message.answer("Добрый день! 🤖 Попробуйте пройти квиз.")
    await send_question(message.from_user.id)

async def send_question(user_id: int):
    data = user_data[user_id]
    if data["q_index"] < len(questions):
        q = questions[data["q_index"]]

        buttons = [
            [InlineKeyboardButton(text=option, callback_data=f"{data['q_index']}_{i}")]
            for i, option in enumerate(q["options"])
        ]
        kb = InlineKeyboardMarkup(inline_keyboard=buttons)

        await bot.send_photo(
            user_id,
            q["image"],
            caption=f"{progress_bar(data['q_index']+1,len(questions))}\n\n{q['text']}",
            reply_markup=kb
        )
    else:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🚀 Записаться на пробное", url=FORM_URL)]
            ]
        )
        await bot.send_message(
            user_id,
            f"Квиз завершён! Ваш результат: {data['score']}/{len(questions)}. ",
            reply_markup=kb
        )

@dp.callback_query()
async def answer_handler(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    data = user_data.get(user_id)
    if not data:
        await callback.message.answer("Пожалуйста, начните с /start")
        await callback.answer()
        return
    try:
        q_index, a_index = map(int, callback.data.split("_"))
    except Exception:
        await callback.answer("Некорректные данные.")
        return
    if q_index != data["q_index"]:
        await callback.answer("Этот вопрос уже обработан.")
        return
    q = questions[q_index]
    if a_index == q["correct"]:
        data["score"] += 1
        await callback.message.answer("✅ Верно!")
    else:
        await callback.message.answer(f"❌ Неверно! Правильный ответ: {q['options'][q['correct']]}")
    await callback.message.answer(q["comment"])
    data["q_index"] += 1
    await send_question(user_id)
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())