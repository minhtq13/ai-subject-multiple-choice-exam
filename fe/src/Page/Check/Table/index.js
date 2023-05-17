import { Table } from "antd";
import "./Table.css";

export default function TableCheck({ data }) {
  const cau = () => {
    const array = [];
    let j = 0;
    for (let i = 1; i < 121; i++) {
      let check = data.diem[j] === i;
      array.push({
        title: i.toString(),
        dataIndex: i.toString(),
        key: i.toString(),
        width: 50,
        render: (value) => (
          <div className={check === true ? "true" : "false"}>{value}</div>
        ),
      });
      if (check === true) j++;
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
      title: "SBD",
      dataIndex: "SBD",
      key: "SBD",
      width: 100,
      fixed: "left",
    },
    {
      title: "CAU",
      children: cau(),
    },
    {
      title: "DIEM",
      dataIndex: "DIEM",
      key: "DIEM",
      width: 200,
      fixed: "right",
    },
  ];
  const dataSource = [...data.da, ...data.kq];
  return (
    <Table
      columns={columns}
      dataSource={dataSource}
      bordered
      size="middle"
      scroll={{
        x: "calc(700px + 50%)",
        y: 240,
      }}
    />
  );
}
