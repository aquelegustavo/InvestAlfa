from datetime import datetime
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from .data import get_data


def job():
    timezone = pytz.timezone("America/Sao_Paulo")
    now = datetime.now().astimezone(timezone)
    day = now.today().weekday()

    # Apenas dias de semana
    if not day in (5, 6):
        # Apenas no período em que a Bolsa de Valores está aberta
        if now.hour >= 10 and now.hour <= 18:
            print("Obtendo dados da bolsa...")
            get_data()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'interval', minutes=5)
    scheduler.start()
