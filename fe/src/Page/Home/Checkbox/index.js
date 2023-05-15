import { Button, Form, InputNumber, Radio, Space } from "antd";

const formItemLayout = {
  labelCol: {
    span: 6,
  },
  wrapperCol: {
    span: 14,
  },
};

const onFinish = (values) => {
  console.log("Received values of form: ", values);
};

export default function CheckBox() {
  return (
    <Form
      name="validate_other"
      {...formItemLayout}
      onFinish={onFinish}
      initialValues={{
        "input-number": 0,
      }}
      style={{
        maxWidth: 600,
      }}
    >
      <Form.Item label="MA DE THI">
        <Form.Item name="input-number" noStyle>
          <InputNumber min={0} max={999} />
        </Form.Item>
      </Form.Item>

      {new Array(120).fill(0).map((_, index) => (
        <Form.Item
          key={index}
          name={`cau${index + 1}`}
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
