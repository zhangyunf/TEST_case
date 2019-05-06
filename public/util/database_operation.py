#-*- endcoding:utf-8 -*-
import pymysql
from public.read_config.config import ReadConfig
from public.read_config.request_config_read import ReadRequest
from public.util.log import *

class MysqlOperation(object):

    def __init__(self):
        self.conn = None
        self.userSqlsor = None

    def connent_database(self, host):
        read_config = ReadConfig()
        self.conn = pymysql.connect(
            host=host,
            user=read_config.get_database_user,
            password=read_config.get_database_password,
        )
        self.userSqlsor = self.conn.cursor()

    def update_database(self, sql):
        self.userSqlsor.execute(sql)
        self.conn.commit()

    def get_value(self, sql, index):
        # 从数据库获取数据并返回
        self.userSqlsor.execute(sql)
        result = self.userSqlsor.fetchone()
        # 关闭光标对象
        self.userSqlsor.close()
        # 关闭数据库连接
        self.conn.close()
        log("查询数据库成功")
        return result[int(index)]

    def database_operation(self, case, data_pool):
        read_requests = ReadRequest()
        host = ""
        database = case.database.split(",")
        if "url" in database[0]:
            host = read_requests.get_url
        else:
            host = database[0]
        for index, sq in enumerate(database):
            if index >= 1 and sq != "":
                self.connent_database(host)
                if "==" not in sq:
                    # 修改数据库
                    try:
                        self.update_database(eval(sq))
                        log("修改数据库成功")
                    except Exception as error:
                        log("%s在修改数据库%s发生错误%s" % (case.caseNum, sq, error))
                    finally:
                        # 关闭光标对象
                        self.userSqlsor.close()
                        # 关闭数据库连接
                        self.conn.close()
                else:
                    # 从数据库获取信息
                    data = sq.split("==")
                    try:
                        result = self.get_value(eval(data[2]), data[1])
                        data_pool.update({case.caseNum + "_" + data[0]: result})
                    except Exception as error:
                        log("%s在获取数据库%s发生错误%s" % (case.caseNum, data[1], error))

if __name__ == '__main__':
    s = MysqlOperation()
    s.database_operation("192.168.55.105", "UPDATE `funds`.`funds_orders` SET `updated_at` = '2019-04-24 00:10:00.000000' WHERE (`id` =330371406241996800);")