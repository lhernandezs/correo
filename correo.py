import smtplib
import os.path
import json

from email.message          import EmailMessage
from email.headerregistry   import Address
from modelo                 import Instructor
from jinja2                 import (Environment, select_autoescape, FileSystemLoader,)

class Correo:

    # variable de entorno para la API de jinja2
    ENV = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape())

    # constructor de la clase - cada correo tiene un email que recibe, un servidor que recibe, un nombre del que recibe y el modelo con los datos
    def __init__(self, emaRec, serRec, namRec, modelo):

        # lee desde un archivo json los datos del servidor de correo que remite
        with open(os.path.join('json', 'sercorreo.json'), 'r') as conex:
            arc = json.load(conex)
            conex.close()

        self._emaEnv = arc["emailRemitente"] 
        self._serEnv = arc["servidorRemitente"] 
        self._namEnv = arc["nombreRemitente"] 

        self._asunto = arc["asunto"] 
        self._templa = arc["template"]

        self._emaRec        = emaRec
        self._serRec        = serRec
        self._namRec        = namRec

        self._modelo        = modelo

    # renderiza la plantilla -template- con los datos -modelo-
    def render_html(self, modelo: Instructor):
        template_result = Correo.ENV.get_template(self._templa)
        template_result = template_result.render(user=modelo)
        return template_result

    # metodo que envia el email
    def send_email(self, email_message: EmailMessage):
        remitente = self._emaEnv + "@" + self._serEnv
        destinatarios = self._emaRec + "@" + self._serRec
        smtp = smtplib.SMTP_SSL("smtp.gmail.com")
        # smtp.login(remitente, "ghpflywujadbastq") # para que gmail pueda enviar correos desde un aplicativo externo se requiere una clave de 16 caracteres
        smtp.login(remitente, "bihnlljggmslwxvn") # para enviar correo desde la cuenta coordinacionvirtualcsf@gmail.com
        smtp.sendmail(remitente, destinatarios, email_message.as_string())
        smtp.quit()

    # construye el cuerpo del email con los datos del modelo
    def build_email(self, user: Instructor):
        html_data: str = self.render_html(user)
        email_message               = EmailMessage()
        email_message["Subject"]    = self._asunto
        email_message["From"]       = Address(username=self._emaEnv, domain=self._serEnv, display_name=self._namEnv)
        email_message["To"]         = Address(username=self._emaRec, domain=self._serRec, display_name=self._namRec)
        email_message.add_alternative(html_data, subtype="html")
        self.send_email(email_message=email_message)