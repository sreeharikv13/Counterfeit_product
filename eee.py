import demjson
from flask import Flask, render_template, request, redirect, session, jsonify
from DBConnection import Db
import qrcode
from enc_dec import AESCipher
from email.mime import image
import smtplib
from email.mime.text import MIMEText
# from flask_mail import Mail

import datetime

app = Flask(__name__)
app.secret_key = "block"
path = r"D:\2022-2023\LBS_Counterfiet\Counterfiet Final\counterfiet\static\Image\\"
qrpath = r"D:\2022-2023\LBS_Counterfiet\Counterfiet Final\counterfiet\static\\"

import json
from web3 import Web3, HTTPProvider

# truffle development blockchain address
blockchain_address = 'http://127.0.0.1:9545'
# Client instance to interact with the blockchain
web3 = Web3(HTTPProvider(blockchain_address))
# Set the default account (so we don't need to set the "from" for every transaction call)
web3.eth.defaultAccount = web3.eth.accounts[0]

compiled_contract_path = 'D:/2022-2023/LBS_Counterfiet/Counterfiet Final/counterfiet/node_modules/.bin/build/contracts/StructDemo.json'
# Deployed contract address (see `migrate` command output: `contract address`)
deployed_contract_address = '0xE0Cb4F46B258349D502aE1D95E2de7ff80c8ccE1'


#
# Path to the compiled contract JSON file

#
# Path to the compiled contract JSON file
@app.route('/', methods=['POST', 'get'])
def login1():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = Db()
        res = db.selectOne("select * from login where user_name = '" + username + "' and password = '" + password + "'")
        if res is not None:
            session['lg'] = "lin"
            session['lid'] = res['login_id']
            if res['user_type'] == 'admin':
                return redirect('/ahome')
            if res['user_type'] == 'manufacturer':
                return redirect('/mhome')
            if res['user_type'] == 'pending':
                return ''' <script> alert("Please wait for verification...!!!!");window.location='/' </script>   '''
        else:
            return ''' <script> alert("Invalid Username  or Password...!!!!");window.location='/' </script>   '''

    return render_template("login.html")


@app.route('/mhome')
def mhome():
    if session['lg'] == "lin":
        return render_template("Manufacture/index.html")
    else:
        return redirect('/')


@app.route('/logout')
def logout():
    session['lg'] = ""
    session.clear()
    return redirect('/')


# ===================================================admin=================================================================
@app.route('/ahome')
def ahome():
    if session['lg'] == "lin":
        return render_template("Admin/index.html")
    else:
        return redirect('/')


@app.route('/view_man')
def view_man():
    if session['lg'] == "lin":
        db = Db()
        q = db.select("select * from login,company where ins_id=login_id and user_type='pending'")
        return render_template("Admin/View_manufacture.html", data=q)
    else:
        return redirect('/')


@app.route('/view_mans')
def view_mans():
    if session['lg'] == "lin":
        db = Db()
        q = db.select("select * from login,company where ins_id=login_id and user_type='manufacturer'")
        return render_template("Admin/View_manufacture.html", data=q)
    else:
        return redirect('/')


@app.route('/view_user')
def view_user():
    if session['lg'] == "lin":
        db = Db()
        q = db.select("select * from user")
        return render_template("Admin/View_user.html", data=q)
    else:
        return redirect('/')


@app.route('/view_com')
def view_com():
    if session['lg'] == "lin":
        db = Db()
        q = db.select("select * from user,spam where spam.uid=user.user_id")
        return render_template("Admin/View_com.html", data=q)
    else:
        return redirect('/')


@app.route('/approve/<i>')
def approve(i):
    if session['lg'] == "lin":
        db = Db()
        q = db.update("update login set user_type='manufacturer' where login_id='" + i + "'")
        return ''' <script> alert("Approved successfully...!!!!");window.location='/view_man' </script>   '''

    else:
        return redirect('/')


@app.route('/reject/<i>')
def reject(i):
    if session['lg'] == "lin":
        db = Db()
        q = db.delete("delete from login where login_id='" + i + "'")
        q1 = db.delete("delete from company where ins_id='" + i + "'")
        return ''' <script> alert("Rejected successfully...!!!!");window.location='/view_man' </script>   '''

    else:
        return redirect('/')


@app.route('/view_comp')
def view_comp():
    if session['lg'] == "lin":
        db = Db()
        q = db.select("select * from user,complaint where complaint.user_id=user.user_id")
        print(q)
        return render_template("Admin/View_complaints.html", data=q)
    else:
        return redirect('/')


@app.route('/reply/<i>', methods=['get', 'post'])
def reply(i):
    if session['lg'] == "lin":
        if request.method == 'POST':
            db = Db()
            r = request.form['r']
            db.update("update complaint set reply='" + r + "',reply_date=curdate() where complaint_id='" + i + "'")
            return ''' <script> alert("Updated successfully...!!!!");window.location='/view_comp' </script>   '''

        return render_template("Admin/send_reply.html")
    else:
        return redirect('/')


# ===================================================manifacture===========================================================
@app.route('/reg', methods=['post', 'get'])
def reg():
    if request.method == 'POST':
        n1 = request.form['n1']
        n2 = request.form['n2']
        n3 = request.form['n3']
        n4 = request.form['n4']
        n5 = request.form['n5']
        n6 = request.form['n6']
        n7 = request.form['n7']
        n8 = request.form['n8']
        n9 = request.form['n9']
        n10 = request.form['n10']
        db = Db()
        q2 = db.selectOne("select * from login where user_name='" + n8 + "'")
        if q2 is None:
            q = db.insert(
                "insert into `login`(`login_id`,`user_name`,`password`,`user_type`) values ( NULL,'" + n8 + "','" + n10 + "','pending');")
            q1 = db.insert(
                "insert into `company`(`ins_id`,`ins_name`,`ins_license`,`ins_establishedyr`,`ins_place`,`ins_post`,`ins_pin`,`ins_district`,`ins_ph`,`ins_email`) values ( '" + str(
                    q) + "','" + n1 + "','" + n2 + "','" + n3 + "','" + n4 + "','" + n5 + "','" + n7 + "','" + n6 + "','" + n9 + "','" + n8 + "');")
            return ''' <script> alert("Registered sucessfully...!!!!");window.location='/' </script>   '''

        else:
            return ''' <script> alert("USer already found...!!!!");window.location='/reg' </script>   '''

    return render_template("Manufacture/reg.html")


@app.route('/product_add', methods=['post', 'get'])
def product_add():
    if session['lg'] == "lin":
        if request.method == 'POST':
            n1 = request.form['n1']
            n2 = request.form['n2']
            n3 = request.form['n3']
            n4 = request.form['n4']
            n5 = request.form['n5']
            with open(compiled_contract_path) as file:
                contract_json = json.load(file)  # load contract info as JSON
                contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
            c = 0
            contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
            blocknumber = web3.eth.get_block_number()
            for i in range(blocknumber, 1, -1):
                a = web3.eth.get_transaction_by_block(i, 0)
                decoded_input = contract.decode_function_input(a['input'])
                if str(decoded_input[1]['p']) == n1 and str(decoded_input[1]['l']) == n2 and str(
                        decoded_input[1]['t']) == n3 and str(decoded_input[1]['ins']) == n4 and str(
                        decoded_input[1]['d']) == n5:
                    c += 1
                else:
                    c = c
            if c == 0:
                message2 = contract.functions.addEmployee(blocknumber + 1, n1, n2, n3, n4, n5,
                                                          (session['lid'])).transact()

                # Create qr code instance
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_H,
                    box_size=3,
                    border=4,
                )
                # Add data
                a = AESCipher("cp")
                enc_data = a.encrypt(str(blocknumber + 1))
                qr.add_data(str(enc_data))
                qr.make(fit=True)
                import datetime
                img = qr.make_image()
                img.save(qrpath + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + n1 + "image.jpg")
                return ''' <script> alert("Inserted...!!!!");window.location="/product_add" </script>   '''
            else:
                return ''' <script> alert("Already Inserted...!!!!");window.location="/product_add" </script>   '''

        return render_template("Manufacture/product_add.html")
    else:
        return redirect('/')


@app.route('/product_view', methods=['post', 'get'])
def product_view():
    if session['lg'] == "lin":
        data = []
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)  # load contract info as JSON
            contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        blocknumber = web3.eth.get_block_number()
        # print(blocknumber)
        for i in range(blocknumber, 0, -1):
            a = web3.eth.get_transaction_by_block(i, 0)
            decoded_input = contract.decode_function_input(a['input'])
            res = {}
            res['productname'] = decoded_input[1]['p']
            res['location'] = decoded_input[1]['l']
            res['timestamp'] = decoded_input[1]['t']
            res['ins'] = decoded_input[1]['ins']
            res['details'] = decoded_input[1]['d']
            res['mid'] = decoded_input[1]['mid']
            if str(decoded_input[1]['mid']) == str(session['lid']):
                data.append(res)

        return render_template("Manufacture/product_view.html", data=data)
    else:
        return redirect('/')


@app.route('/mview_com')
def mview_com():
    if session['lg'] == "lin":
        db = Db()
        q = db.select("select * from user,spam where spam.uid=user.user_id")
        return render_template("Manufacture/SPAM.html", data=q)
    else:
        return redirect('/')


# =======================================================================================================================================

@app.route('/login', methods=['post'])
def login():
    db = Db()
    username = request.form['username']
    password = request.form['password']
    r = {}
    qry = "select * from login where user_name='" + username + "' and password='" + password + "' and user_type='user'"
    res = db.selectOne(qry)
    if res is not None:
        r['lid'] = res['login_id']
        r['type'] = res['user_type']
        r['status'] = "ok"
    else:
        r['status'] = "none"
    print(r)
    return demjson.encode(r)


@app.route('/forgo', methods=['post'])
def forgo():
    db = Db()
    username = request.form['username']
    r = {}
    qry = "select * from login where user_name='" + username + "'"
    res = db.selectOne(qry)
    if res is not None:
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)

            gmail.ehlo()

            gmail.starttls()

            gmail.login('yourmail@gmail.com', '')

        except Exception as e:
            print("Couldn't setup email!!" + str(e))

        msg = MIMEText("Your Password is " + str(res['password']))

        msg['Subject'] = 'Verification'

        msg['To'] = username

        msg['From'] = 'yourmail@gmail.com'

        try:

            gmail.send_message(msg)
            r['status'] = "ok"

        except Exception as e:

            print("COULDN'T SEND EMAIL", str(e))
            r['status'] = "Could not send mail"


    else:
        r['status'] = "none"
    return demjson.encode(r)


@app.route('/reg1', methods=['post'])
def reg1():
    db = Db()
    n1 = request.form['n']
    n2 = request.form['e']
    n3 = request.form['p']
    n5 = request.form['p1']
    r = {}
    q = db.selectOne("select * from login where user_name='" + n2 + "'")
    if q is None:
        q1 = db.insert(
            "insert into `login`(`user_name`,`password`,`user_type`) values ( '" + n2 + "','" + n5 + "','user');")

        res = db.insert("insert into `user`(`user_id`,`name`,`email`,`phone`) values ( '" + str(
            q1) + "','" + n1 + "','" + n2 + "','" + n3 + "');")
        if int(q1) > 0:
            r['status'] = "ok"
        else:
            r['status'] = "Please register again"
    else:
        r['status'] = "Username already found"
    print(r)
    return demjson.encode(r)


@app.route('/andviewproducts', methods=['post', 'get'])
def andviewproducts():
    try:
        b = request.form['srno']
        q = AESCipher("cp")
        b = q.decrypt(b)
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)  # load contract info as JSON
            contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        blocknumber = web3.eth.get_block_number()
        count = 0
        for i in range(blocknumber, 0, -1):
            a = web3.eth.get_transaction_by_block(i, 0)
            decoded_input = contract.decode_function_input(a['input'])
            if str(decoded_input[1]['bid']) == b:
                db = Db()
                q = db.selectOne("select * from company where ins_id='" + str(decoded_input[1]['mid']) + "'")
                return jsonify(status="ok", m=str(q['ins_name']), p=decoded_input[1]['p'], l=decoded_input[1]['l'],
                               t=decoded_input[1]['t'], i=decoded_input[1]['ins'], d=decoded_input[1]['d'])
            else:
                count = count + 1
        if count > 0:
            return jsonify(status="none")
    except Exception as e:
        return jsonify(status="none")


@app.route('/csend', methods=['post'])
def csend():
    db = Db()
    lid = request.form['lid']
    p = request.form['s']
    n = request.form['c']
    r = {}
    res = db.insert(
        "insert into `spam`(`product_name`,`note`,`date`,`uid`) values ( '" + p + "','" + n + "',curdate(),'" + lid + "');")
    if res > 0:
        r['status'] = "ok"
    else:
        r['status'] = "none"
    return demjson.encode(r)


@app.route('/sendcomplaints', methods=['post'])
def sendcomplaints():
    db = Db()
    lid = request.form['lid']
    com = request.form['comp']
    r = {}
    res = db.insert(
        "insert into `complaint`(`complaint_id`,`complaint`,`complaint_date`,`reply`,`reply_date`,`user_id`) values ( '','" + com + "',curdate(),'pending','0000-00-00','" + lid + "');")
    if int(res) > 0:
        r['status'] = "ok"
    else:
        r['status'] = "none"
    return demjson.encode(r)


@app.route('/viewcompnt', methods=['post'])
def viewcompnt():
    db = Db()
    lid = request.form['lid']
    r = {}
    res = db.select("select * from  `complaint` where user_id='" + lid + "'")
    print(res)
    if len(res) > 0:
        r['status'] = "ok"
        r['data'] = res
        print(res)
    else:
        r['status'] = "none"
    return demjson.encode(r)


@app.route('/delcom', methods=['post'])
def delcom():
    db = Db()
    pid = request.form['pid']
    r = {}
    res = db.delete("delete from `complaint` where complaint_id='" + pid + "'")
    if res > 0:
        r['status'] = "ok"
    else:
        r['status'] = "none"
    return demjson.encode(r)


@app.route('/viewman', methods=['post'])
def viewman():
    db = Db()
    r = {}
    res = db.select("select * from  `company`")
    print(res)
    if len(res) > 0:
        r['status'] = "ok"
        r['data'] = res
        print(res)
    else:
        r['status'] = "none"
    return demjson.encode(r)


@app.route('/viewprd', methods=['post', 'get'])
def viewprd():
    mid = request.form['mid']
    data = []
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    blocknumber = web3.eth.get_block_number()
    # print(blocknumber)
    for i in range(blocknumber, 0, -1):
        a = web3.eth.get_transaction_by_block(i, 0)
        decoded_input = contract.decode_function_input(a['input'])
        res = {}
        res['productname'] = decoded_input[1]['p']
        res['location'] = decoded_input[1]['l']
        res['timestamp'] = decoded_input[1]['t']
        res['ins'] = decoded_input[1]['ins']
        res['details'] = decoded_input[1]['d']
        res['mid'] = decoded_input[1]['mid']
        if str(decoded_input[1]['mid']) == str(mid):
            data.append(res)
    return jsonify(status="ok", data=data)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
