from flask import Flask, redirect, url_for, render_template, request, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import random
import string

app=Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    source = StringField('Source',
                           validators=[DataRequired(), Length(min=2, max=20)])
    destination = StringField('Destination',
                           validators=[DataRequired(), Length(min=2, max=20)])
    msg = TextAreaField('Enter your message here:',
                           validators=[DataRequired(), Length(min=0, max=160)])
    getpost = SelectField('GET/POST',choices=[("GET"), ("POST")])
    submit = SubmitField('Send SMS')


@app.route('/simulation', methods=['POST', 'GET'])
def simulation():
    #create random numbers
    randid = ''.join([random.choice(string.ascii_letters
                                    + string.digits) for n in range(32)])

    error_code = [0, -1, -2, -3, -4, -5, -6, -7, -8, -10, -11]
    error_description = ["Ok", "NoMessage", "NoSource", "NoDestination", "UnsupportedDestination", "InvalidCredentials",
                         "NoCredit", "InvalidDataCoding", "IPnotwhitelisted", "UnknownError",
                         "InvalidInstanceConnection"]
    error = dict(zip(error_code, error_description))
    prob = [0.8, 0, 0, 0, 0.05, 0.03, 0.02, 0, 0.02, 0.05, 0.03]
    print(error.items())
    eout = random.choices(list(error.items()), weights=(0.8, 0, 0, 0, 0.05, 0.03, 0.02, 0, 0.02, 0.05, 0.03), k=1)
    ecode = eout[0][0]
    edescription = eout[0][1]
    
    #instance of the form
    form = RegistrationForm()
    print(form.errors)
    if request.method =="POST":
        if form.is_submitted():
            print("submitted")
        if form.validate():
            print ("valid")
        print(form.errors)
        getpost=form.getpost.data
        if form.validate_on_submit():
            response="\n{\n ErrorCode: "+str(ecode)+",\n ErrorDescription: "+edescription+",\n SMS:[ \n    {ErrorCode: "+str(ecode)+",\n     Id: "+randid+ ",\n     OriginatingAddress: "+form.source.data+",\n     DestinationAddress: "+form.destination.data+",}\n    ], \n MessageCount:1,\n MessageParts:1 \n}\n"
            DLR="\n{\n ErrorCode: "+str(ecode)+",\n ErrorDescription: "+edescription+",\n{"
            flash('your message has been send', 'danger')
            return render_template("layout.html",response=response,getpost=getpost,DLR=DLR,form=form)
        else:
            return render_template("layout.html", content="Error in validation", form=form)
    else:
        #flash('Welcome to MontyMobile Simulation Section', 'success')
        form.username.data = ""
        form.password.data = ""
        form.source.data = ""
        form.destination.data = ""
        form.msg.data = ""
        form.msg.data = ""
        form.getpost.data = ""
        return render_template("layout.html", content="GET",form=form)



if __name__=="__main__":
    app.run(debug=True)