from flask import Flask,render_template,request,session,flash
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,RadioField,SelectField,TextAreaField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

app=Flask(__name__)
app.config['SECRET_KEY']= 'mykey'
Bootstrap(app)

class myForm(FlaskForm):
    name=StringField("ป้อนชื่อ",validators=[DataRequired()])
    isAccept=BooleanField('ยอมรับ')
    gender=RadioField('เพศ',choices=[('male','ชาย'),('female','หญิง'),('other','อื่นๆ')])
    skill=SelectField('ความสามารถ',choices=[('พูดeng','พูดeng'),('ร้องเพลง','ร้องเพลง'),('เขียนเกม','เขียนเกม')])
    adress=TextAreaField("ป้อนที่อยู่")
    submit=SubmitField("บันทึก")

@app.route('/',methods=['get','post'])
def index():
    form=myForm()
    if form.validate_on_submit():
        flash('บันทึกเรียบร้อย')
        session['name']=form.name.data
        session['isAccept']=form.isAccept.data
        session['gender']=form.gender.data
        session['skill']=form.skill.data
        session['adress']=form.adress.data
        # ลบข้อมูล
        form.name.data=""
        form.isAccept.data=""
        form.gender.data=""
        form.adress.data=""
    return render_template("index.html",form=form)

if __name__=="__main__":
    app.run(debug=True)
