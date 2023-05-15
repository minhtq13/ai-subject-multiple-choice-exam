export default function DefaultLayout({ children }) {
  return (
    <div>
      <div className="container">
        <div className="content">{children}</div>
      </div>
    </div>
  );
}
