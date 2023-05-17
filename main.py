import os
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from be import get, post
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def show(rows):
    data = []
    for r in rows:
        data.append({
            "id": r[0],
            "SBD": r[1],
            "MDT": r[2],
            "1": r[3],
            "2": r[4],
            "3": r[5],
            "4": r[6],
            "5": r[7],
            "6": r[8],
            "7": r[9],
            "8": r[10],
            "9": r[11],
            "10": r[12],
            "11": r[13],
            "12": r[14],
            "13": r[15],
            "14": r[16],
            "15": r[17],
            "16": r[18],
            "17": r[19],
            "18": r[20],
            "19": r[21],
            "20": r[22],
            "21": r[23],
            "22": r[24],
            "23": r[25],
            "24": r[26],
            "25": r[27],
            "26": r[28],
            "27": r[29],
            "28": r[30],
            "29": r[31],
            "30": r[32],
            "31": r[33],
            "32": r[34],
            "33": r[35],
            "34": r[36],
            "35": r[37],
            "36": r[38],
            "37": r[39],
            "38": r[40],
            "39": r[41],
            "40": r[42],
            "41": r[43],
            "42": r[44],
            "43": r[45],
            "44": r[46],
            "45": r[47],
            "46": r[48],
            "47": r[49],
            "48": r[50],
            "49": r[51],
            "50": r[52],
            "51": r[53],
            "52": r[54],
            "53": r[55],
            "54": r[56],
            "55": r[57],
            "56": r[58],
            "57": r[59],
            "58": r[60],
            "59": r[61],
            "60": r[62],
            "61": r[63],
            "62": r[64],
            "63": r[65],
            "64": r[66],
            "65": r[67],
            "66": r[68],
            "67": r[69],
            "68": r[70],
            "69": r[71],
            "70": r[72],
            "71": r[73],
            "72": r[74],
            "73": r[75],
            "74": r[76],
            "75": r[77],
            "76": r[78],
            "77": r[79],
            "78": r[80],
            "79": r[81],
            "80": r[82],
            "81": r[83],
            "82": r[84],
            "83": r[85],
            "84": r[86],
            "85": r[87],
            "86": r[88],
            "87": r[89],
            "88": r[90],
            "89": r[91],
            "90": r[92],
            "91": r[93],
            "92": r[94],
            "93": r[95],
            "94": r[96],
            "95": r[97],
            "96": r[98],
            "97": r[99],
            "98": r[100],
            "99": r[101],
            "100": r[102],
            "101": r[103],
            "102": r[104],
            "103": r[105],
            "104": r[106],
            "105": r[107],
            "106": r[108],
            "107": r[109],
            "108": r[110],
            "109": r[111],
            "110": r[112],
            "111": r[113],
            "112": r[114],
            "113": r[115],
            "114": r[116],
            "115": r[117],
            "116": r[118],
            "117": r[119],
            "118": r[120],
            "119": r[121],
            "120": r[122],
            "DIEM": r[123],
            "ID_check": r[124]
        })
    return data

@app.route("/getAll", methods=['GET'])
@cross_origin(origin='*')
def getAllApi():
    rows = get.get_all("SELECT * FROM bailam")
    data = show(rows)
    return jsonify({"result": data})

@app.route("/getById", methods=['GET'])
@cross_origin(origin='*')
def getById():
    id = request.args.get("id")
    rows = get.get_by_id(id)
    data = show(rows)
    return jsonify({"result": data})

@app.route("/check", methods=['GET'])
@cross_origin(origin='*')
def getCheck():
    mdt = request.args.get("MDT")
    sbd = request.args.get("SBD")
    rows = get.get_by_mdt(mdt, sbd)
    data = show(rows)
    return jsonify({"result": data})

@app.route("/getCheckById", methods=['GET'])
@cross_origin(origin='*')
def getCheckById():
    id = request.args.get("id")
    data1, data2, dung = get.get_check_by_id(id)
    kq = show(data1)
    da = show(data2)
    return jsonify({"kq": kq, "da": da, "diem": dung})


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file-upload', methods=['POST'])
@cross_origin(origin='*')
def upload():
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        now = datetime.now()
        filename = secure_filename(file.filename)
        print(now.strftime("%d_%m_%Y_%H_%M_%S") + filename)
        file.save(os.path.join("./be/images", now.strftime("%d_%m_%Y_%H_%M_%S") + filename))
        resp = jsonify({'message' : 'File successfully uploaded', "result": now.strftime("%d_%m_%Y_%H_%M_%S") + filename})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp

@app.route("/api", methods=['POST'])
@cross_origin(origin='*')
def postApi():
    img = request.args.get("img")
    if(img):
        rows = post.postKT(img)
        data = []
        for r in rows:
            data.append({
                "id": r[0]
            })
        return jsonify({"status": 1, "message": "Successful", "result": data[len(data)-1] })
    return jsonify({"status": -1, "message": "Fail"})

@app.route("/cham", methods=['POST'])
@cross_origin(origin='*')
def postCham():
    img = request.args.get("img")
    id = request.args.get("id")
    if(img):
        rows, dung = post.postChamDiem(img, id)
        data = []
        for r in rows:
            data.append({
                "id": r[0]
            })
        return jsonify({"status": 1, "message": "Successful", "result": data[len(data)-1], "kq": len(dung)/12 })
    return jsonify({"status": -1, "message": "Fail"})

@app.route("/getApi", methods=['POST'])
@cross_origin(origin='*')
def postGetApi():
    SBD = request.args.get("SBD")

    MDT = request.args.get("MDT")

    c1 = request.args.get("c1")

    c2 = request.args.get("c2")

    c3 = request.args.get("c3")

    c4 = request.args.get("c4")

    c5 = request.args.get("c5")

    c6 = request.args.get("c6")

    c7 = request.args.get("c7")

    c8 = request.args.get("c8")

    c9 = request.args.get("c9")

    c10 = request.args.get("c10")

    c11 = request.args.get("c11")

    c12 = request.args.get("c12")

    c13 = request.args.get("c13")

    c14 = request.args.get("c14")

    c15 = request.args.get("c15")

    c16 = request.args.get("c16")

    c17 = request.args.get("c17")

    c18 = request.args.get("c18")

    c19 = request.args.get("c19")

    c20 = request.args.get("c20")

    c21 = request.args.get("c21")

    c22 = request.args.get("c22")

    c23 = request.args.get("c23")

    c24 = request.args.get("c24")

    c25 = request.args.get("c25")

    c26 = request.args.get("c26")

    c27 = request.args.get("c27")

    c28 = request.args.get("c28")

    c29 = request.args.get("c29")

    c30 = request.args.get("c30")

    c31 = request.args.get("c31")

    c32 = request.args.get("c32")

    c33 = request.args.get("c33")

    c34 = request.args.get("c34")

    c35 = request.args.get("c35")

    c36 = request.args.get("c36")

    c37 = request.args.get("c37")

    c38 = request.args.get("c38")

    c39 = request.args.get("c39")

    c40 = request.args.get("c40")

    c41 = request.args.get("c41")

    c42 = request.args.get("c42")

    c43 = request.args.get("c43")

    c44 = request.args.get("c44")

    c45 = request.args.get("c45")

    c46 = request.args.get("c46")

    c47 = request.args.get("c47")

    c48 = request.args.get("c48")

    c49 = request.args.get("c49")

    c50 = request.args.get("c50")

    c51 = request.args.get("c51")

    c52 = request.args.get("c52")

    c53 = request.args.get("c53")

    c54 = request.args.get("c54")

    c55 = request.args.get("c55")

    c56 = request.args.get("c56")

    c57 = request.args.get("c57")

    c58 = request.args.get("c58")

    c59 = request.args.get("c59")

    c60 = request.args.get("c60")

    c61 = request.args.get("c61")

    c62 = request.args.get("c62")

    c63 = request.args.get("c63")

    c64 = request.args.get("c64")

    c65 = request.args.get("c65")

    c66 = request.args.get("c66")

    c67 = request.args.get("c67")

    c68 = request.args.get("c68")

    c69 = request.args.get("c69")

    c70 = request.args.get("c70")

    c71 = request.args.get("c71")

    c72 = request.args.get("c72")

    c73 = request.args.get("c73")

    c74 = request.args.get("c74")

    c75 = request.args.get("c75")

    c76 = request.args.get("c76")

    c77 = request.args.get("c77")

    c78 = request.args.get("c78")

    c79 = request.args.get("c79")

    c80 = request.args.get("c80")

    c81 = request.args.get("c81")

    c82 = request.args.get("c82")

    c83 = request.args.get("c83")

    c84 = request.args.get("c84")

    c85 = request.args.get("c85")

    c86 = request.args.get("c86")

    c87 = request.args.get("c87")

    c88 = request.args.get("c88")

    c89 = request.args.get("c89")

    c90 = request.args.get("c90")

    c91 = request.args.get("c91")

    c92 = request.args.get("c92")

    c93 = request.args.get("c93")

    c94 = request.args.get("c94")

    c95 = request.args.get("c95")

    c96 = request.args.get("c96")

    c97 = request.args.get("c97")

    c98 = request.args.get("c98")

    c99 = request.args.get("c99")

    c100 = request.args.get("c100")

    c101 = request.args.get("c101")

    c102 = request.args.get("c102")

    c103 = request.args.get("c103")

    c104 = request.args.get("c104")

    c105 = request.args.get("c105")

    c106 = request.args.get("c106")

    c107 = request.args.get("c107")

    c108 = request.args.get("c108")

    c109 = request.args.get("c109")

    c110 = request.args.get("c110")

    c111 = request.args.get("c111")

    c112 = request.args.get("c112")

    c113 = request.args.get("c113")

    c114 = request.args.get("c114")

    c115 = request.args.get("c115")

    c116 = request.args.get("c116")

    c117 = request.args.get("c117")

    c118 = request.args.get("c118")

    c119 = request.args.get("c119")

    c120 = request.args.get("c120")

    if(SBD):
        post.postGet(SBD, MDT, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, c20, c21, c22, c23, c24, c25, c26, c27, c28, c29, c30, c31, c32, c33, c34, c35, c36, c37, c38, c39, c40, c41, c42, c43, c44, c45, c46, c47, c48, c49, c50, c51, c52, c53, c54, c55, c56, c57, c58, c59, c60, c61, c62, c63, c64, c65, c66, c67, c68, c69, c70, c71, c72, c73, c74, c75, c76, c77, c78, c79, c80, c81, c82, c83, c84, c85, c86, c87, c88, c89, c90, c91, c92, c93, c94, c95, c96, c97, c98, c99, c100, c101, c102, c103, c104, c105, c106, c107, c108, c109, c110, c111, c112, c113, c114, c115, c116, c117, c118, c119, c120)
        return jsonify({"status": 1, "message": "Successful"})
    return jsonify({"status": -1, "message": "Fail"})

if __name__ == "__main__":
    app.run()