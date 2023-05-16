import { Button, Form, InputNumber, Radio, Space } from "antd";
import "./Checkbox.css";
import { postForm } from "../../../api";

const formItemLayout = {
  labelCol: {
    span: 6,
  },
  wrapperCol: {
    span: 14,
  },
};

const onFinish = async (values) => {
  await postForm(values);
  console.log("Received values of form: ", values);
};

export default function CheckBox() {
  return (
    <Form
      name="validate_other"
      {...formItemLayout}
      onFinish={onFinish}
      initialValues={{
        MDT: 0,
      }}
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
      <Form.Item label="MA DE THI">
        <Form.Item name="MDT" noStyle>
          <InputNumber style={{ margin: "0px 10px" }} min={0} max={999} />
        </Form.Item>
      </Form.Item>

      <div className="formInput">
        {new Array(120).fill(0).map((_, index) => (
          <Form.Item
            key={index}
            name={`c${index + 1}`}
            label={`Cau ${index + 1}`}
          >
            <Radio.Group>
              <Radio value="a">A</Radio>
              <Radio value="b">B</Radio>
              <Radio value="c">C</Radio>
              <Radio value="d">D</Radio>
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
          <Button type="primary" htmlType="submit">
            Submit
          </Button>
          <Button htmlType="reset">reset</Button>
        </Space>
      </Form.Item>
    </Form>
  );
}
