from nicegui import ui
import argparse

####################################################################################

# #传参
# # 创建解析器
# parser = argparse.ArgumentParser(description="nicegui")
# # 添加参数
# parser.add_argument('filename', type=str, help='需要处理的文件名')
#
# # 解析参数
# args = parser.parse_args()

####################################################################################

# 定义主页
def home_page():
    with ui.column().classes("items-center justify-center w-full h-full"):
        # 主页标题
        ui.label("欢迎来到多功能工具主页").classes(
            "text-h3 text-bold text-primary"
        )
        ui.label("请选择一个功能：").classes("text-h5 text-grey-8 q-mb-lg")

        # 按钮样式
        button_style = "w-80 h-20 bg-primary text-white rounded-xl shadow-lg transition-transform transform hover:scale-105"

        # 功能按钮
        ui.button("图像像素选择工具", on_click=lambda: ui.navigate.to("/pixel-picker")).classes(button_style)
        ui.button("其他功能页面", on_click=lambda: ui.navigate.to("/other-feature")).classes(button_style)
        ui.button("返回主页", on_click=lambda: ui.navigate.to("/")).classes(button_style)






# 配置路由
ui.page("/", title="主页")(home_page)

# 启动应用
ui.run(port=9000, reload=True)