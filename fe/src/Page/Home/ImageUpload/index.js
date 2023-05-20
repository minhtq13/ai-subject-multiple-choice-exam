import { UploadOutlined } from "@ant-design/icons";
import { Button, Form, Space, Upload } from "antd";
import { postDAimg } from "../../../api";
import { useState } from "react";
import Loading from "../../../Layout/component/Loading";

export default function ImageUpload({ setResult }) {
  const [loading, setLoading] = useState(false);
  const formItemLayout = {
    labelCol: {
      span: 6,
    },
    wrapperCol: {
      span: 14,
    },
  };

  const normFile = (e) => {
    if (Array.isArray(e)) {
      return e;
    }
    return e?.fileList;
  };

  const onFinish = async (values) => {
    setLoading(true);
    const res = await postDAimg({ img: values.upload[0].response.result });
    setResult(res?.data?.result);
    setLoading(false);
  };
  return (
    <Form
      name="validate_other"
      {...formItemLayout}
      onFinish={onFinish}
      initialValues={{
        "input-number": 0,
      }}
      onChange={() => {
        setResult();
      }}
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
      autoComplete="off"
    >
      <Form.Item
        name="upload"
        label="Upload"
        valuePropName="fileList"
        getValueFromEvent={normFile}
        extra="Img"
      >
        <Upload
          name="file"
          action="http://127.0.0.1:5000/file-upload"
          listType="picture"
          maxCount={1}
        >
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
