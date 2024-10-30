const adb = require('adbkit');
const { exec } = require('child_process');

const client = adb.createClient();
const connectedDevices = {};

function getRandomPort(usedPorts) {
  let port;
  do {
    port = Math.floor(Math.random() * (65535 - 1024 + 1)) + 1024;
  } while (usedPorts.has(port));
  return port;
}

async function disconnectOfflineDevices() {
  return new Promise((resolve, reject) => {
    exec('adb devices', (error, stdout) => {
      if (error) {
        console.error(`获取设备列表时发生错误: ${error.message}`);
        return reject(error);
      }

      const lines = stdout.split('\n');
      const offlineDevices = lines.filter(line => line.includes('offline')).map(line => line.split('\t')[0]);

      if (offlineDevices.length > 0) {
        offlineDevices.forEach(deviceId => {
          exec(`adb disconnect ${deviceId}`, (err) => {
            if (err) {
              console.error(`断开设备 ${deviceId} 失败: ${err.message}`);
            } else {
              console.log(`已断开设备 ${deviceId}`);
            }
          });
        });
      }
      resolve();
    });
  });
}

async function tcpIpConnect(deviceId) {
  return new Promise((resolve, reject) => {
    exec(`adb -s ${deviceId} shell ip route`, (error, stdout) => {
      if (error) {
        console.error(`获取设备 ${deviceId} 的 IP 地址时发生错误: ${error.message}`);
        return reject(error);
      }

      const ipMatch = stdout.match(/src (\d+\.\d+\.\d+\.\d+)/);
      if (!ipMatch) {
        return reject(new Error('无法找到 IP 地址'));
      }
      const deviceIp = ipMatch[1];
      const tcpPort = getRandomPort(new Set());

      exec(`adb -s ${deviceId} tcpip ${tcpPort}`, (error) => {
        if (error) {
          return reject(error);
        }

        exec(`adb connect ${deviceIp}:${tcpPort}`, async (error) => {
          if (error) {
            return reject(error);
          }

          console.log(`成功连接到设备 ${deviceIp}:${tcpPort}`);
          // 添加延时
          await new Promise(resolve => setTimeout(resolve, 2000));
          resolve({ deviceIp, tcpPort });
        });
      });
    });
  });
}


async function main() {
  try {
    await disconnectOfflineDevices();
    console.log('正在开始监控设备连接状态...');
    const tracker = await client.trackDevices();

    tracker.on('add', async (device) => {
      console.log(`检测到新设备: ${device.id}`);

      if (connectedDevices[device.id]) {
        console.log(`设备 ${device.id} 已经连接，跳过`);
        return;
      }

      try {
        await tcpIpConnect(device.id);
        connectedDevices[device.id] = true; // 标记设备已连接
      } catch (err) {
        console.error(`处理设备 ${device.id} 时发生错误: ${err.message}`);
      }
    });

    tracker.on('error', (err) => {
      console.error('追踪设备时发生错误:', err.message);
    });

    tracker.on('end', () => {
      console.log('设备追踪结束');
    });
  } catch (err) {
    console.error('发生错误:', err.message);
  }
}

main();
