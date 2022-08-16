"""
Enviar email ao usuário

"""
import base64
from io import BytesIO
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.template import Context
from django.template.loader import get_template
from rest_framework import status
from matplotlib import pyplot
from ..quotes.models import Quote
from ..monitoring.models import Monitoring
from ..users.models import CustomUser
from ..companies.models import Company


def create_chart(company_code):
    """ 
    Gerar gráfico das últimas cotações da empresa

    Função gera uma imagem contendo o gráfico com as cotações armazenadas da empresa que está sendo monitorada.

    Arguments:
        company_code: Código da empresa

    """
    pyplot.switch_backend('AGG')
    pyplot.figure(figsize=(10, 4))

    data = Quote.objects.filter(parent_company__code=company_code)

    x = list(map(lambda quote: quote.timestamp, data))
    y = list(map(lambda quote: quote.value, data))

    pyplot.plot(x, y)

    buffer = BytesIO()
    pyplot.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

    return graph


def get_context(uid, monitoring_id):
    """
    Obtenção do contexto do template

    Arguments:
        uid: Id do usuário
        monitoring_id: Id do monitoramento

    Return: Contexto do template

    """
    monitoring = get_object_or_404(
        Monitoring, pk=monitoring_id)

    user = get_object_or_404(
        CustomUser, uid=uid)

    if monitoring.user != user:
        return HttpResponse({"Não autorizado"}, status=status.HTTP_403_FORBIDDEN)

    user_monitoring = Monitoring.objects.filter(user__uid=uid)

    print(user_monitoring)

    company = get_object_or_404(
        Company, code=monitoring.company.code)

    if company.last_quote < monitoring.tunnel_min:
        company.action = "down"

    elif company.last_quote > monitoring.tunnel_max:
        company.action = "up"

    return {
        'user': user,
        'chart': create_chart(monitoring.company.code),
        'company': company,
        'monitoring': monitoring,
        'user_monitoring': user_monitoring
    }


def send_email(uid, monitoring_id):
    """
    Envio de email ao usuário

    Função envia email para o usuário de acordo com as configurações da aplicação.

    Arguments:
        uid: Id do usuário
        monitoring_id: Id do monitoramento

    """
    context = get_context(uid, monitoring_id)

    html = get_template('email.html')
    if context['company'].last_quote < context['monitoring'].tunnel_min:
        action = "cairam"
        r = "Recomendamos a compra de ativos."

    else:
        action = "subiram"
        r = "Recomendamos a venda de ativos."

    subject = f"As ações da(o) {context['company'].name} {action}!"
    text_content = f"{subject} {r}"

    html_content = html.render(context)
    msg = EmailMultiAlternatives(
        subject,
        text_content,
        "inoamecontrata@gmail.com",
        [context["user"].email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
