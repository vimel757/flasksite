from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  



@app.route('/', methods=['GET', 'POST'])
def quick_registration():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        district = request.form.get('district')

        url = "https://dev.yip.kerala.gov.in/yipapp/index.php/Idea2021/add_pre_reg"
        data = {
            "prereg_name": name,
            "prereg_email": email,
            "prereg_mob": mobile,
            "districtd": district
        }
        response = requests.post(url, data=data)

        if response.status_code == 200:
            json_response = response.json()
            if json_response.get("Success") == "1":
       
                tempreg_id = json_response.get("tempregId")
                session['tempreg_id'] = tempreg_id
                session['prereg_name'] = name
                session['prereg_email'] = email
                session['prereg_mob'] = mobile
                session['districtd'] = district
                return redirect(url_for('verify_otp'))
            else:
            
                error_message = json_response.get("msg")
                return render_template('registration.html', error_message=error_message)
        else:
           
            error_message = "Failed to register. Please try again later."
            return render_template('registration.html', error_message=error_message)
    else:
        return render_template('registration.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    tempreg_id = session.get('tempreg_id')

    if not tempreg_id:
        return redirect(url_for('quick_registration'))

    if request.method == 'POST':
        otp_received = request.form.get('otp')


        name = session.get('prereg_name')
        email = session.get('prereg_email')
        mobile = session.get('prereg_mob')
        district = session.get('districtd')

       
        url = "https://dev.yip.kerala.gov.in/yipapp/index.php/Com_mobile_otp/checkotp"
        data = {
            "otp_received": otp_received,
            "user_id": email,
            "prereg_name": name,
            "prereg_email": email,
            "prereg_mob": mobile,
            "districtd": district
        }
        response = requests.post(url, data=data)

        if response.status_code == 200:
            json_response = response.json()
            if json_response.get("Success") == "1":
               
                return redirect(url_for('login'))  
            else:
                
                error_message = json_response.get("msg")
                return render_template('verify_otp.html', error_message=error_message)
        else:
       
            error_message = "Failed to verify OTP. Please try again later."
            return render_template('verify_otp.html', error_message=error_message)
    else:
        return render_template('verify_otp.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

    
        if email == 'admin@example.com' and password == 'password':
            
            session['user_email'] = email
            return redirect(url_for('quick_registration'))
        else:
            error_message = "Invalid email or password. Please try again."
            return render_template('login.html', error_message=error_message)

    else:
        return render_template('login.html')



@app.route('/logout')
def logout():

    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

    


