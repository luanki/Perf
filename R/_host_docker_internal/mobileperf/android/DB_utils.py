import psycopg2
import os
import configparser
import pandas as pd
import datetime

class DatabaseOperations:
    # def __init__(self):
    #     self.db_config = {
    #         'db': os.getenv('DB_NAME'),
    #         'name': os.getenv('DB_USER'),
    #         'password': os.getenv('DB_PASSWORD'),
    #         'ip': os.getenv('DB_HOST'),
    #         'port': os.getenv('DB_PORT')
    #     }
    def __init__(self):
        self.db_config = self.read_config()

    def read_config(self):
        # 获取项目根目录路径
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(project_root, 'config.ini')
        # print(config_path)
        config = configparser.ConfigParser()
        config.read(config_path)
        return {
            'db': config['database']['db_name'],
            'user': config['database']['db_user'],
            'password': config['database']['db_password'],
            'host': config['database']['db_host'],
            'port': config['database']['db_port']
        }

    def connect(self):
        try:
            conn = psycopg2.connect(
                dbname=self.db_config['db'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                host=self.db_config['host'],
                port=self.db_config['port']
            )
            # print("连接数据库成功了！！！！")
            return conn
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return None

    def devices_info_insert(self, device_id, device_name):
        conn = self.connect()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("""
                        INSERT INTO devices (device_id, device_name, created_at)
                        VALUES (%s, %s, CURRENT_TIMESTAMP)
                        """, (device_id, device_name))
            conn.commit()
            print("设备数据插入成功！")
        except Exception as e:
            conn.rollback()
            print(f"Failed to insert data: {e}")
        finally:
            cur.close()
            conn.close()

    # 插入cpu_info数据
    def CPU_info_insert(self, cpu_data):
        conn = self.connect()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("""
                        INSERT INTO cpu_info (device_id, datetime, device_cpu_rate, user_rate, system_rate, idle_rate, package_name, pid, pid_cpu_rate, recorded_at, device_ids)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s)
                        """, cpu_data)
            conn.commit()
            print("cpu数据插入成功！")
        except Exception as e:
            conn.rollback()
            print(f"Failed to insert data: {e}")
        finally:
            cur.close()
            conn.close()

    # 查询ids区分同设备不同时间段数据
    def get_latest_ids(self, device_id):
        conn = self.connect()
        if not conn:
            return None
        cur = conn.cursor()
        try:
            cur.execute("""
                        SELECT ids FROM devices WHERE device_id = %s ORDER BY created_at DESC LIMIT 1;
                        """, (device_id,))
            result = cur.fetchone()
            if result:
                return result[0]
            return None
        except Exception as e:
            print(f"Failed to fetch ids: {e}")
            return None
        finally:
            cur.close()
            conn.close()

    def insert_meminfo(self, meminfo_data):
        conn = self.connect()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("""
                        INSERT INTO meminfo (device_id, datetime, total_ram, free_ram, package_name, pid, pid_pss, recorded_at, device_ids)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s)
                        """, meminfo_data)
            conn.commit()
            print("meminfo数据插入成功！")
        except Exception as e:
            conn.rollback()
            print(f"Failed to insert data: {e}")
        finally:
            cur.close()
            conn.close()

    def insert_fpsinfo(self, fps_data):
        conn = self.connect()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("""
                        INSERT INTO fps_info (device_id, datetime, activity_window, fps, jank, recorded_at, device_ids)
                        VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s)
                        """, fps_data)
            conn.commit()
            print("fps数据插入成功！")
        except Exception as e:
            conn.rollback()
            print(f"Failed to insert data: {e}")
        finally:
            cur.close()
            conn.close()

    def get_all_devices(self):
        conn = self.connect()
        if not conn:
            return None
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM devices;")
            devices = cur.fetchall()
            print("查看所有设备！")
            return devices
        except Exception as e:
            print(f"Failed to fetch devices: {e}")
            return None
        finally:
            cur.close()
            conn.close()

    def get_devices_perf_info(self, sn, ids):
        conn = self.connect()
        if not conn:
            return None
        cur = conn.cursor()
        try:
            cur.execute(
                """
                WITH fps_data AS (
                SELECT fps1.*
                FROM fps_info fps1
                WHERE fps1.device_ids = %s
            ),
            cpu_data AS (
                SELECT cpu1.*
                FROM cpu_info cpu1
                WHERE cpu1.device_ids = %s
            ),
            mem_data AS (
                SELECT mem1.*
                FROM meminfo mem1
                WHERE mem1.device_ids = %s
            ),
            combined_data AS (
                SELECT
                    d.id AS device_id,
                    d.device_name,
                    d.created_at,
                    fps.id AS fps_id,
                    fps.datetime AS fps_datetime,
                    fps.activity_window,
                    fps.fps,
                    fps.jank,
                    fps.recorded_at AS fps_recorded_at,
                    cpu.id AS cpu_id,
                    cpu.datetime AS cpu_datetime,
                    cpu.device_cpu_rate,
                    cpu.user_rate,
                    cpu.system_rate,
                    cpu.idle_rate,
                    cpu.package_name AS cpu_package_name,
                    cpu.pid AS cpu_pid,
                    cpu.pid_cpu_rate,
                    cpu.recorded_at AS cpu_recorded_at,
                    mem.id AS mem_id,
                    mem.datetime AS mem_datetime,
                    mem.total_ram,
                    mem.free_ram,
                    mem.package_name AS mem_package_name,
                    mem.pid AS mem_pid,
                    mem.pid_pss,
                    mem.recorded_at AS mem_recorded_at
                FROM devices d
                LEFT JOIN fps_data fps ON d.ids = fps.device_ids
                LEFT JOIN cpu_data cpu ON fps.device_ids = cpu.device_ids
                    AND fps.datetime = cpu.datetime -- 按照datetime进行匹配
                LEFT JOIN mem_data mem ON fps.device_ids = mem.device_ids
                    AND fps.datetime = mem.datetime -- 按照datetime进行匹配
                WHERE d.device_id = %s
                    AND d.ids = %s
                ORDER BY fps.datetime
            )
            SELECT
                *,
                (SELECT COUNT(*) FROM fps_data) AS total_fps,
                (SELECT COUNT(*) FROM cpu_data) AS total_cpu,
                (SELECT COUNT(*) FROM mem_data) AS total_mem
            FROM combined_data;
                """
                , (ids, ids, ids, sn, ids))
            devices = cur.fetchall()
            print("查看所有设备！")
            # 获取查询结果的列名列表
            columns = [column[0] for column in cur.description]

            # 将查询结果存储为键值对形式的字典，并存储到列表中
            result = []
            for row in devices:
                row_dict = {}
                for i in range(len(columns)):
                    row_dict[columns[i]] = row[i]
                result.append(row_dict)

            return result
        except Exception as e:
            print(f"Failed to fetch devices: {e}")
            return None
        finally:
            cur.close()
            conn.close()



    # def get_mem_info(self, sn, ids):
    #     conn = self.connect()
    #     if not conn:
    #         return None
    #     cur = conn.cursor()
    #     try:
    #         cur.execute("""
    #                         select * from meminfo where device_ids = %s and device_id = %s
    #                         """, (ids, sn))
    #         devices = cur.fetchall()
    #         print("查看指定设备meminfo！")
    #         return devices
    #     except Exception as e:
    #         print(f"Failed to fetch devices: {e}")
    #         return None
    #     finally:
    #         cur.close()
    #         conn.close()

    # def get_fps_info(self, sn, ids):
    #     conn = self.connect()
    #     if not conn:
    #         return None
    #     cur = conn.cursor()
    #     try:
    #         cur.execute("""
    #                         select * from fps_info where device_ids = %s and device_id = %s
    #                         """, (ids, sn))
    #         devices = cur.fetchall()
    #         print("查看指定设备fpsinfo！")
    #         return devices
    #     except Exception as e:
    #         print(f"Failed to fetch devices: {e}")
    #         return None
    #     finally:
    #         cur.close()
    #         conn.close()

    def get_cpu_info(self, sn, ids):
        conn = self.connect()
        if not conn:
            return None
        cur = conn.cursor()
        try:
            cur.execute("""
                    select * from cpu_info where device_ids = %s and device_id = %s
                    """, (ids, sn))
            devices = cur.fetchall()
            print("查看指定设备cpuinfo！")
            columns = [column[0] for column in cur.description]

            # 将查询结果存储为键值对形式的字典，并存储到列表中
            result = []
            for row in devices:
                row_dict = {}
                for i in range(len(columns)):
                    if isinstance(row[i], datetime.datetime):
                        row_dict[columns[i]] = row[i].strftime('%Y-%m-%d %H:%M:%S')  # 转换为字符串格式
                    else:
                        row_dict[columns[i]] = row[i]
                result.append(row_dict)

            return result if result else []  # 返回空列表 [] 如果 result 为空
        except Exception as e:
            print(f"Failed to fetch cpuinfo: {e}")
            return None
        finally:
            cur.close()
            conn.close()

    def get_mem_info(self, sn, ids):
        conn = self.connect()
        if not conn:
            return None
        cur = conn.cursor()
        try:
            cur.execute("""
                    select * from meminfo where device_ids = %s and device_id = %s
                    """, (ids, sn))
            devices = cur.fetchall()
            print("查看指定设备meminfo！")
            columns = [column[0] for column in cur.description]

            # 将查询结果存储为键值对形式的字典，并存储到列表中
            result = []
            for row in devices:
                row_dict = {}
                for i in range(len(columns)):
                    if isinstance(row[i], datetime.datetime):
                        row_dict[columns[i]] = row[i].strftime('%Y-%m-%d %H:%M:%S')  # 转换为字符串格式
                    else:
                        row_dict[columns[i]] = row[i]
                result.append(row_dict)

            return result if result else []  # 返回空列表 [] 如果 result 为空
        except Exception as e:
            print(f"Failed to fetch memory: {e}")
            return None
        finally:
            cur.close()
            conn.close()

    def get_fps_info(self, sn, ids):
        conn = self.connect()
        if not conn:
            return None
        cur = conn.cursor()
        try:
            cur.execute("""
                    select * from fps_info where device_ids = %s and device_id = %s
                    """, (ids, sn))
            devices = cur.fetchall()
            print("查看指定设备fpsinfo！")
            columns = [column[0] for column in cur.description]

            # 将查询结果存储为键值对形式的字典，并存储到列表中
            result = []
            for row in devices:
                row_dict = {}
                for i in range(len(columns)):
                    if isinstance(row[i], datetime.datetime):
                        row_dict[columns[i]] = row[i].strftime('%Y-%m-%d %H:%M:%S')  # 转换为字符串格式
                    else:
                        row_dict[columns[i]] = row[i]
                result.append(row_dict)

            return result if result else []  # 返回空列表 [] 如果 result 为空
        except Exception as e:
            print(f"Failed to fetch fps: {e}")
            return None
        finally:
            cur.close()
            conn.close()
# # 定义数据库配置信息
# db_config = {
#     'db': 'Perf',
#     'name': 'postgres',
#     'password': '7to12pg12',
#     'ip': '10.8.8.110',
#     'port': '5433'
# }


# db_operations = DatabaseOperations()
#
# # 测试连接
# conn = db_operations.connect()
#
# # 测试 get_latest_ids 方法
# device_id = 'S30PQkRa0500702'
# ids = '18'
# d = db_operations.get_cpu_info(device_id,ids)
# print(d)
