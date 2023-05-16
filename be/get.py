import sqlite3


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

def get_by_mdt(mdt, sbd):
    conn = sqlite3.connect("./be/Database.db")
    data = conn.execute("SELECT * FROM bailam WHERE MDT = ? AND SBD = ?", [mdt, sbd]).fetchall()
    conn.commit()
    conn.close()
    return data

if __name__ == "__main__":
    print(get_by_id(1))