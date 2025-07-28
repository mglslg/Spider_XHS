import streamlit as st
import glob

from sync_app.sync_service import *
from sync_app.sync_util import *

page = st.sidebar.radio("菜单", ["给我爬", "Excel 文件列表", "配置"])

if page == "配置":
    st.title("配置页面")

    # 1. 配置 cookie 的入口
    cookie = st.text_input("Cookie", value=get_cookie())

    # 2. 配置 user profile 根目录
    user_profile = st.text_input("User Profile", value=get_user_profile())

    # 3. 配置 Notion Token
    notion_token = st.text_input("Notion Token", value=get_notion_token(), type="password")

    # 4. 配置 Notion DatabaseId
    notion_database_id = st.text_input("Notion Database ID", value=get_notion_database_id())

    # 5. 保存按钮
    if st.button("保存"):
        set_cookie(cookie)
        set_user_profile(user_profile)
        set_notion_token(notion_token)
        set_notion_database_id(notion_database_id)
        st.success("配置已保存！")

elif page == "Excel 文件列表":
    st.header("Excel 文件列表")
    st.divider()

    excel_dir = "datas/excel_datas"
    excel_files = glob.glob(os.path.join(excel_dir, "*.xlsx"))

    # 获取文件创建时间并排序（倒序）
    files_with_time = [(f, os.path.getctime(f)) for f in excel_files]
    files_with_time.sort(key=lambda x: x[1], reverse=True)

    for file_path, _ in files_with_time:
        file_name = os.path.basename(file_path)
        col1, col2, col3, col4 = st.columns([5, 1, 1, 2])
        with col1:
            st.write(file_name)
        with col2:
            with open(file_path, "rb") as f:
                st.download_button("下载", data=f, file_name=file_name, key=f"download_{file_name}")
        with col3:
            if st.button("删除", key=f"delete_{file_name}"):
                os.remove(file_path)
                st.rerun()  # 刷新页面以更新列表
        with col4:
            if st.button("同步到notion", key=f"sync_{file_name}"):
                with st.spinner('notion同步中……'):
                    try:
                        file_path = os.path.join('datas/excel_datas', file_name)
                        import_xls_to_notion(file_path)
                        st.success(f"{file_name} 已同步到 Notion！")
                    except Exception as e:
                        st.error(f"同步失败: {str(e)}")
        st.divider()

elif page == "给我爬":
    st.header("给我爬")

    breakpoint_id_note = st.text_input("笔记断点ID (为空时爬取全量)", value="")
    if st.button("爬取笔记"):
        try:
            with st.spinner("数据爬取中..."):  # 显示加载转圈
                success, msg = spider_note(breakpoint_id_note)  # 传入断点ID
            if success:
                st.success(f"爬取成功，请到Excel文件列表中查看")
            else:
                st.error(f"爬取失败：{msg}")
        except Exception as e:
            st.error(f"错误：{e}")

    st.divider()

    breakpoint_id_collect = st.text_input("收藏断点ID (为空时爬取全量)", value="")
    if st.button("爬取收藏"):
        try:
            with st.spinner("数据爬取中..."):  # 显示加载转圈
                success, msg = spider_collection(breakpoint_id_collect)  # 传入断点ID
            if success:
                st.success(f"爬取成功，请到Excel文件列表中查看")
            else:
                st.error(f"爬取失败：{msg}")
        except Exception as e:
            st.error(f"错误：{e}")

    st.divider()

    breakpoint_id_like = st.text_input("点赞断点ID (为空时爬取全量)", value="")
    if st.button("爬取点赞"):
        try:
            with st.spinner("数据爬取中..."):  # 显示加载转圈
                success, msg = spider_like(breakpoint_id_like)  # 传入断点ID
            if success:
                st.success(f"爬取成功，请到Excel文件列表中查看")
            else:
                st.error(f"爬取失败：{msg}")
        except Exception as e:
            st.error(f"错误：{e}")

    st.divider()
