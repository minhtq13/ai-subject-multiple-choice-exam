import { Table } from "antd";
import "./Table.css";

export default function TableCheck({ data }) {
  const cau = () => {
    const array = [];
    for (let i = 1; i < 121; i++) {
      array.push({
        title: i.toString(),
        dataIndex: i.toString(),
        key: i.toString(),
        width: 50,
        render: (text, _, index) => (
          <div
            className={
              index > 0
                ? data.diem[index - 1][i - 1]
                  ? "true"
                  : "false"
                : "warning"
            }
          >
            {text}
          </div>
        ),
      });
    }

    return array;
  };
  const columns = [
    {
      title: "MĐT",
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
      title: "Điểm",
      dataIndex: "DIEM",
      key: "DIEM",
      width: 200,
      fixed: "right",
    },
  ];
  const dataSource = [...data.da, ...data.bl];
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
