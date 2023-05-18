import { Button, Form, InputNumber, Space } from "antd";
import { useState } from "react";
import Loading from "../../Layout/component/Loading";
import { getCheckById } from "../../api";
import TableCheck from "./Table";

export default function Check() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState();
  const formItemLayout = {
    labelCol: {
      span: 6,
    },
    wrapperCol: {
      span: 14,
    },
  };

  const onFinish = async (values) => {
    setLoading(true);
    const res = await getCheckById(values.ID);
    setResult(res);
    setLoading(false);
  };
  return (
    <div>
      <p style={{ margin: "20px", textAlign: "center" }}>XEM CHI TIET KET QUA CUA BAN</p>
      <Form
        name="validate_other"
        {...formItemLayout}
        onFinish={onFinish}
        initialValues={{
          "input-number": 0,
        }}
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Form.Item label="ID">
          <Form.Item name="ID" noStyle>
            <InputNumber style={{ margin: "0px 10px" }} min={0} max={999} />
          </Form.Item>
        </Form.Item>

        <Form.Item
          wrapperCol={{
            span: 12,
            offset: 6,
          }}
        >
          <Space>
            <Button
              type="primary"
              htmlType="submit"
              disabled={loading}
              style={{ width: "100px" }}
            >
              {!loading ? "Submit" : <Loading />}
            </Button>
            <Button htmlType="reset">reset</Button>
          </Space>
        </Form.Item>
      </Form>
      {result && (
        <div>
          <div>So cau dung: {result.diem.length}</div>
          <TableCheck data={result} />
        </div>
      )}
    </div>
  );
}
