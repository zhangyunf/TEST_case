#-*- endcoding:utf-8 -*-
from xml.sax import saxutils
from public.read_config.config import ReadConfig

class Template(object):
    STATUS = {
        0: 'pass',
        1: 'fail',
    }

    DEFAULT_TITLE = '自动化测试报告'
    DEFAULT_DESCRIPTION = ''

    # 邮件正文HTML模板
    SUBJECTHTML = r"""详细测试报告见附件
"""
    #HTML报告tmpl
    HTML_TMPL = r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>%(title)s</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
    <script src="http://libs.baidu.com/jquery/2.0.0/jquery.min.js"></script>
    <script src="http://libs.baidu.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
    <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
    %(stylesheet)s
</head>
<body>
<script language="javascript" type="text/javascript"><!--
output_list = Array();
/* level - 0:Summary; 1:Failed; 2:All */
function showCase(level) {
    trs = document.getElementsByTagName("tr");
    for (var i = 0; i < trs.length; i++) {
        tr = trs[i];
        id = tr.id;
        if (id.substr(0,2) == 'ft') {
            if (level == 2 || level == 0 ) {
                tr.className = 'hiddenRow';
            }
            else {
                tr.className = '';
            }
        }
        if (id.substr(0,2) == 'pt') {
            if (level < 2) {
                tr.className = 'hiddenRow';
            }
            else {
                tr.className = '';
            }
        }
    }
    //加入【详细】切换文字变化 --Findyou
    detail_class=document.getElementsByClassName('detail');
	//console.log(detail_class.length)
	if (level == 3) {
		for (var i = 0; i < detail_class.length; i++){
			detail_class[i].innerHTML="收起"
		}
	}
	else{
			for (var i = 0; i < detail_class.length; i++){
			detail_class[i].innerHTML="详细"
		}
	}
}
function showClassDetail(cid, count) {
    var id_list = Array(count);
    var toHide = 1;
    for (var i = 0; i < count; i++) {
        //ID修改 点 为 下划线 -Findyou
        tid0 = 't' + cid.substr(1) + '_' + (i+1);
        tid = 'f' + tid0;
        tr = document.getElementById(tid);
        if (!tr) {
            tid = 'p' + tid0;
            tr = document.getElementById(tid);
        }
        id_list[i] = tid;
        if (tr.className) {
            toHide = 0;
        }
    }
    for (var i = 0; i < count; i++) {
        tid = id_list[i];
        //修改点击无法收起的BUG，加入【详细】切换文字变化 --Findyou
        if (toHide) {
            document.getElementById(tid).className = 'hiddenRow';
            document.getElementById(cid).innerText = "详细"
        }
        else {
            document.getElementById(tid).className = '';
            document.getElementById(cid).innerText = "收起"
        }
    }
}
function html_escape(s) {
    s = s.replace(/&/g,'&amp;');
    s = s.replace(/</g,'&lt;');
    s = s.replace(/>/g,'&gt;');
    return s;
}
</script>
%(heading)s
%(report)s
%(ending)s
</body>
</html>
"""
    STYLESHEET_TMPL = """
<style type="text/css" media="screen">
body        { font-family: Microsoft YaHei,Tahoma,arial,helvetica,sans-serif;padding: 20px; font-size: 80%; }
table       { font-size: 100%; }
/* -- heading ---------------------------------------------------------------------- */
.heading {
    margin-top: 0ex;
    margin-bottom: 1ex;
}
.heading .description {
    margin-top: 4ex;
    margin-bottom: 6ex;
}
/* -- report ------------------------------------------------------------------------ */
#total_row  { font-weight: bold; }
.passCase   { color: #5cb85c; }
.failCase   { color: #d9534f; font-weight: bold; }
.norunCase  { color: #f0ad4e; font-weight: bold; }
.hiddenRow  { display: none; }
.testcase   { margin-left: 2em; }
</style>
"""

    # Heading
    #

    HEADING_TMPL = """<div class='heading'>
<h1>%(title)s</h1>
%(parameters)s
<p class='description'>%(description)s</p>
</div>
"""
    # variables: (title, parameters, description)

    HEADING_ATTRIBUTE_TMPL = """<p class='attribute'><strong>%(name)s:</strong> %(value)s</p>
"""
    # variables: (name, value)



    # ------------------------------------------------------------------------
    # ReportREPORT_TMPL
    #

    REPORT_TMPL = """
<p id='show_detail_line'>
<a class="btn btn-primary" href='javascript:showCase(0)'>概要{ %(summary)s }</a>
<a class="btn btn-danger" href='javascript:showCase(1)'>失败{ %(faile)s }</a>
<a class="btn btn-success" href='javascript:showCase(2)'>通过{ %(success_count)s }</a>
<a class="btn btn-success" href='javascript:showCase(2)'>未执行{ %(norun_count)s }</a>
<a class="btn btn-info" href='javascript:showCase(3)'>所有{ %(all)s }</a>
</p>
<table id='result_table' class="table table-condensed table-bordered table-hover">
<colgroup>
<col align='left' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
</colgroup>
<tr id='header_row' class="text-center success" style="font-weight: bold;font-size: 14px;">
    <td>用例集/测试用例</td>
    <td>总计</td>
    <td>通过</td>
    <td>失败</td>
    <td>未执行</td>
    <td>详细</td>
</tr>
%(test_list)s
<tr id='total_row' class="text-center active">
    <td>总计</td>
    <td>%(all)s</td>
    <td>%(success_count)s</td>
    <td>%(faile)s</td>
    <td>%(norun_count)s</td>
    <td>通过率:%(summary)s</td>
</tr>
</table>
""" # variables: (test_list, count, Pass, fail, error)

    REPORT_CLASS_TMPL = r"""
<tr class='%(style)s'>
    <td class="text-center">%(desc)s</td>
    <td class="text-center">%(count)s</td>
    <td class="text-center">%(Pass)s</td>
    <td class="text-center">%(fail)s</td>
    <td class="text-center">%(norun_count)s</td>
    <td class="text-center"><a href="javascript:showClassDetail('%(cid)s',%(count)s)" class="detail" id='%(cid)s'>详细</a></td>
</tr>
""" # variables: (style, desc, count, Pass, fail, error, cid)


    REPORT_TEST_WITH_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='5' align='center'>
    <!--css div popup start-->
    <button id='btn_%(tid)s' type="button"  class="btn btn-danger btn-xs collapsed" data-toggle="collapse" data-target='#div_%(tid)s'>失败</button>
    <div id='div_%(tid)s' class="collapse">
        <pre>
        %(script)s
        </pre>
    </div>
    <!--css div popup end-->
    </td>
</tr>
""" # variables: (tid, Class, style, desc, status)


    REPORT_TEST_NO_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='5' align='center'><span class="label label-success success">%(status)s</td>
</tr>
""" # variables: (tid, Class, style, desc, status)


    REPORT_TEST_OUTPUT_TMPL = r"""
%(id)s: %(output)s
""" # variables: (id, output)



    # ------------------------------------------------------------------------
    # ENDING
    #

    ENDING_TMPL = """<div id='ending'>&nbsp;</div>
    <div style=" position:fixed;right:50px; bottom:30px; width:20px; height:20px;cursor:pointer">
    <a href="#"><span class="glyphicon glyphicon-eject" style = "font-size:30px;" aria-hidden="true">
    </span></a></div>"""

# -------------------- The end of the Template class -------------------

class HTMLTestRunner(Template):

    def __init__(self, title=None, description=None):
        self.report_path = ReadConfig().get_html_report_path
        if title is None:
            self.title = self.DEFAULT_TITLE
        else:
            self.title = title
        if description is None:
            self.description = self.DEFAULT_DESCRIPTION
        else:
            self.description = description

    def generateReport(self, result):

        # 生成报告
        report_attrs = self.getReportAttributes(result)
        stylesheet = self._generate_stylesheet()
        heading = self._generate_heading(report_attrs)
        report = self._generate_report(result)
        ending = self._generate_ending()
        output = self.HTML_TMPL % dict(
            title=saxutils.escape(self.title),
            stylesheet=stylesheet,
            heading=heading,
            report=report,
            ending=ending,
        )
        with open(self.report_path, "w", encoding="utf-8") as file:
            file.write(output)


    def getReportAttributes(self, result):
        """
        整理测试结果
        """
        status = []
        status.append('共计 %d' % (result["count"]))
        status.append('成功 %d' % result["pass_count"])
        status.append('失败 %d' % result["faile_count"])
        status.append('未执行%d' % result["non-execution"])
        pas = round(result["pass_count"] / (result["pass_count"] + result["faile_count"]) * 100, 2)
        status.append('通过率= %0.2f%%' % pas)

        if status:
            status = '  '.join(status)
        else:
            status = 'none'
        return [
            ("执行人员", "张云飞    张聪山"),
            ('开始时间', result["start_time"]),
            ("结束时间", result["end_time"]),
            ('测试结果', status),
        ]

    def _generate_stylesheet(self):
        '''格式'''
        return self.STYLESHEET_TMPL

    def _generate_heading(self, report_attrs):
        a_lines = []
        for name, value in report_attrs:
            '''
            name:title
            value:统计数据
            '''
            line = self.HEADING_ATTRIBUTE_TMPL % dict(
                    name = saxutils.escape(name),
                    value = saxutils.escape(value),
                )
            a_lines.append(line)
        heading = self.HEADING_TMPL % dict(
            title = saxutils.escape(self.title),
            parameters = ''.join(a_lines),
            description = saxutils.escape(self.description),
        )
        return heading

    def _generate_report(self, result):
        rows = []
        # 用例集
        '''
        style:根据用例集是否全部通过设置格式
        desc:用例集名称
        count:总案例数
        pass:通过案例数
        fail:失败案例数
        cid:第几个用例集
        '''
        for index, case_set in enumerate(result["case"]):
            row = self.REPORT_CLASS_TMPL % dict(
                style='failClass' if case_set.faile_count > 0 else 'passClass',
                desc=case_set.set_name,
                count=case_set.count,
                Pass=case_set.pass_count,
                fail=case_set.faile_count,
                norun_count=case_set.no_run,
                cid='c%s' % (index + 1),
            )
            rows.append(row)
            # 用例集下的用例
            for tid, case in enumerate(case_set.run_case):
                self._generate_report_test(rows, index, tid, case)



        pas = '%0.2f%%' % round(result["pass_count"] / (result["pass_count"] + result["faile_count"]) * 100,2)
        # 表格概要+表格最后一行
        '''
        概要
        summary:概要
        faile:失败案例个数
        cuccess_count:成功案例个数
        all:总案例个数
        '''
        report = self.REPORT_TMPL % dict(
            summary=pas,
            faile=str(result["faile_count"]),
            success_count=str(result["pass_count"]),
            all=result["count"],
            test_list=''.join(rows),
            norun_count=str(result["non-execution"])
        )
        return report

    def _generate_report_test(self, rows, index, tid, case):

        #判断是否通过
        has_output = True if case.actual_result == None or "Success" in case.actual_result else False
        tid = ("p" if has_output else "f") + 't%s_%s' % (index + 1, tid + 1)
        desc = case.caseNum
        #选择通过还是失败的html表格格式
        tmpl = self.REPORT_TEST_NO_OUTPUT_TMPL if has_output else self.REPORT_TEST_WITH_OUTPUT_TMPL
        '''
        tid：案例编号
        output:失败日志
        '''
        case_desc = "未执行" if None == case.actual_result else case.actual_result
        script = self.REPORT_TEST_OUTPUT_TMPL % dict(
            id=tid,
            output=saxutils.escape(case_desc),
        )
        case_result = ""
        style = ""
        if case.actual_result != None:
            if "Success" in case.actual_result:
                case_result = "通过"
                style = "passCase"
            elif "False" in case.actual_result:
                case_result = "失败"
                style = "failCase"
        else:
            case_result = "未执行"
            style = "norunCase"
        row = tmpl % dict(
            tid=tid,
            Class='hiddenRow' if has_output else 'none',
            style=style,
            desc=desc,
            script=script,
            status=case_result,
        )
        rows.append(row)
        if not has_output:
            return

    def _generate_ending(self):
        '''结束'''
        return self.ENDING_TMPL

if __name__ == "__main__":
    result = {
              "desc":"交易所",
              "success_count": 100,
              "failure_count": 200,
              "all_case":300,
              "start_time": 4341432143244,
              "stop_time":  4341432149999}
    a = HTMLTestRunner()
    a.generateReport(result)