import psycopg2
import os
import configparser
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
        #print(config_path)
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
            #print("连接数据库成功了！！！！")
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

    #插入cpu_info数据
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

    #查询ids区分同设备不同时间段数据
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





# # 定义数据库配置信息
# db_config = {
#     'db': 'Perf',
#     'name': 'postgres',
#     'password': '7to12pg12',
#     'ip': '10.8.8.110',
#     'port': '5433'
# }

# 创建 DatabaseOperations 实例
# db_operations = DatabaseOperations()
#
# # 测试连接
# conn = db_operations.connect()
#
# # 测试 get_latest_ids 方法
# device_id = 'Q200PRiRk2901327'
# latest_ids = db_operations.get_latest_ids(device_id)
# if latest_ids:
#     print(f"Latest ids for device_id {device_id}: {latest_ids}")
# else:
#     print(f"No ids found for device_id {device_id}")


