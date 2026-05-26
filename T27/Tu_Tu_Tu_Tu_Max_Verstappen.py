import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
#каюсь, оце вже мені підказав ШІ, бо не знав як позбутись помилки в консолі

import cgi
import os
import sys
import codecs

encoding = 'utf-8'
if os.name == 'nt' and sys.stdout.encoding != 'utf-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

HTML_PAGE = """Content-type: text/html; charset={}\n\n
<html>
<head>
    <title>Лабораторна робота</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f9f9f9; }}
        table {{ border-collapse: collapse; margin-top: 10px; background: white; }}
        td, th {{ border: 1px solid black; padding: 8px; text-align: center; }}
        .matr-input {{ width: 50px; text-align: center; }}
        input[type="text"], input[type="password"] {{ padding: 5px; margin: 5px 0; }}
        input[type="submit"] {{ padding: 6px 12px; cursor: pointer; }}
    </style>
</head>
<body>
{}
</body>
</html>
"""

login = "MADMax"
password = "4timesWDCchamp"

form = cgi.FieldStorage()
step = form.getvalue('step', 'login')
is_auth = form.getvalue('is_auth', '0')
content = ""


if step == 'check_login':
    l = form.getvalue('login', '').strip()
    p = form.getvalue('password', '').strip()
    if l == login and p == password:
        step = 'menu'
        is_auth = '1'
    else:
        content = """
        <h3 style="color:red;">Неправильний логін або пароль</h3>
        <a href="">Спробувати ще раз</a>
        """

if step == 'login':
    content = """
    <h3>Вхід в систему</h3>
    <form method=POST>
        <input type=hidden name=step value="check_login">
        Логін: <input type=text name=login value=""><br><br>
        Пароль: <input type=password name=password value=""><br><br>
        <input type=submit value="Увійти">
    </form>
    """

elif step == 'menu' and is_auth == '1':
    content = """
    <h3>Головне меню</h3>

    <h4>Задача 27.4</h4>
    <p>Визначення кількості змін знаку в послідовності до появи 0.</p>
    <form method=POST>
        <input type=hidden name=step value="task1_input">
        <input type=hidden name=is_auth value="1">
        <input type=submit value="Перейти до 27.4">
    </form>
    <hr>

    <h4>Задача 27.10</h4>
    <p>Множення двох матриць.</p>
    <form method=POST>
        <input type=hidden name=step value="task2_dims">
        <input type=hidden name=is_auth value="1">
        <input type=submit value="Перейти до 27.10">
    </form>
    """


elif step == 'task1_input' and is_auth == '1':
    seq = form.getvalue('seq', '')
    new_val = form.getvalue('new_val', '').strip()

    error_msg = ""
    if new_val:
        try:
            val_int = int(new_val)
            if val_int == 0:
                nums = [int(x) for x in seq.split(',') if x]
                changes = 0
                for i in range(1, len(nums)):
                    if nums[i] * nums[i - 1] < 0:
                        changes += 1

                content = f"<h3>Результат (Задача 27.4)</h3>"
                if nums:
                    content += f"<p>Введена послідовність: {seq}, 0</p>"
                    content += f"<p>Кількість змін знаку: <b>{changes}</b></p>"
                else:
                    content += "<p>Послідовність порожня (одразу введено 0).</p>"

                content += """
                <form method=POST>
                    <input type=hidden name=step value="menu">
                    <input type=hidden name=is_auth value="1">
                    <input type=submit value="В головне меню">
                </form>
                """
                step = 'done'
            else:
                if seq == '':
                    seq = str(val_int)
                else:
                    seq += ',' + str(val_int)
        except ValueError:
            error_msg = "<p style='color:red;'>Введіть ціле число</p>"

    if step != 'done':
        content = f"""
        <h3>Задача 27.4</h3>
        {error_msg}
        <p>Вже введено: <b>{seq if seq else 'Поки нічого'}</b></p>
        <form method=POST>
            <input type=hidden name=step value="task1_input">
            <input type=hidden name=is_auth value="1">
            <input type=hidden name=seq value="{seq}">
            Нове число (0 для завершення): <input type=text name=new_val autofocus>
            <input type=submit value="Обробити">
        </form>
        <br>
        <form method=POST>
            <input type=hidden name=step value="menu">
            <input type=hidden name=is_auth value="1">
            <input type=submit value="Назад">
        </form>
        """


elif step == 'task2_dims' and is_auth == '1':
    content = f"""
    <h3>Задача 27.10: Розміри матриць</h3>
    <form method=POST>
        <input type=hidden name=step value="task2_mat1">
        <input type=hidden name=is_auth value="1">
        <b>Матриця A:</b><br>
        Рядки: <input type=text name=n1 size=3 value="2"> 
        Стовпці: <input type=text name=m1 size=3 value="2"><br><br>

        <b>Матриця B:</b><br>
        Рядки: <input type=text name=n2 size=3 value="2"> 
        Стовпці: <input type=text name=m2 size=3 value="2"><br><br>

        <input type=submit value="Далі">
    </form>
    """

elif step == 'task2_mat1' and is_auth == '1':
    n1 = form.getvalue('n1', '0').strip()
    m1 = form.getvalue('m1', '0').strip()
    n2 = form.getvalue('n2', '0').strip()
    m2 = form.getvalue('m2', '0').strip()

    is_valid = False
    if n1.isdigit() and m1.isdigit() and n2.isdigit() and m2.isdigit():
        if int(n1) > 0 and int(m1) > 0 and int(n2) > 0 and int(m2) > 0:
            is_valid = True

    if not is_valid:
        content = f"""
        <h3>Задача 27.10: Розміри матриць</h3>
        <p style='color:red;'>Розміри мають бути натуральними числами</p>
        <form method=POST>
            <input type=hidden name=step value="task2_mat1">
            <input type=hidden name=is_auth value="1">
            <b>Матриця A:</b><br>
            Рядки: <input type=text name=n1 size=3 value="{n1}"> 
            Стовпці: <input type=text name=m1 size=3 value="{m1}"><br><br>

            <b>Матриця B:</b><br>
            Рядки: <input type=text name=n2 size=3 value="{n2}"> 
            Стовпці: <input type=text name=m2 size=3 value="{m2}"><br><br>

            <input type=submit value="Далі">
        </form>
        """


    elif m1 != n2:
        content = f"""
        <h3>Задача 27.10: Розміри матриць</h3>
        <p style='color:red;'>Матриці неможливо перемножити (стовпці А мають дорівнювати рядкам В)</p>
        <form method=POST>
            <input type=hidden name=step value="task2_mat1">
            <input type=hidden name=is_auth value="1">
            <b>Матриця A:</b><br>
            Рядки: <input type=text name=n1 size=3 value="{n1}"> 
            Стовпці: <input type=text name=m1 size=3 value="{m1}"><br><br>

            <b>Матриця B:</b><br>
            Рядки: <input type=text name=n2 size=3 value="{n2}"> 
            Стовпці: <input type=text name=m2 size=3 value="{m2}"><br><br>

            <input type=submit value="Далі">
        </form>
        """
    else:
        empty_err = "<p style='color:red;'>Заповніть всі поля Матриці А</p>" if form.getvalue('empty_err') else ""

        content = f"<h3>Введення Матриці A ({n1}x{m1})</h3>"
        content += empty_err
        content += "<form method=POST>"
        content += "<input type=hidden name=step value='task2_mat2'>"
        content += "<input type=hidden name=is_auth value='1'>"
        content += f"<input type=hidden name=n1 value='{n1}'><input type=hidden name=m1 value='{m1}'>"
        content += f"<input type=hidden name=n2 value='{n2}'><input type=hidden name=m2 value='{m2}'>"

        content += "<table>"
        for i in range(int(n1)):
            content += "<tr>"
            for j in range(int(m1)):
                prev_val = form.getvalue(f'A_{i}_{j}', '')
                content += f"<td><input type=text class='matr-input' name='A_{i}_{j}' value='{prev_val}'></td>"
            content += "</tr>"
        content += "</table><br>"
        content += "<input type=submit value='Далі до Матриці B'></form>"

elif step == 'task2_mat2' and is_auth == '1':
    n1 = int(form.getvalue('n1', '0'))
    m1 = int(form.getvalue('m1', '0'))
    n2 = int(form.getvalue('n2', '0'))
    m2 = int(form.getvalue('m2', '0'))

    a_ok = True
    a_hidden_inputs = ""
    for i in range(n1):
        for j in range(m1):
            val = form.getvalue(f'A_{i}_{j}', '').strip()
            if val == '':
                a_ok = False
            a_hidden_inputs += f"<input type=hidden name='A_{i}_{j}' value='{val}'>\n"

    if not a_ok:
        content = "<h3>Не всі поля Матриці А заповнено</h3>"
        content += "<form method=POST>"
        content += "<input type=hidden name=step value='task2_mat1'>"
        content += "<input type=hidden name=is_auth value='1'>"
        content += "<input type=hidden name=empty_err value='1'>"
        content += f"<input type=hidden name=n1 value='{n1}'><input type=hidden name=m1 value='{m1}'>"
        content += f"<input type=hidden name=n2 value='{n2}'><input type=hidden name=m2 value='{m2}'>"
        content += a_hidden_inputs
        content += "<input type=submit value='Повернутися до Матриці А'></form>"
    else:
        empty_err = "<p style='color:red;'>Заповніть всі поля Матриці B</p>" if form.getvalue('empty_err') else ""

        content = f"<h3>Введення Матриці B ({n2}x{m2})</h3>"
        content += empty_err
        content += "<form method=POST>"
        content += "<input type=hidden name=step value='task2_res'>"
        content += "<input type=hidden name=is_auth value='1'>"
        content += f"<input type=hidden name=n1 value='{n1}'><input type=hidden name=m1 value='{m1}'>"
        content += f"<input type=hidden name=n2 value='{n2}'><input type=hidden name=m2 value='{m2}'>"
        content += a_hidden_inputs

        content += "<table>"
        for i in range(n2):
            content += "<tr>"
            for j in range(m2):
                prev_val = form.getvalue(f'B_{i}_{j}', '')
                content += f"<td><input type=text class='matr-input' name='B_{i}_{j}' value='{prev_val}'></td>"
            content += "</tr>"
        content += "</table><br>"
        content += "<input type=submit value='Обчислити добуток'></form>"

elif step == 'task2_res' and is_auth == '1':
    n1 = int(form.getvalue('n1', '0'))
    m1 = int(form.getvalue('m1', '0'))
    n2 = int(form.getvalue('n2', '0'))
    m2 = int(form.getvalue('m2', '0'))

    b_ok = True
    b_hidden_inputs = ""
    for i in range(n2):
        for j in range(m2):
            val = form.getvalue(f'B_{i}_{j}', '').strip()
            if val == '': b_ok = False
            b_hidden_inputs += f"<input type=hidden name='B_{i}_{j}' value='{val}'>\n"

    a_hidden_inputs = ""
    for i in range(n1):
        for j in range(m1):
            val = form.getvalue(f'A_{i}_{j}', '').strip()
            a_hidden_inputs += f"<input type=hidden name='A_{i}_{j}' value='{val}'>\n"

    if not b_ok:
        content = "<h3>Не всі поля Матриці B заповнено</h3>"
        content += "<form method=POST>"
        content += "<input type=hidden name=step value='task2_mat2'>"
        content += "<input type=hidden name=is_auth value='1'>"
        content += "<input type=hidden name=empty_err value='1'>"
        content += f"<input type=hidden name=n1 value='{n1}'><input type=hidden name=m1 value='{m1}'>"
        content += f"<input type=hidden name=n2 value='{n2}'><input type=hidden name=m2 value='{m2}'>"
        content += a_hidden_inputs
        content += b_hidden_inputs
        content += "<input type=submit value='Повернутися до Матриці B'></form>"
    else:
        try:
            A = []
            for i in range(n1):
                row = []
                for j in range(m1):
                    row.append(float(form.getvalue(f'A_{i}_{j}')))
                A.append(row)

            B = []
            for i in range(n2):
                row = []
                for j in range(m2):
                    row.append(float(form.getvalue(f'B_{i}_{j}')))
                B.append(row)

            result = [[0 for _ in range(m2)] for _ in range(n1)]
            for i in range(n1):
                for j in range(m2):
                    for k in range(m1):
                        result[i][j] += A[i][k] * B[k][j]

            content = "<h3>Результат 27.10</h3>"

            content += "<b>Матриця A:</b><table>"
            for row in A: content += "<tr>" + "".join([f"<td>{x}</td>" for x in row]) + "</tr>"
            content += "</table><br>"

            content += "<b>Матриця B:</b><table>"
            for row in B: content += "<tr>" + "".join([f"<td>{x}</td>" for x in row]) + "</tr>"
            content += "</table><br>"

            content += "<b>Добуток (A x B):</b><table style='background-color:#e6ffe6;'>"
            for row in result: content += "<tr>" + "".join([f"<td>{x}</td>" for x in row]) + "</tr>"
            content += "</table><br>"

        except ValueError:
            content = "<h3 style='color:red;'>Помилка: в полях матриць мають бути лише числа</h3>"

        content += """
        <form method=POST>
            <input type=hidden name=step value="menu">
            <input type=hidden name=is_auth value="1">
            <input type=submit value="В головне меню">
        </form>
        """

if not content:
    content = "<h3>Пу-пу-пу, щось пішло не так</h3><a href='?step=login'>На головну</a>"

print(HTML_PAGE.format(encoding, content))