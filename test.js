const adb = require("adbkit");
const { exec } = require("child_process");
const axios = require("axios");

const client = adb.createClient();
const REPORT_URL = "http://127.0.0.1:5100/api/report";
const DISCONNECT_URL = "http://127.0.0.1:5100/api/disconnect";
const connectedDevices = {};

async function handleNewDevice(device) {
  if (connectedDevices[device.id]) {
    console.log(`设备 ${device.id} 已经连接，跳过`);
    return;
  }

  console.log(`😍😍设备: ${device.id} 连接中...`);

  try {
    const tcpPort = Math.floor(Math.random() * (65535 - 1024 + 1)) + 1024;
    const server = await client.createTcpUsbBridge(device.id, {
      auth: () => Promise.resolve(),
    });
    await server.listen(tcpPort);

    console.log(`设备 ${device.id} 已映射到 TCP 端口: ${tcpPort}。`);

    const reportData = { deviceId: device.id, tcpPort };
    connectedDevices[device.id] = { ...reportData, server };

    await axios.post(REPORT_URL, reportData);
    console.log(`成功上报设备 ${device.id} 和端口 ${tcpPort}`);
  } catch (err) {
    console.error(`处理设备 ${device.id} 时发生错误: ${err.message}`);
  }
}

async function handleDisconnectedDevice(device) {
  console.log(`设备: ${device.id} 断开连接中...`);

  if (connectedDevices[device.id]) {
    const reportData = connectedDevices[device.id];
    const { tcpPort } = reportData;
    delete connectedDevices[device.id];

    try {
      await axios.post(DISCONNECT_URL, { deviceId: device.id, tcpPort });
      console.log(`成功上报设备 ${device.id} 断开连接，端口 ${tcpPort}`);
    } catch (err) {
      console.error(`上报断开连接错误: ${err.message}`);
    } finally {
      console.log(`断开连接的端口号: ${tcpPort}`);
    }

    if (reportData.server) {
      reportData.server.close();
      console.log(`设备 ${device.id} 已清理`);
    }
  } else {
    console.log(`设备 ${device.id} 不在已连接设备列表中，跳过清理`);
  }
}

async function main() {
  let tracker;

  const restartTracker = async () => {
    console.log("重新启动设备追踪...");
    try {
      if (tracker) {
        tracker.removeAllListeners(); // 清除所有监听器
      }
      tracker = await client.trackDevices();
      tracker.on("add", handleNewDevice);
      tracker.on("remove", handleDisconnectedDevice);
      tracker.on("error", handleError);
      tracker.on("end", () => {
        console.log("设备追踪结束");
      });
      console.log("设备追踪已重启");
    } catch (err) {
      console.error("重新启动设备追踪时发生错误:", err.message);
    }
  };

  const handleError = async (err) => {
    console.error("追踪设备时发生错误:", err.message);
    if (err.message.includes("Connection closed")) {
      await restartTracker();
    }
  };

  try {
    console.log("正在开始监控设备连接状态...");
    tracker = await client.trackDevices();
    tracker.on("add", handleNewDevice);
    tracker.on("remove", handleDisconnectedDevice);
    tracker.on("error", handleError);
    tracker.on("end", () => {
      console.log("设备追踪结束");
    });
  } catch (err) {
    console.error("发生错误:", err.message);
  }
}

main();
