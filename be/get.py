import sqlite3

def check(data1, data2):
    dung = []
    j = 0
    for data in data2:
        dung.append([])
        for i in range(1, 121):
            if data1[0][i + 1] == data[i + 2] or data1[0][i + 1] == '':
                dung[j].append(True)
            else:
                dung[j].append(False)
        j = j + 1
    return dung

def get_all(sql):
    conn = sqlite3.connect("./be/Database.db")
    data = conn.execute(sql).fetchall()
    conn.close()

    return data

def get_by_id(id):
    conn = sqlite3.connect("./be/Database.db")
    data = conn.execute("SELECT * FROM bailam WHERE id = ?", [id]).fetchall()
    conn.commit()
    conn.close()
    return data

def get_check_by_id(id):
    conn = sqlite3.connect("./be/Database.db")
    data1 = conn.execute("SELECT * FROM bailam WHERE id = ?", [id]).fetchall()
    data2 = conn.execute("SELECT * FROM bailam WHERE id = ?", [data1[0][124]]).fetchall()
    dung = check(data1, data2)
    conn.commit()
    conn.close()
    return data1, data2, dung

def get_check_by_mdt(mdt, sbd):
    conn = sqlite3.connect("./be/Database.db")
    if sbd == None:
        data1 = conn.execute("SELECT * FROM dapan WHERE MDT = ?", [mdt]).fetchall()
        data2 = conn.execute("SELECT * FROM bailam WHERE MDT = ?", [mdt]).fetchall()
    if mdt == None:
        data2 = conn.execute("SELECT * FROM bailam WHERE SBD = ?", [sbd]).fetchall()
        data1 = conn.execute("SELECT * FROM dapan WHERE MDT = ?", [data2[0][2]]).fetchall()
    if sbd != None and mdt != None:
        data1 = conn.execute("SELECT * FROM dapan WHERE MDT = ?", [mdt]).fetchall()
        data2 = conn.execute("SELECT * FROM bailam WHERE MDT = ? AND SBD = ?", [mdt, sbd]).fetchall()
    dung = check(data1, data2)
    conn.commit()
    conn.close()
    return data1, data2, dung

def get_by_mdt(mdt, sbd):
    conn = sqlite3.connect("./be/Database.db")
    data = conn.execute("SELECT * FROM bailam WHERE MDT = ? AND SBD = ?", [mdt, sbd]).fetchall()
    conn.commit()
    conn.close()
    return data

if __name__ == "__main__":
    print(get_by_id(1))