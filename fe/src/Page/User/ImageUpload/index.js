import { UploadOutlined } from "@ant-design/icons";
import { Alert, Button, Form, InputNumber, Space, Upload } from "antd";
import { postChamDiem } from "../../../api";
import { useState } from "react";
import Loading from "../../../Layout/component/Loading";

export default function ImageUpload() {
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

  const normFile = (e) => {
    setResult();
    if (Array.isArray(e)) {
      return e;
    }
    return e?.fileList;
  };

  const onFinish = async (values) => {
    setLoading(true);
    const res = await postChamDiem({
      img: values.upload[0].response.result,
      id: values.ID,
    });
    setResult(res);
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
      {result && (
        <Alert
          message={`Success diem: ${result.data?.kq}, id: ${result.data?.result?.id}`}
          type="success"
          style={{ margin: "10px" }}
        />
      )}

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
