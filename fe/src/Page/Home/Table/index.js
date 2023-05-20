import { Table } from "antd";
import "./Table.css";

export default function TableDA({ data }) {
  const cau = () => {
    const array = [];
    for (let i = 1; i < 121; i++) {
      array.push({
        title: i.toString(),
        dataIndex: i.toString(),
        key: i.toString(),
        width: 50,
      });
    }
    return array;
  };
  const columns = [
    {
      title: "MDT",
      dataIndex: "MDT",
      key: "MDT",
      width: 100,
      fixed: "left",
    },
    {
      title: "CAU",
      children: cau(),
    },
  ];
  return (
    <Table
      columns={columns}
      dataSource={[data]}
      bordered
      size="middle"
      scroll={{
        x: "calc(700px + 50%)",
        y: 240,
      }}
    />
  );
}
