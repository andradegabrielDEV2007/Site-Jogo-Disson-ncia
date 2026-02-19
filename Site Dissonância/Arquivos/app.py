from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///dados.db"
db = SQLAlchemy() 
db.init_app(app) #associa o banco de dados à aplicação 


#Configuração do email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'leonardogabril985@gmail.com'
app.config['MAIL_PASSWORD'] = 'mldl ovuc xyjy ffmy'
mail = Mail(app)

class FormJogar (db.Model):
    __tablename__ = 'formJogar'
    
    idJogar = db.Column(db.Integer, primary_key=True)
    nomeJogar = db.Column(db.String(80), nullable=False)
    emailJogar = db.Column(db.String(120), nullable=False)
    
class FormMensagem (db.Model):
    __tablename__ = 'formMensagem'
    
    idMensagem = db.Column (db.Integer, primary_key=True)
    emailMensagem = db.Column(db.String(120), nullable=False)
    mensagemCliente = db.Column(db.String(140), nullable=False)
    


@app.route ('/')
def home():
    fomulario_jogar = FormJogar.query.all()
    formulario_mensagem = FormMensagem.query.all()
    return render_template ('home.html')

@app.route('/sobre')
def sobre ():
    return render_template ('sobre.html')

@app.route ('/equipe')
def equipe():
    return render_template ('equipe.html')

@app.route ('/jogar', methods = ['GET', 'POST'])

def jogar():
    if request.method == 'POST':
        nomeJogar = request.form['nomeJogar']
        emailJogar = request.form['emailJogar']
        
      
        db.session.add(FormJogar(nomeJogar=nomeJogar, emailJogar=emailJogar))
        db.session.commit()
        
        msg = Message(
            subject='Aqui está o jogo!', 
            sender='leonardogabril985@gmail.com',
            recipients= [emailJogar]
        )
        
        link_download = 'https://drive.google.com/drive/folders/1lidn6E8fWp-ESM3ey5Klf01o5bQKt_nt?usp=sharing'
        msg.body = (f"Obrigado {nomeJogar} por se inscrever! Clique no link para baixar:{link_download}")
       
        mail.send(msg)
        
        return render_template('home.html')

    
    return render_template('jogar.html')



@app.route ('/faq', methods = ['GET', 'POST'])
def faq ():
    
    if request.method=='POST':
        emailFaq = request.form['emailFaq']
        duvidaFaq = request.form['duvidaFaq']
        
        db.session.add(FormMensagem(emailMensagem=emailFaq, mensagemCliente=duvidaFaq))
        db.session.commit()
        
        
        msG = Message(
        subject=f'Mensagem do FAQ de: {emailFaq}', 
        sender='leonardogabril985@gmail.com',
        recipients=['leonardogabril985@gmail.com']
        )
        msG.body = (duvidaFaq)
       
        mail.send(msG)
        
        return render_template('home.html')
    
    return render_template ('faq.html')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)