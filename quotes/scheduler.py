from datetime import datetime
from .data import get_data
from apscheduler.schedulers.background import BackgroundScheduler


def job():
    now = datetime.now().hour
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
