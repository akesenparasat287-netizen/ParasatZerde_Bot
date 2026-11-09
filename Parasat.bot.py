import os
import telebot

# Боттың токені
TOKEN = '9127120988:AAEpPRMrPYDk3yI1Ij9shiVxr3S3IFAbq8g'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  welcome_text = (
      'Саламатсыз ба! «ParasatZerde_bot» қызметіне қош келдіңіз.\n\n'
      'Бұл бот EAN-13 штрих-кодын модулярлық арифметика (Mod 10 алгоритмі)'
      ' арқылы тексеріп, отандық және жергілікті тауарлардың'
      ' түпнұсқалығын анықтауға көмектеседі.\n\n'
      'Тексеру үшін 13 цифрдан тұратын штрих-коды жіберіңіз!'
  )
  bot.reply_to(message, welcome_text)


@bot.message_handler(func=lambda message: True)
def check_barcode(message):
  code = message.text.strip()

  # 13 цифрдан тұратынын және тек сан екенін тексеру
  if len(code) != 13 or not code.isdigit():
    bot.reply_to(
        message,
        '❌ Қате формат! Дұрыс 13 цифрдан тұратын штрих-кодты енгізіңіз.',
    )
    return

  try:
    digits = [int(x) for x in code]

    # Mod 10 алгоритмі бойынша есептеу
    even_sum = sum(digits[1:12:2])
    odd_sum = sum(digits[0:11:2])

    total = (even_sum * 3) + odd_sum
    remainder = total % 10

    calc_check = 0 if remainder == 0 else 10 - remainder
    actual_check = digits[12]

    country_code = code[:3]

    # Нәтижені шығару
    if calc_check == actual_check:
      res = (
          f'✅ **Штрих-код ДҰРЫС! Өнім түпнұсқа.**\n\n'
          f'📌 **Мемлекет/Өңір коды:** {country_code} (Қазақстан/Отандық)\n'
          f'🔢 **Бақылау цифры:** {actual_check} (Математикалық есептеумен'
          ' сәйкес)'
      )
    else:
      res = (
          f'❌ **Ескерту! Штрих-код ҚАТЕ немесе ФАЛЬСИФИКАЦИЯЛАНҒАН!**\n\n'
          f'🔢 **Есептелген мән:** {calc_check}\n'
          f'⚠️ **Кодтағы цифр:** {actual_check}\n'
          f'Бұл тауардың жасанды болуы мүмкін екенін көрсетеді.'
      )

    bot.reply_to(message, res, parse_mode='Markdown')

  except Exception as e:
    bot.reply_to(
        message, '⚠️ Есептеу барысында қате орын алды. Қайта көріңіз.'
    )


# Ботты іске қосу
if __name__ == '__main__':
  print('Бот іске қосылды...')
  bot.polling(none_stop=True)
