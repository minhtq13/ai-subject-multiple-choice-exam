import { Switch } from "antd";
import CheckBox from "./Checkbox";
import { useState } from "react";
import "./Home.css";
import ImageUpload from "./ImageUpload";
import TableDA from "./Table";

export default function Home() {
  const [choose, setChoose] = useState(false);
  const [result, setResult] = useState();
  const changeMode = () => {
    setResult();
    setChoose(!choose);
  };
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
      {result && <TableDA data={result} />}
    </div>
  );
}
