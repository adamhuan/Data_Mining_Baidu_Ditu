# -*- coding:utf-8 -*

# ********************************************
# <editor-fold desc="模块：导入">

# ******** 时间
import time

# ******** Helium
# ---
from helium import *

# ******** Excel
# -- 写
import xlwt
# -- 读
import xlrd

# </editor-fold>

# ********************************************
# <editor-fold desc="类：定义">

# ))))))))))))))))))) class_xlwt / Excel / 写
class class_xlwr:

    def __init__(self, str_Excel_name_file):

        # 变量 / 类
        self.file_name = str_Excel_name_file

        # 对象 / 类
        self.obj_excel_workbook = xlwt.Workbook(encoding="ascii")

    def do_sheet(self, sheet_name):
        # Sheet
        self.obj_excel_workbook_sheet = self.obj_excel_workbook.add_sheet(sheetname=sheet_name)

    def do_write(self, data_to_write, which_line):

        # Write / 处理
        column_len = len(data_to_write)

        # 开始写
        for current_col in range(0, column_len):
            self.obj_excel_workbook_sheet.write(which_line, current_col, data_to_write[current_col])

        # 保存
        self.obj_excel_workbook.save(self.file_name)

# ))))))))))))))))))) class_baidu_ditu / 探索【百度地图】
class class_baidu_ditu:

    # ))))))))))))))) 初始化
    def __init__(self, source_city, target_city, search_string):
        # 变量 / 函数
        str_url_baidu_ditu = "ditu.baidu.com"

        # 变量 / 类
        self.helium_driver = start_chrome(url=str_url_baidu_ditu)
        self.total_count = 1

        # 具体【搜索】的条件

        # city_source = "武汉"
        # city_target = "深圳"
        # what_you_want = "烧烤"

        city_source = source_city
        city_target = target_city
        what_you_want = search_string

        # 对象 / 类
        self.obj_excel = class_xlwr("百度地图_结果.xls")
        # 定义【Sheet】
        self.obj_excel.do_sheet("搜索【" + city_target + "】的【" + what_you_want + "】")
        # 定义【列】
        self.obj_excel.do_write(['商家名称', '备注信息【1】', '备注信息【2】'], 0)

        # 定位城市
        self.identify_city(str_city_source=city_source, str_city_target=city_target)

        # 搜索
        self.do_search(str_search=what_you_want)

        # 等待
        time.sleep(5)

        # 数据处理
        self.get_data_action_flow()

    # )))))))))))))))
    # 获取元素
    def get_Element_by_JS(self, str_js):

        # ))))))))))) Pass
        pass

        # ))))))))))) 返回值
        return_object = None

        # ))))))))))) 处理
        return_object = self.helium_driver.execute_script(str_js)

        # ))))))))))) 返回阶段
        return return_object

    # )))))))))))))))

    # 切换地图所在地
    def identify_city(self, str_city_source, str_city_target):

        # 显示
        print("function::identify_city")

        # 点击：所在地
        click(str_city_source)

        # 点击：目标地
        click(str_city_target)

    # 输入你要查询的内容
    def do_search(self, str_search):

        # 显示
        print("function::do_search")

        # 获得目标对象

        # - 搜索：输入框
        obj_search_input = self.get_Element_by_JS(
            "return document.getElementById('sole-input')"
        )
        # - 搜索：按钮
        obj_search_button = self.get_Element_by_JS(
            "return document.getElementById('search-button')"
        )

        # 输入搜索内容
        obj_search_input.send_keys(str_search)

        # 按：回车
        press(ENTER)

    # 动作流
    def get_data_action_flow(self):

        # 显示
        print("function::get_data_action_flow")

        # 是否执行【下一页】
        do_next = True

        # 变量
        # 前一次的页码
        self.sign_prev_page_num = 0

        # 处理
        while_cursor = 1
        while do_next:

            # 显示
            print(" ==================== " + str(while_cursor) + " ==================== ")

            # 单页
            self.get_data_action_current_page()

            # 等待
            time.sleep(10)

            # 翻页
            do_next = self.get_data_action_navg_page()

            # 等待
            time.sleep(5)

            # 递增
            while_cursor = while_cursor + 1

    # 单页
    def get_data_action_current_page(self):

        # 显示
        print(" ---> function::get_data_action_current_page")

        # 变量 / 函数
        obj_curPage = self.get_Element_by_JS(
            "return document.getElementById('cards-level1')"
        )
        hover(obj_curPage)

        # 处理
        obj_item_set = None
        obj_item_set_len = 0
        while obj_item_set_len == 0:
            obj_item_set_root = self.get_Element_by_JS(
                "return document.getElementsByClassName('poilist')"
            )
            for root_item in obj_item_set_root:
                obj_item_set = root_item.find_elements_by_xpath(
                    "//ul[@class='poilist']/child::li")

                obj_item_set_len = len(obj_item_set)

        # 显示
        print("%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("数量：" + str(obj_item_set_len))

        # 处理
        item_cursor = 0
        for item in obj_item_set:

            # 显示
            if_while = True
            while if_while:
                try:
                    # 处理
                    print("------ " + item.tag_name + " || " + str(item.get_attribute("data-index")))
                    # 标识
                    if_while = False
                except Exception as err:
                    # 处理
                    item = self.get_Element_by_JS(
                        "return document.getElementsByClassName('search-item cater-item')[" + str(item_cursor) + "]"
                    )
                    # 标识
                    if_while = True

            # 变量
            obj_target_item = item.find_element_by_xpath(
                "//li[@data-index='" + str(item.get_attribute("data-index")) + "']/div/div[3]")
            obj_target_item_text = obj_target_item.text

            # 显示
            print(obj_target_item_text.split('\n'))

            # 处理
            self.obj_excel.do_write(obj_target_item_text.split('\n'),self.total_count)

            # 自增
            item_cursor = item_cursor + 1
            self.total_count = self.total_count + 1
            # 等待
            time.sleep(1)

    # 翻页
    def get_data_action_navg_page(self):

        # 显示
        print(" ---> function::get_data_action_navg_page")

        # 返回值
        # 为真 / 还有翻页
        # 为假 / 没有翻页
        if_next = True

        # 变量 / 函数
        obj_curPage = self.get_Element_by_JS(
            "return document.getElementById('cards-level1')"
        )
        hover(obj_curPage)

        obj_curPage = self.get_Element_by_JS(
            "return document.getElementsByClassName('curPage')"
        )

        print("=============================")
        for item in obj_curPage:

            # 显示
            print("当前页码：" + str(item.text))

            if item.text == self.sign_prev_page_num:
                if_next = False

            # 赋值
            self.sign_prev_page_num = item.text

        # 处理
        click("下一页")

        # 返回阶段
        return if_next

# </editor-fold>

# ********************************************
# <editor-fold desc="主函数">
if __name__ == "__main__":

    # %%%%%%%%%%%%%%%%%%
    print("<爬虫程序> ---> 百度地图")

    # %%%%%%%%%%%%%%%%%%
    obj_baidu_ditu = class_baidu_ditu(source_city="武汉", target_city="深圳", search_string="花店")

# </editor-fold>

# ********************************************
# 结束阶段
# ********************************************
# Finished