import { UploadOutlined } from "@ant-design/icons";
import { Button, Form, InputNumber, Space, Upload } from "antd";

const formItemLayout = {
  labelCol: {
    span: 6,
  },
  wrapperCol: {
    span: 14,
  },
};

const normFile = (e) => {
  console.log("Upload event:", e);
  if (Array.isArray(e)) {
    return e;
  }
  return e?.fileList;
};

const onFinish = async (values) => {
  console.log("Received values of form: ", values);
};

export default function ImageUpload() {
  return (
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
      <Form.Item label="MA DE THI">
        <Form.Item name="MDT" noStyle>
          <InputNumber style={{ margin: "0px 10px" }} min={0} max={999} />
        </Form.Item>
      </Form.Item>
      <Form.Item label="MA DE THI">
        <Form.Item name="MDT" noStyle>
          <InputNumber style={{ margin: "0px 10px" }} min={0} max={999} />
        </Form.Item>
      </Form.Item>

      <Form.Item
        name="upload"
        label="Upload"
        valuePropName="fileList"
        getValueFromEvent={normFile}
        extra="Img"
      >
        <Upload name="logo" action="/upload.do" listType="picture">
          <Button icon={<UploadOutlined />}>Click to upload</Button>
        </Upload>
      </Form.Item>

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
