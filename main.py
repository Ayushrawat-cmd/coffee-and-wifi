from flask import Flask, redirect, render_template, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired,Length
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    cafe_location = StringField("Cafe location on google map's URL", validators=[DataRequired()])
    open = StringField(label="Opening time", validators=[DataRequired()])
    close = StringField(label="Closing time", validators=[DataRequired()])
    coffee = SelectField(label="Coffee Rating",choices=[("☕️","☕️"), ("☕️☕️","☕️☕️"),("☕️☕️☕️","☕️☕️☕️"),("☕️☕️☕️☕️","☕️☕️☕️☕️"),("☕️☕️☕️☕️☕️","☕️☕️☕️☕️☕️")])
    wifi = SelectField(label = "Wifi Strength", choices=[("💪","💪"),("💪💪","💪💪"),("💪💪💪","💪💪💪"),("💪💪💪💪","💪💪💪💪"),("💪💪💪💪💪","💪💪💪💪💪"), ])
    power = SelectField(label="Power Socket Availability",choices=[("🔌","🔌"), ("🔌🔌","🔌🔌"),("🔌🔌🔌","🔌🔌🔌"),("🔌🔌🔌🔌","🔌🔌🔌🔌"),("🔌🔌🔌🔌🔌","🔌🔌🔌🔌🔌")])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf-8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', rows = list_of_rows)


@app.route('/add',methods =['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print("True")
            return redirect(url_for('cafes'))
        List = [form.cafe.data,form.cafe_location.data, form.open.data, form.close.data, form.coffee.data, form.wifi.data, form.power.data]
        with open('cafe-data.csv', 'a', encoding="utf-8", newline='\n') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(List)
            csv_file.close()
        return redirect(url_for('cafes'))
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    else:
        return render_template('add.html', form=form)




if __name__ == '__main__':
    app.run(debug=True)
