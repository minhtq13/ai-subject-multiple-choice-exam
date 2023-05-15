import Header from "../component/Header";

export default function OnlyHeaderLayout({ children }) {
  return (
    <div>
      <Header />
      <div>{children}</div>
    </div>
  );
}
