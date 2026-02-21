from flask import Flask, render_template

from flask import Flask, render_template,request,redirect,url_for 
from flask_wtf.csrf import CSRFProtect
from flask import flash 
from config import DevelopmentConfig
import forms
from models import db,Alumnos

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)
db.init_app(app)
csrf=CSRFProtect(app)
@app.errorhandler(404) 
def page_not_fount(error):
 return render_template("404.html"),404

@app.route("/index")
def index():
    alumnos = Alumnos.query.all() 
    return render_template("index.html", alumnos=alumnos)

@app.route('/Alumnos', methods=['GET', 'POST'])
def alumnos():
    create_form = forms.UserForm(request.form)
    
    if request.method == 'POST' and create_form.validate():
        alum = Alumnos(
            nombre=create_form.nombre.data,
            apaterno=create_form.apaterno.data,
            email=create_form.correo.data  
        )
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('index'))
    
        
    return render_template("Alumnos.html", form=create_form)

@app.route("/detalles", methods=['GET', 'POST'])
def detalles():
    if request.method=='GET':
         id=request.args.get('id')
         #select * from alumnos where id=id
         alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
         nombre=alum1.nombre
         apaterno=alum1.apaterno
         email=alum1.email     
    return render_template("detalles.html", id=id,nombre=nombre,
                           apaterno=apaterno,emsil=email)


if __name__ == '__main__':
	with app.app_context():
		db.create_all()
	app.run()
	
#insertar17-02-2026 comit 