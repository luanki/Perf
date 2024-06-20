import psycopg2
import configparser
import os
class DatabaseOperations:
    def __init__(self):
        self.db_config = self.read_config()

    def read_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        return dict(config.items('database'))

    def connect(self):
        try:
            # print(
            #     f"Connecting to database {self.db_config['db']} at {self.db_config['ip']}:{self.db_config['port']} as {self.db_config['name']}...")
            conn = psycopg2.connect(
                dbname=self.db_config['db_name'],
                user=self.db_config['db_user'],
                password=self.db_config['db_password'],
                host=self.db_config['db_host'],
                port=self.db_config['db_port']
            )
            print("Connected to database successfully.连接数据库成功了！！！！")
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
            print("Data inserted successfully.")
        except Exception as e:
            conn.rollback()
            print(f"Failed to insert data: {e}")
        finally:
            cur.close()
            conn.close()

    def CPU_info_insert(self, cpu_data):
        conn = self.connect()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO cpu_info (datetime, device_cpu_rate, user_rate, system_rate, idle_rate, package, pid, pid_cpu)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, cpu_data)
            conn.commit()
            print("Data inserted successfully.")
        except Exception as e:
            conn.rollback()
            print(f"Failed to insert data: {e}")
        finally:
            cur.close()
            conn.close()

    def update(self, cpu_data, id):
        conn = self.connect()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE cpu_info
                SET datetime = %s, device_cpu_rate = %s, user_rate = %s, system_rate = %s, idle_rate = %s, package = %s, pid = %s, pid_cpu = %s
                WHERE id = %s
            """, cpu_data + (id,))
            conn.commit()
            print("Data updated successfully.")
        except Exception as e:
            conn.rollback()
            print(f"Failed to update data: {e}")
        finally:
            cur.close()
            conn.close()

    def delete(self, id):
        conn = self.connect()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM cpu_info WHERE id = %s", (id,))
            conn.commit()
            print("Data deleted successfully.")
        except Exception as e:
            conn.rollback()
            print(f"Failed to delete data: {e}")
        finally:
            cur.close()
            conn.close()

    def fetch(self, id):
        conn = self.connect()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM cpu_info WHERE id = %s", (id,))
            result = cur.fetchone()
            return result
        except Exception as e:
            print(f"Failed to fetch data: {e}")
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

# # 创建 DatabaseOperations 实例
# db_operations = DatabaseOperations(db_config)
#
# # 测试连接
# conn = db_operations.connect()
# if conn is not None:
#     print("连接数据库成功！")
#     conn.close()
# else:
#     print("连接数据库失败！")
# 创建 DatabaseOperations 实例

