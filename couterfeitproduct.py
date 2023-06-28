import time
from Flask import Flask, render_template, request, redirect, session, jsonify
from DBConnection import Db
import qrcode
from enc_dec import AESCipher

app = Flask(__name__)
app.secret_key = "hii"

import json
from web3 import Web3, HTTPProvider

# truffle development blockchain address
blockchain_address = 'http://127.0.0.1:7545'
# Client instance to interact with the blockchain
web3 = Web3(HTTPProvider(blockchain_address))
# Set the default account (so we don't need to set the "from" for every transaction call)
web3.eth.defaultAccount = web3.eth.accounts[0]
compiled_contract_path = r'C:\Users\ssree\PycharmProjects\couterfeitproduct\BlockChain\build\contracts\StructDemo.json'
# Deployed contract address (see `migrate` command output: `contract address`)
deployed_contract_address = '0xe7ee38Da431314a58dE886963b10AF4949c50640'

static_path = r"C:\Users\ssree\PycharmProjects\couterfeitproduct\static\\"


@app.route('/login', methods=['get', 'post'])
def login():
    if request.method == "POST":
        u = request.form['textfield']
        p = request.form['textfield2']
        db = Db()
        res = db.selectOne("select * from login WHERE username='" + u + "'and password='" + p + "'")
        if res is not None:
            session['lid'] = res['loginid']
            if res['usertype'] == "admin":
                session['log'] = "lo"
                return redirect('/admin_home')
            elif res['usertype'] == "manufacture":
                session['lid'] = res['loginid']
                session['log'] = "lo"
                return redirect("/mfc_home")
            else:
                return "invalid"
        else:
            return "invalid"
    else:
        return render_template("login.html")


@app.route('/complaintreply')
def complaintreply():
    if session['log'] == "lo":
        db = Db()
        res = db.select("select * from complaint,USER WHERE user.user_id=complaint.user_id")
        return render_template("admin/complaintreply.html", data=res)
    else:
        return redirect('/')


@app.route('/reply/<d>', methods=['get', 'post'])
def reply(d):
    if session['log'] == "lo":
        if request.method == "POST":
            r = request.form['textarea']
            db = Db()
            db.update("update complaint set reply='" + r + "', replydate=curdate() where complaint_id='" + d + "'")
            return '<script>alert("send");window.location="/complaintreply"</script>'
        else:
            return render_template('admin/reply.html')
    else:
        return redirect('/')


@app.route('/verifymanufacture')
def verifymanufacture():
    if session['log'] == "lo":
        db = Db()
        res = db.select(
            "SELECT * from manufacture,login where manufacture.manufacture_loginid=login.loginid and login.usertype='pending'")
        return render_template("admin/verifymanfacture.html", data=res)
    else:
        return redirect('/')


@app.route('/verify/<d>')
def verify(d):
    if session['log'] == "lo":
        # if request.method=="POST":
        db = Db()
        db.update("update login set usertype='manufacture' WHERE loginid='" + d + "' ")
        return '<script>alert("verify");window.location="/verifymanufacture"</script>'
    else:
        return redirect('/')


@app.route('/viewmanufacture')
def viewmanufacture():
    if session['log'] == "lo":
        db = Db()
        res = db.select(
            "SELECT * from manufacture,login where manufacture.manufacture_loginid=login.loginid and login.usertype='manufacture'")
        return render_template("admin/viewmanufacture.html", data=res)
    else:
        return redirect('/')


@app.route('/viewspam')
def viewspam():
    if session['log'] == "lo":
        db = Db()
        res = db.select("select * from spam,user where spam.user_id=user.user_id")
        return render_template("admin/viewspam.html", data=res)
    else:
        return redirect('/')


@app.route('/admin_home')
def admin_home():
    if session['log'] == "lo":
        return render_template("admin/admin_index.html")
    else:
        return redirect('/')


######################          MANUFACTURE
@app.route('/mfc_home')
def mfc_home():
    # if session['log'] == "lo":

    return render_template("manufacture/manufacture_index.html")
    # else:
    #     return redirect('/')


@app.route('/mfc_productmanagement')
def mfc_productmanagement():
    if session['log'] == "lo":
        return render_template("manufacture/productmanagement.html")
    else:
        return redirect('/')


@app.route('/mfc_reg', methods=['get', 'post'])
def mfc_reg():
    # if session['log'] == "lo":
    if request.method == "POST":
        comp_name = request.form['textfield']
        Established_year = request.form['textfield2']
        image = request.files['fileField']
        place = request.form['textfield3']
        post = request.form['textfield10']
        pin = request.form['textfield4']
        district = request.form['textfield5']
        license = request.form['textfield6']
        email = request.form['textfield7']
        phoneno = request.form['textfield8']
        pswd = request.form['textfield9']
        dt = time.strftime("%Y%m%d_%H%M%S")
        image.save(static_path + "manufacture_img\\" + dt + ".jpg")
        path = "/static/manufacture_img/" + dt + ".jpg"
        db = Db()
        res = db.insert("insert into login values('','" + email + "','" + pswd + "','pending')")
        db.insert("insert into manufacture values('" + str(
            res) + "','" + Established_year + "','" + path + "','" + place + "','" + post + "','" + pin + "','" + district + "','" + license + "','" + email + "','" + phoneno + "', '" + comp_name + "')")
        return '<script>alert("manufacture added");window.location="/";</script>'
    else:
        return render_template("reg_index.html")
        # else:
        #     return redirect('/')


@app.route('/mfc_addproduct', methods=['get', 'post'])
def mfc_addproduct():
    if session['log'] == "lo":
        if request.method == "POST":
            product_name = request.form['textfield']
            image = request.files['fileField']
            quantity = request.form['textfield2']
            manufacture_rate = request.form['textfield3']
            manufacture_date = request.form['textfield4']
            expire_date = request.form['textfield5']
            dt = time.strftime("%Y%m%d_%H%M%S")
            image.save(static_path + "manufacture_img\\" + dt + ".jpg")
            path = "/static/manufacture_img/" + dt + ".jpg"
            db = Db()

            # q=db.insert("insert into product values('','"+product_name+"','"+str(path)+"','"+quantity+"','"+manufacture_rate+"','"+manufacture_date+"','"+expire_date+"','"+str(session['lid'])+"')")

            # ============================================================================================



            with open(compiled_contract_path) as file:
                contract_json = json.load(file)  # load contract info as JSON
                contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
            c = 0
            contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
            blocknumber = web3.eth.get_block_number()
            for i in range(blocknumber, 3, -1):
                a = web3.eth.get_transaction_by_block(i, 0)
                decoded_input = contract.decode_function_input(a['input'])
                if str(decoded_input[1]['product_name']) == product_name and str(
                        decoded_input[1]['quantity']) == quantity and str(
                        decoded_input[1]['mdate']) == manufacture_date and str(
                        decoded_input[1]['price']) == manufacture_rate and str(
                        decoded_input[1]['expire_date']) == expire_date:
                    c += 1
                else:
                    c = c
            if c == 0:
                message2 = contract.functions.addProduct(blocknumber + 1, product_name, quantity, manufacture_date,
                                                         manufacture_rate, expire_date, str(path),
                                                         (session['lid'])).transact()

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
                img.save(
                    r"C:\Users\ssree\PycharmProjects\couterfeitproduct\static\qrcode_image\\" + datetime.datetime.now().strftime(
                        "%Y%m%d%H%M%S") + product_name + "image.jpg")
                return ''' <script> alert("Inserted...!!!!");window.location="/mfc_addproduct" </script>   '''
            else:
                return ''' <script> alert("Already Inserted...!!!!");window.location="/mfc_addproduct" </script>   '''





            # ============================================================================================


        else:
            return render_template("manufacture/productmanagement.html")
    else:
        return redirect("/")


@app.route('/mfc_viewproduct')
def mfc_viewproduct():
    if session['log'] == "lo":
        # db=Db()
        # res=db.select("select * from product WHERE product.manufacture_id='"+str(session['lid'])+"'")


        data = []
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)  # load contract info as JSON
            contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        blocknumber = web3.eth.get_block_number()
        # print(blocknumber)
        for i in range(blocknumber, 2, -1):
            a = web3.eth.get_transaction_by_block(i, 0)
            decoded_input = contract.decode_function_input(a['input'])
            res = {}
            res['product_name'] = decoded_input[1]['product_name']
            res['image'] = decoded_input[1]['image']
            res['quantity'] = decoded_input[1]['quantity']
            res['manufacture_date'] = decoded_input[1]['mdate']
            res['manufacture_rate'] = decoded_input[1]['price']
            res['expire_date'] = decoded_input[1]['expire_date']
            res['manufacture_id'] = decoded_input[1]['mid']
            if str(decoded_input[1]['mid']) == str(session['lid']):
                data.append(res)

        return render_template("manufacture/viewproduct.html", data=data)
    else:
        return redirect('/')


@app.route('/mfc_viewspam')
def mfc_viewspam():
    if session['log'] == "lo":
        db = Db()
        res = db.select("select * from spam,`user` where spam.user_id=`user`.user_id ")
        return render_template("manufacture/viewspam.html", data=res)
    else:
        return redirect('/')


@app.route('/')
def index():
    # if session['log'] == "lo":

    return render_template("index.html")
    # else:
    #     return redirect('/')


@app.route('/logout')
def Logout():
    if session['log'] == "lo":
        session['log'] = ""
        return redirect('/')
    else:
        return redirect('/')


#############################ANDROID#############################
@app.route('/Register', methods=['post'])
def Register():
    db = Db()
    name = request.form['ab']
    email = request.form['cb']
    phone_no = request.form['eb']
    password = request.form['gb']
    res = db.insert("insert into login values ('','" + email + "','" + password + "','user')")
    db.insert("insert into user values('" + str(res) + "','" + name + "','" + email + "','" + phone_no + "')")
    return jsonify(status="ok")


@app.route('/login1', methods=['post'])
def login1():
    un = request.form['u']
    ps = request.form['p']
    db = Db()
    res = db.selectOne("select * from login WHERE username='" + un + "'and password='" + ps + "'")
    if res is not None:
        if res['usertype'] == 'user':
            return jsonify(status="ok", lid=res['loginid'], type=res['usertype'])
        else:
            return jsonify(status="no")
    else:
        return jsonify(status="no")


@app.route('/sentcomplaintuser', methods=['post'])
def sentcomplaintuser():
    lid = request.form['lid']
    co = request.form['comp']
    db = Db()
    db.insert("insert into complaint values('','" + lid + "','" + co + "',curdate(),'pending','pending')")
    return jsonify(status="ok")


@app.route('/view_complaint', methods=['post'])
def viewcomplaint():
    lid = request.form['lid']
    db = Db()
    res = db.select("select * from complaint where user_id='" + lid + "'")
    return jsonify(status="ok", data=res)


@app.route('/view_productdetails', methods=['post'])
def view_productdetails():
    db = Db()
    res = db.select("select * from product,manufacture where product.manufacture_id=manufacture.manufacture_loginid")
    print(res)

    return jsonify(status="ok", data=res)


@app.route('/sentasspam', methods=['post'])
def sentasspam():
    lid = request.form['lid']
    s = request.form['s']
    im = request.files['pic']
    dt = time.strftime("%Y%m%d_%H%M%S")
    im.save(static_path + "manufacture_img\\" + dt + ".jpg")
    path = "/static/manufacture_img/" + dt + ".jpg"
    db = Db()
    db.insert("insert into spam values('','" + lid + "','" + s + "','" + str(path) + "',curdate())")
    return jsonify(status="ok")


@app.route('/and_view_qrproduct', methods=['post', 'get'])
def and_view_qrproduct():
    try:
        b = request.form['contents']
        q = AESCipher("cp")
        b = q.decrypt(b)
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)  # load contract info as JSON
            contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        blocknumber = web3.eth.get_block_number()
        count = 0
        for i in range(blocknumber, 2, -1):
            a = web3.eth.get_transaction_by_block(i, 0)
            decoded_input = contract.decode_function_input(a['input'])
            print(decoded_input)
            if str(decoded_input[1]['bid']) == b:
                # db=Db()
                # q=db.selectOne("select * from company where ins_id='"+str(decoded_input[1]['mid'])+"'")
                return jsonify(status="ok", product_name=str(decoded_input[1]['product_name']),
                               quantity=decoded_input[1]['quantity'], manufacture_date=decoded_input[1]['mdate'],
                               manufacture_rate=decoded_input[1]['price'], expire_date=decoded_input[1]['expire_date'],
                               image=decoded_input[1]['image'])
            else:
                count = count + 1
        if count > 0:
            return jsonify(status="none")
    except Exception as e:
        return jsonify(status="none")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
