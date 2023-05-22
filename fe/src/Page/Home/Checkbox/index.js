import { Button, Form, InputNumber, Radio, Space } from "antd";
import "./Checkbox.css";
import { postDA } from "../../../api";
import { useState } from "react";
import Loading from "../../../Layout/component/Loading";

const formItemLayout = {
  labelCol: {
    span: 6,
  },
  wrapperCol: {
    span: 14,
  },
};

export default function CheckBox({ setResult }) {
  const [loading, setLoading] = useState(false);

  const onFinish = async (values) => {
    setLoading(true);
    const res = await postDA(values);
    setResult(res?.data?.result);
    setLoading(false);
  };
  return (
    <Form
      name="validate_other"
      {...formItemLayout}
      onFinish={onFinish}
      initialValues={{}}
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
      <Form.Item label="MDT">
        <Form.Item name="MDT" noStyle>
          <InputNumber style={{ margin: "0px 10px" }} min={0} max={999} />
        </Form.Item>
      </Form.Item>

      <div className="formInput">
        {new Array(120).fill(0).map((_, index) => (
          <Form.Item
            key={index}
            name={`c${index + 1}`}
            label={`Câu ${index + 1}`}
          >
            <Radio.Group>
              <Radio value="A">A</Radio>
              <Radio value="B">B</Radio>
              <Radio value="C">C</Radio>
              <Radio value="D">D</Radio>
            </Radio.Group>
          </Form.Item>
        ))}
      </div>

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
  );
}
