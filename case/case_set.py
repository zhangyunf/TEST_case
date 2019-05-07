#-*- endcoding:utf-8 -*-


class CaseSet(object):

    def __init__(self, setlist):
        # 用例集名称
        self.set_name = setlist[0].value
        # 用例集案例总数
        self.count = setlist[1].value
        # 是否执行
        self.is_run = setlist[2].value
        # 通过数量
        self.pass_count = 0
        # 失败的数量
        self.faile_count = 0
        # 未执行的数量
        self.no_run = 0
        # 需要执行的案例
        self.run_case = []

    def description(self):
        # 打印案例数据
        print("%s--%s--%s--%d--%d--%s" % (self.set_name, self.count, self.is_run, self.pass_count, self.faile_count, self.run_case))






