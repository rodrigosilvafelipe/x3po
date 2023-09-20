import smtplib
import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def enviarEmail(config):
    try:
        de = "escritax+x3po@escritax.com.br"
        para = "x3po@escritax.com.br"
        assunto = f"X3PO - {config['assunto']}"
        mensagem = config['mensagem']

        # Configurações do servidor SMTP do Zoho
        servidor = smtplib.SMTP("smtp.zoho.com", 587)
        servidor.starttls()
        servidor.login("escritax@escritax.com.br", "zUqiKRvpBKvw")

        # Cria o corpo do e-mail
        msg = MIMEMultipart()
        msg["Subject"] = assunto
        msg["From"] = de
        msg["To"] = para

        # Adiciona o corpo do e-mail como texto HTML
        corpo = MIMEText(mensagem, "html")
        msg.attach(corpo)

        # Anexa o arquivo PDF
        if "pdf64" in config:

            # pdf_base64 = config["pdf64"]
            # pdf_anexo = MIMEApplication(base64.b64decode(pdf_base64), Name=config["nomePdf64"])
            # pdf_anexo["Content-Disposition"] = f'attachment; filename="{config["nomePdf64"]}"'
            # msg.attach(pdf_anexo)

            # Abre o arquivo PDF em modo binário
            with open(config["pdf64"], 'rb') as pdf_file:
                # Lê o conteúdo do arquivo PDF
                pdf_contents = pdf_file.read()

            # Cria o objeto MIME para o arquivo PDF
            pdf_anexo = MIMEApplication(pdf_contents, Name=config["nomeDocumento"])
            pdf_anexo["Content-Disposition"] = f'attachment; filename="{config["nomeDocumento"]}"'

            # Anexa o arquivo PDF à mensagem de e-mail (substitua msg pelo objeto MIMEMultipart que você está usando)
            msg.attach(pdf_anexo)

        # Envia o e-mail
        servidor.sendmail(de, para, msg.as_string())

        # Fecha a conexão com o servidor SMTP
        servidor.quit()

        return {"execução": True}

    except Exception as e:
        return {"erro": e, "execução": False}
