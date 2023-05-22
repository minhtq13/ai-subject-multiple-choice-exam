import { Image, Table } from "antd";
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
      title: "Câu",
      children: cau(),
    },
    {
      title: "Điểm",
      dataIndex: "DIEM",
      key: "DIEM",
      width: 200,
      fixed: "right",
    },
    {
      title: "Ảnh",
      dataIndex: "img",
      key: "img",
      width: 200,
      fixed: "right",
      render: (text) =>
        text && <Image width={200} src={require(`../../../images/${text}`)} />,
    },
  ];
  const dataSource = [...data.da, ...data.bl];
  return (
    <div>
      <Table
        columns={columns}
        dataSource={dataSource}
        bordered
        size="middle"
        scroll={{
          x: "calc(700px + 50%)",
          y: 2000,
        }}
      />
    </div>
  );
}
