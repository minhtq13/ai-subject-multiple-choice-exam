import { Link, useLocation } from "react-router-dom";
import "./Header.css";

export default function Header() {
  let location = useLocation();
  const navs = [
    {
      text: "DAP AN",
      router: "/",
    },
    {
      text: "BAI THI",
      router: "/submit",
    }
  ];
  return (
    <div className="header">
      {navs.map((nav, index) => (
        <Link
          className={"nav"}
          style={{
            backgroundColor:
              location.pathname === nav.router ? "#ccc" : "transparent",
          }}
          key={index}
          to={nav.router}
        >
          {nav.text}
        </Link>
      ))}
    </div>
  );
}
