"""
Agendamento da obtenção de dados da Bolsa de valores

"""

from datetime import datetime
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from .data import get_data


def job():
    """
    Tarefa a ser agendada

    """
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
    """
    Iniciação do agendamento

    A cada 5 minutos, enquanto o a Bolsa estiver aberta, a função de obtenção de dados deverá ser executada e as novas cotações deverão ser salvas no banco de dados

    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'interval', minutes=5)
    scheduler.start()
