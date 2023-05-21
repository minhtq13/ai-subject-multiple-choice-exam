import { Link, useLocation } from "react-router-dom";
import "./Header.css";
import { Tabs } from "antd";

export default function Header() {
  let location = useLocation();
  const items = [
    {
      key: "1",
      label: (
        <Link className="link" to="/">
          Đáp Án
        </Link>
      ),
    },
    {
      key: "2",
      label: (
        <Link className="link" to="/submit">
          Bài Thi
        </Link>
      ),
    },
    {
      key: "3",
      label: (
        <Link className="link" to="/check">
          Xem Chi Tiết
        </Link>
      ),
    },
  ];
  const activeKey = () => {
    switch (location.pathname) {
      case "/":
        return "1";
      case "/submit":
        return "2";
      case "/check":
        return "3";
      default:
        return "1";
    }
  };
  return (
    <div className="header">
      <Tabs defaultActiveKey={activeKey()} type="card" items={items} />
    </div>
  );
}
