FROM python:3
RUN pip install pyTelegramBotAPI
COPY ./bot.py /bot.py
CMD python /bot.py
