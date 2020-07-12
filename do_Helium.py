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

        # 变量
        data_to_write_type = type(data_to_write)

        # 显示
        print("目标数据类型：" + str(data_to_write_type))

        # Write / 处理
        column_len = len(data_to_write)

        # 开始写
        if data_to_write_type is list:
            for current_col in range(0, column_len):
                self.obj_excel_workbook_sheet.write(which_line, current_col, data_to_write[current_col])

        else:
            for item in data_to_write:
                # 数据
                item_value = data_to_write.get(item)

                # 显示
                # print("----------")
                # print("Key = " + item)
                # print("Value = " + item_value)

                if item == "title":
                    self.obj_excel_workbook_sheet.write(which_line, 0, item_value)
                if item == "type":
                    self.obj_excel_workbook_sheet.write(which_line, 1, item_value)
                if item == "stars":
                    self.obj_excel_workbook_sheet.write(which_line, 2, item_value)
                if item == "price":
                    self.obj_excel_workbook_sheet.write(which_line, 3, item_value)
                if item == "address":
                    self.obj_excel_workbook_sheet.write(which_line, 4, item_value)
                if item == "phone":
                    self.obj_excel_workbook_sheet.write(which_line, 5, item_value)
                if item == "business_time":
                    self.obj_excel_workbook_sheet.write(which_line, 6, item_value)

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
        self.what_you_want = search_string

        # 对象 / 类
        self.obj_excel = class_xlwr("百度地图_结果.xls")
        # 定义【Sheet】
        self.obj_excel.do_sheet("搜索【" + city_target + "】的【" + self.what_you_want + "】")
        # 定义【列】
        self.obj_excel.do_write(['名称', '类型', '星级评分', '参考价', '地址','电话','营业时间'], 0)

        # 定位城市
        self.identify_city(str_city_source=city_source, str_city_target=city_target)

        # 搜索
        self.do_search(str_search=self.what_you_want)

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
        try:
            click(str_city_source)
        except Exception as err:
            click("全国")

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
        item_cursor = 1
        for current_cursor in range(0,obj_item_set_len):

            current_index = current_cursor + 1

            item = None

            obj_item_set_root = self.get_Element_by_JS(
                "return document.getElementsByClassName('poilist')"
            )
            for root_item in obj_item_set_root:
                item = root_item.find_element_by_xpath(
                    "//ul[@class='poilist']/li[" + str(current_index) + "]")

            # 变量
            item_index = item.get_attribute("data-index")

            # 显示
            if_while = True
            while if_while:
                try:
                    # 处理
                    print("")
                    print("------ " + item.tag_name + " || " + str(item_index))
                    # 标识
                    if_while = False
                except Exception as err:

                    # 处理
                    obj_item_set_root = self.get_Element_by_JS(
                        "return document.getElementsByClassName('poilist')"
                    )
                    for root_item in obj_item_set_root:
                        item = root_item.find_element_by_xpath(
                            "//ul[@class='poilist']/li[" + str(item_index) + "]")

                        obj_item_set_len = len(obj_item_set)

                    # 标识
                    if_while = True

            # 点击
            click(item)

            time.sleep(8)

            # 变量
            total_message = {}

            # 总共
            obj_target_item = self.get_Element_by_JS(
                "return document.getElementsByClassName('poidetail-container')"
            )[0]
            obj_target_item_text = obj_target_item.text

            # 标题
            try:
                obj_title = obj_target_item.find_element_by_xpath(
                    "//div[@class='generalHead-left-header-title']")

                print("标题：" + obj_title.text)

                total_message.update(title = obj_title.text)
            except Exception as err:
                pass

            # 类型
            try:
                obj_type = obj_target_item.find_element_by_xpath(
                    "//div[@class='generalHead-left-header-aoitag animation-common']")
                print("类型：" + obj_type.text)
                total_message.update(type = obj_type.text)
            except Exception as err:
                pass

            # 星级评分
            try:
                obj_star_1 = obj_target_item.find_element_by_xpath(
                    "//span[@class='left-header-visit']")
                obj_star_2 = obj_target_item.find_element_by_xpath(
                    "//span[@class='left-header-know-visit']")

                obj_star = obj_star_1.text + " " + obj_star_2.text
                print("星级评分：" + obj_star)
                total_message.update(stars = obj_star)
            except Exception as err:
                print("没有找到星级评分")

            # 参考价
            try:
                obj_price = obj_target_item.find_element_by_xpath(
                    "//span[@class='left-header-reference-price']")
                print("参考价：" + obj_price.text)
                total_message.update(price = obj_price.text)
            except Exception as err:
                print("没有找到参考价")

            # 地址
            try:
                obj_address = obj_target_item.find_element_by_xpath(
                    "//div[@class='generalInfo-address item']")
                print("地址：" + obj_address.text)
                total_message.update(address = obj_address.text)
            except Exception as err:
                pass

            # 电话
            try:
                obj_phone = obj_target_item.find_element_by_xpath(
                    "//div[@class='generalInfo-telnum item']")
                print("电话：" + obj_phone.text)
                total_message.update(phone = obj_phone.text)
            except Exception as err:
                pass

            # 营业时间
            try:
                obj_business_time = obj_target_item.find_element_by_xpath(
                    "//div[@class='content c-auxiliary']")
                print("营业时间：" + obj_business_time.text)
                total_message.update(business_time=obj_business_time.text)
            except Exception as err:
                pass

            # 显示
            print(total_message)

            # 处理 / 写Excel文件
            self.obj_excel.do_write(total_message, self.total_count)

            # 返回

            print("@@@@@@@@@@@@")

            object_return_root = self.get_Element_by_JS(
                "return document.getElementById('cards-level0')"
                # "return document.getElementsByClassName('status-return')"
            )

            object_return = object_return_root.find_element_by_xpath(
                "//ul/li[1]")

            print(object_return.get_attribute("data-fold"))

            print("---> 返回")
            click(object_return)

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

        try:
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

        except Exception as err:

            # 显示
            print("当前搜索没有下一页信息")

            # 赋值
            if_next = False

        # 返回阶段
        return if_next

# </editor-fold>

# ********************************************
# <editor-fold desc="主函数">
if __name__ == "__main__":
    # %%%%%%%%%%%%%%%%%%
    print("<爬虫程序> ---> 百度地图")

    # %%%%%%%%%%%%%%%%%%
    obj_baidu_ditu = class_baidu_ditu(
        source_city="武汉", target_city="武汉", search_string="影院"
    )

# </editor-fold>

# ********************************************
# 结束阶段
# ********************************************
# Finished
