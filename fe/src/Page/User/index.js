import { Switch } from "antd";
import CheckBox from "./Checkbox";
import { useState } from "react";
import "./User.css";
import ImageUpload from "./ImageUpload";
import TableBL from "./Table";

export default function User() {
  const [choose, setChoose] = useState(false);
  const [result, setResult] = useState();
  const changeMode = () => {
    setResult();
    setChoose(!choose);
  };
  console.log(result);
  return (
    <div className="wrapper">
      <div className="switch" style={{ color: "#1677ff" }}>
        Chuyển kiểu nhập dữ liệu: <Switch onChange={changeMode} />
      </div>
      {!choose ? (
        <CheckBox setResult={setResult} />
      ) : (
        <ImageUpload setResult={setResult} />
      )}
      {result && <TableBL data={result} />}
    </div>
  );
}
