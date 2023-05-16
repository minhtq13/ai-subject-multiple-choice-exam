import { Switch } from "antd";
import CheckBox from "./Checkbox";
import { useState } from "react";
import "./User.css";
import ImageUpload from "./ImageUpload";

export default function User() {
  const [choose, setChoose] = useState(false);
  const changeMode = () => {
    setChoose(!choose);
  };
  return (
    <div className="wrapper">
      <div className="switch">
        Change Mode: <Switch onChange={changeMode} />
      </div>
      {!choose ? <CheckBox /> : <ImageUpload />}
    </div>
  );
}
