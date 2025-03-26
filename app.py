from flask import Flask, render_template, request, make_response, redirect, url_for
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/url_params')
def url_params():
    params = request.args
    return render_template('url_params.html', params=params)

@app.route('/headers')
def headers():
    headers = dict(request.headers)
    return render_template('headers.html', headers=headers)

@app.route('/cookies')
def cookies():
    cookies = request.cookies
    return render_template('cookies.html', cookies=cookies)

@app.route('/form_params', methods=['GET', 'POST'])
def form_params():
    if request.method == 'POST':
        form_data = request.form
        return render_template('form_params.html', form_data=form_data)
    return render_template('form_params.html')

@app.route('/phone', methods=['GET', 'POST'])
def phone():
    error = None
    formatted_number = None
    
    if request.method == 'POST':
        phone_number = request.form.get('phone', '')
        
        # Удаляем все допустимые символы для проверки
        digits = re.sub(r'[\s\(\)\-\.\+]', '', phone_number)
        
        # Проверяем наличие недопустимых символов
        if not re.match(r'^[\d\s\(\)\-\.\+]+$', phone_number):
            error = 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.'
        # Проверяем количество цифр
        elif len(digits) not in [10, 11]:
            error = 'Недопустимый ввод. Неверное количество цифр.'
        else:
            # Форматируем номер
            digits = re.sub(r'\D', '', phone_number)
            if len(digits) == 11 and digits[0] in ['7', '8']:
                digits = '8' + digits[1:]
            elif len(digits) == 10:
                digits = '8' + digits
            
            formatted_number = f"{digits[0]}-{digits[1:4]}-{digits[4:7]}-{digits[7:9]}-{digits[9:]}"
    
    return render_template('phone.html', error=error, formatted_number=formatted_number)

if __name__ == '__main__':
    app.run(debug=True) 