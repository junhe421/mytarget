import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys
from datetime import datetime, timedelta
import logging
import random
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(),  # 输出到控制台
        logging.FileHandler('app.log', encoding='utf-8')  # 同时保存到文件
    ]
)
logger = logging.getLogger('GoalTracker')

def log_operation(func):
    """操作日志装饰器"""
    def wrapper(*args, **kwargs):
        try:
            logger.info(f'开始执行: {func.__name__}')
            result = func(*args, **kwargs)
            logger.info(f'执行成功: {func.__name__}')
            return result
        except Exception as e:
            logger.error(f'执行失败: {func.__name__}, 错误: {str(e)}', exc_info=True)
            raise
    return wrapper

class Theme:
    LIGHT = {
        'bg': '#ffffff',
        'fg': '#2c3e50',
        'primary': '#3498db',
        'primary_dark': '#2980b9',
        'primary_light': '#ebf5fb',
        'secondary_bg': '#f8f9fa',
        'completed_fg': '#95a5a6',
        'high_priority': '#e74c3c',
        'medium_priority': '#f39c12',
        'low_priority': '#2ecc71',
        'border': '#e0e0e0',
        'hover': '#f5f5f5'
    }
    
    DARK = {
        'bg': '#1a1a1a',
        'fg': '#ecf0f1',
        'primary': '#3498db',
        'primary_dark': '#2980b9',
        'primary_light': '#2c3e50',
        'secondary_bg': '#2c3e50',
        'completed_fg': '#7f8c8d',
        'high_priority': '#c0392b',
        'medium_priority': '#d35400',
        'low_priority': '#27ae60',
        'border': '#34495e',
        'hover': '#2c3e50'
    }

class Language:
    def __init__(self):
        self.current_lang = 'zh_CN'
        self.languages = self.load_languages()
    
    def load_languages(self):
        """加载语言文件"""
        try:
            lang_file = os.path.join('data', 'languages.json')
            if os.path.exists(lang_file):
                with open(lang_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            logger.error('Language file not found')
            return {}
        except Exception as e:
            logger.error(f'Failed to load language file: {str(e)}')
            return {}
    
    def get_text(self, key, *args):
        """获取指定语言的文本"""
        try:
            text = self.languages[self.current_lang]
            for k in key.split('.'):
                text = text[k]
            return text.format(*args) if args else text
        except:
            return key
    
    def toggle_language(self):
        """切换语言"""
        self.current_lang = 'en_US' if self.current_lang == 'zh_CN' else 'zh_CN'
        return self.current_lang

class GoalTracker:
    def __init__(self):
        # 初始化主窗口
        self.root = tk.Tk()
        self.lang = Language()
        self.root.title(self.lang.get_text('app_title'))
        logger.info('启动目标管理器')
        
        # 设置窗口图标（如果存在）
        icon_path = os.path.join(os.path.dirname(__file__), "mt.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except:
                pass
        
        # 初始化主题
        self.current_theme = Theme.LIGHT
        
        # 设置窗口样式
        self.root.overrideredirect(True)  # 无边框
        self.root.attributes('-topmost', True)  # 置顶
        self.root.configure(bg=self.current_theme['bg'])
        
        # 设置窗口初始位置和大小
        self.root.geometry('300x520+100+100')
        
        # 初始化拖动变量
        self.drag_data = {'x': 0, 'y': 0, 'dragging': False}
        
        # 数据文件路径
        self.data_file = 'goals.json'
        self.quotes_file = 'quotes.json'
        
        # 当前选中的分类
        self.current_category = 'weekly'
        
        # 小横幅模式相关变量
        self.is_minimized = False
        self.last_activity_time = time.time()
        self.activity_timeout = 10  # 10秒无活动后最小化
        self.current_quote_index = 0
        self.quotes = self.load_quotes()
        
        # 初始化目标数据
        self.goals = self.load_data()
        
        # 创建界面
        self.create_widgets()
        
        # 更新日期范围
        self.update_date_range()
        
        # 绑定拖动事件
        self.bind_drag_events()
        
        # 创建右键菜单
        self.create_context_menu()
        
        # 启动活动检测
        self.check_activity()
        
        # 启动滚动显示
        self.scroll_quote()

    def load_quotes(self):
        """加载励志语录"""
        try:
            if os.path.exists(self.quotes_file):
                with open(self.quotes_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('quotes', [])
            return []
        except Exception as e:
            logger.error(f"加载励志语录失败: {str(e)}")
            return []

    def save_quotes(self):
        """保存励志语录"""
        try:
            with open(self.quotes_file, 'w', encoding='utf-8') as f:
                json.dump({'quotes': self.quotes}, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"保存励志语录失败: {str(e)}")

    def check_activity(self):
        """检查用户活动"""
        current_time = time.time()
        if not self.is_minimized and current_time - self.last_activity_time > self.activity_timeout:
            self.minimize_window()
        self.root.after(1000, self.check_activity)  # 每秒检查一次

    def minimize_window(self):
        """最小化窗口为横幅模式"""
        if not self.is_minimized:
            # 保存当前位置
            x = self.root.winfo_x()
            y = self.root.winfo_y()
            self.original_geometry = f'300x520+{x}+{y}'
            # 保持相同的x,y位置，只改变大小
            self.root.geometry(f'300x30+{x}+{y}')
            self.hide_main_widgets()
            self.show_banner_widgets()
            self.is_minimized = True

    def restore_window(self):
        """恢复正常窗口"""
        if self.is_minimized:
            # 使用保存的位置恢复窗口
            self.root.geometry(self.original_geometry)
            self.show_main_widgets()
            self.hide_banner_widgets()
            self.is_minimized = False
            self.last_activity_time = time.time()

    def hide_main_widgets(self):
        """隐藏主界面组件"""
        for widget in self.main_widgets:
            widget.pack_forget()

    def show_main_widgets(self):
        """显示主界面组件"""
        self.create_widgets()
        # 重新绑定拖动事件
        self.bind_drag_events()
        # 重新加载和显示数据
        self.update_list()

    def show_banner_widgets(self):
        """显示横幅模式组件"""
        self.banner_frame = tk.Frame(self.root, bg=self.current_theme['primary'], height=30)
        self.banner_frame.pack(fill='x')
        self.banner_frame.grid_columnconfigure(1, weight=1)  # 让语录标签可以扩展
        
        # 计算待办事项数量
        todo_count = sum(1 for goals in self.goals.values() for goal in goals if not goal['completed'])
        
        # 待办数量标签
        todo_label = tk.Label(self.banner_frame,
                            text=f"待办{todo_count}",
                            bg=self.current_theme['primary'],
                            fg='white',
                            font=('微软雅黑', 10))
        todo_label.grid(row=0, column=0, padx=10, pady=5)
        
        # 励志语录标签
        self.quote_label = tk.Label(self.banner_frame, 
                                  text=self.quotes[self.current_quote_index] if self.quotes else "添加你的励志语录",
                                  bg=self.current_theme['primary'],
                                  fg='white',
                                  font=('微软雅黑', 10))
        self.quote_label.grid(row=0, column=1, pady=5, sticky='ew')
        
        # 绑定鼠标事件 - 改为双击恢复窗口
        for widget in [self.banner_frame, todo_label, self.quote_label]:
            widget.bind('<Double-Button-1>', lambda e: self.restore_window())
            widget.bind('<Button-3>', self.show_quote_menu)
            widget.bind('<Button-1>', self.start_drag)
            widget.bind('<B1-Motion>', self.on_drag)
            widget.bind('<ButtonRelease-1>', self.stop_drag)

    def hide_banner_widgets(self):
        """隐藏横幅模式组件"""
        if hasattr(self, 'banner_frame'):
            self.banner_frame.destroy()

    def scroll_quote(self):
        """滚动显示励志语录"""
        if self.is_minimized and self.quotes:
            self.current_quote_index = (self.current_quote_index + 1) % len(self.quotes)
            if hasattr(self, 'quote_label'):
                self.quote_label.config(text=self.quotes[self.current_quote_index])
        self.root.after(3000, self.scroll_quote)  # 每3秒切换一次

    def show_quote_menu(self, event):
        """显示励志语录右键菜单"""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="编辑语录", command=self.edit_quotes)
        menu.add_command(label="添加语录", command=self.add_quote)
        menu.post(event.x_root, event.y_root)

    def edit_quotes(self):
        """编辑励志语录"""
        edit_window = tk.Toplevel(self.root)
        edit_window.title("编辑励志语录")
        edit_window.geometry("400x300")
        
        text = tk.Text(edit_window, font=('微软雅黑', 10))
        text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 显示当前语录
        text.insert('1.0', '\n'.join(self.quotes))
        
        def save():
            content = text.get('1.0', 'end-1c')
            self.quotes = [q.strip() for q in content.split('\n') if q.strip()]
            self.save_quotes()
            edit_window.destroy()
        
        tk.Button(edit_window, text="保存", command=save).pack(pady=10)

    def add_quote(self):
        """添加新的励志语录"""
        add_window = tk.Toplevel(self.root)
        add_window.title("添加励志语录")
        add_window.geometry("400x100")
        
        entry = tk.Entry(add_window, font=('微软雅黑', 10))
        entry.pack(fill='x', padx=10, pady=10)
        
        def save():
            quote = entry.get().strip()
            if quote:
                self.quotes.append(quote)
                self.save_quotes()
            add_window.destroy()
        
        tk.Button(add_window, text="添加", command=save).pack(pady=10)

    def create_widgets(self):
        """创建界面组件"""
        # 存主界面组件引用
        self.main_widgets = []
        
        # 绑定全局鼠标事件
        self.root.bind('<Button-1>', lambda e: self.reset_activity_timer())
        self.root.bind('<Button-3>', lambda e: self.reset_activity_timer())
        self.root.bind('<B1-Motion>', lambda e: self.reset_activity_timer())
        self.root.bind('<MouseWheel>', lambda e: self.reset_activity_timer())
        
        # 标题栏（用于拖动）
        self.title_bar = tk.Frame(self.root, bg=self.current_theme['primary'], height=40)
        self.title_bar.pack(fill='x', pady=(0, 5))
        self.main_widgets.append(self.title_bar)
        
        # Logo和标题
        title_label = tk.Label(self.title_bar, text='📋 我的T', bg=self.current_theme['primary'],
                              fg='white', font=('微软雅黑', 12, 'bold'))
        title_label.pack(side='left', padx=10, pady=5)
        
        # 主题切换按钮
        theme_btn = tk.Label(self.title_bar, text='🌓', bg=self.current_theme['primary'],
                            fg='white', font=('Arial', 12), cursor='hand2')
        theme_btn.pack(side='right', padx=5, pady=5)
        theme_btn.bind('<Button-1>', self.toggle_theme)
        
        # 语言切换按钮
        lang_btn = tk.Label(self.title_bar, text='🌐', bg=self.current_theme['primary'],
                          fg='white', font=('Arial', 12), cursor='hand2')
        lang_btn.pack(side='right', padx=5, pady=5)
        lang_btn.bind('<Button-1>', self.toggle_language)
        
        # 关闭按钮
        close_btn = tk.Label(self.title_bar, text='×', bg=self.current_theme['primary'],
                            fg='white', font=('Arial', 16, 'bold'), cursor='hand2')
        close_btn.pack(side='right', padx=5, pady=5)
        close_btn.bind('<Button-1>', self.quit_app)
        
        # 分类标签框架
        category_frame = tk.Frame(self.root, bg=self.current_theme['bg'])
        category_frame.pack(fill='x', padx=10, pady=5)
        self.main_widgets.append(category_frame)
        
        # 分类按钮容器（用于居中对齐）
        buttons_container = tk.Frame(category_frame, bg=self.current_theme['bg'])
        buttons_container.pack(expand=True)
        
        # 统一的按钮样式
        button_width = 8  # 统一宽度
        button_style = {
            'font': ('微软雅黑', 10),
            'width': button_width,
            'height': 1,
            'bd': 0,
            'cursor': 'hand2',
            'relief': 'flat'
        }
        
        # 分类按钮
        self.weekly_btn = tk.Button(buttons_container, text='本周',
                                   command=lambda: self.switch_category('weekly'),
                                   **button_style)
        self.weekly_btn.pack(side='left', padx=2)
        
        self.monthly_btn = tk.Button(buttons_container, text='本月',
                                    command=lambda: self.switch_category('monthly'),
                                    **button_style)
        self.monthly_btn.pack(side='left', padx=2)
        
        self.yearly_btn = tk.Button(buttons_container, text='本年',
                                   command=lambda: self.switch_category('yearly'),
                                   **button_style)
        self.yearly_btn.pack(side='left', padx=2)
        
        # 更新分类按钮状态
        self.update_category_buttons()
        
        # 日期范围标签
        self.date_label = tk.Label(self.root, text='', bg=self.current_theme['bg'],
                                  fg=self.current_theme['fg'], font=('微软雅黑', 9))
        self.date_label.pack(pady=5)
        self.main_widgets.append(self.date_label)
        
        # 优先级选择框架
        priority_frame = tk.Frame(self.root, bg=self.current_theme['bg'])
        priority_frame.pack(fill='x', padx=10, pady=5)
        self.main_widgets.append(priority_frame)
        
        # 优先级单选按钮容器（用于居中对齐）
        priority_container = tk.Frame(priority_frame, bg=self.current_theme['bg'])
        priority_container.pack(expand=True)
        
        # 优先级单选按钮
        self.priority_var = tk.StringVar(value='low')
        priorities = [
            ('高', 'high', '🔴'),
            ('中', 'medium', '🟡'),
            ('低', 'low', '🟢')
        ]
        
        for text, value, icon in priorities:
            rb = tk.Radiobutton(priority_container, text=f'{icon} {text}',
                               variable=self.priority_var, value=value,
                               bg=self.current_theme['bg'],
                               fg=self.current_theme['fg'],
                               selectcolor=self.current_theme['bg'],
                               font=('微软雅黑', 10))
            rb.pack(side='left', padx=10)
        
        # 输入框和添加按钮框架
        input_frame = tk.Frame(self.root, bg=self.current_theme['bg'])
        input_frame.pack(fill='x', padx=10, pady=5)
        self.main_widgets.append(input_frame)
        
        # 输入框
        self.entry = tk.Entry(input_frame, font=('微软雅黑', 10),
                             bg=self.current_theme['secondary_bg'],
                             fg=self.current_theme['fg'],
                             insertbackground=self.current_theme['fg'])
        self.entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self.entry.bind('<Key>', lambda e: self.reset_activity_timer())  # 添加键盘事件监听
        
        # 添加按钮
        add_btn = tk.Button(input_frame, text='添加', command=self.add_goal,
                           font=('微软雅黑', 10), bg=self.current_theme['primary'],
                           fg='white', bd=0, padx=15, cursor='hand2')
        add_btn.pack(side='right')
        
        # 作者信息标签
        author_frame = tk.Frame(self.root, bg=self.current_theme['bg'])
        author_frame.pack(fill='x', side='bottom', padx=10, pady=5)
        self.main_widgets.append(author_frame)
        
        author_label = tk.Label(author_frame, 
                              text='作者：A先生  QQ交流：3956582704',
                              bg=self.current_theme['bg'],
                              fg=self.current_theme['fg'],
                              font=('微软雅黑', 9))
        author_label.pack()
        
        # 目标列表框架
        self.list_frame = tk.Frame(self.root, bg=self.current_theme['bg'])
        self.list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        self.main_widgets.append(self.list_frame)
        
        # 更新列表显示
        self.update_list()

    def _on_mousewheel(self, event):
        """处理鼠标滚轮事件"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def create_context_menu(self):
        """创建右键菜单"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(
            label=self.lang.get_text('menu.edit'),
            command=self.edit_goal
        )
        self.context_menu.add_command(
            label=self.lang.get_text('menu.delete'),
            command=self.delete_goal
        )

    def show_context_menu_at(self, event, index):
        """在指定位置显示右键菜单"""
        self.selected_index = index
        self.context_menu.post(event.x_root, event.y_root)

    @log_operation
    def update_list(self):
        """更新目标列表显示"""
        # 清除现有列表
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        
        # 创建滚动画布
        canvas = tk.Canvas(self.list_frame, bg=self.current_theme['bg'],
                          highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.list_frame, orient='vertical',
                                command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.current_theme['bg'])
        
        # 配置滚动
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # 布局滚动组件
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # 创建窗口
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # 进度统计
        completed, percentage = self.get_progress_stats()
        stats_frame = tk.Frame(scrollable_frame, bg=self.current_theme['bg'])
        stats_frame.pack(fill='x', padx=5, pady=5)
        
        stats_label = tk.Label(stats_frame,
                             text=f'完成进度: {completed}/{len(self.goals[self.current_category])} ({percentage:.1f}%)',
                             bg=self.current_theme['bg'],
                             fg=self.current_theme['fg'],
                             font=('微软雅黑', 9))
        stats_label.pack(side='left')
        
        # 进度条
        progress_frame = tk.Frame(scrollable_frame, bg=self.current_theme['border'],
                                height=4)
        progress_frame.pack(fill='x', padx=5, pady=(0, 10))
        
        if percentage > 0:
            progress_bar = tk.Frame(progress_frame,
                                  bg=self.current_theme['primary'],
                                  height=4)
            progress_bar.place(relwidth=percentage/100, rely=0, relheight=1)
        
        # 对目标列表进行排序
        # 1. 未完成的排在前面
        # 2. 按优先级排序（高>中>低）
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        sorted_goals = sorted(
            self.goals[self.current_category],
            key=lambda x: (
                x['completed'],  # 首先按完成状态排序（False在前）
                priority_order[x['priority']],  # 然后按优先级排序
                x['text']  # 最后按文本内容排序
            )
        )
        
        # 显示目标列表
        for i, goal in enumerate(sorted_goals):
            # 目标项框架
            item_frame = tk.Frame(scrollable_frame, bg=self.current_theme['bg'])
            item_frame.pack(fill='x', padx=5, pady=2)
            
            # 配置鼠标悬停效果
            item_frame.bind('<Enter>',
                          lambda e, f=item_frame: f.configure(bg=self.current_theme['hover']))
            item_frame.bind('<Leave>',
                          lambda e, f=item_frame: f.configure(bg=self.current_theme['bg']))
            
            # 复选框
            check_var = tk.BooleanVar(value=goal['completed'])
            check = tk.Checkbutton(item_frame,
                                 variable=check_var,
                                 command=lambda g=goal, v=check_var: self.toggle_goal(g, v),
                                 bg=self.current_theme['bg'],
                                 activebackground=self.current_theme['bg'])
            check.pack(side='left', padx=(5, 0))
            
            # 优先级图标
            priority_colors = {
                'high': self.current_theme['high_priority'],
                'medium': self.current_theme['medium_priority'],
                'low': self.current_theme['low_priority']
            }
            priority_icons = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
            
            priority_label = tk.Label(item_frame,
                                    text=priority_icons[goal['priority']],
                                    bg=self.current_theme['bg'],
                                    fg=priority_colors[goal['priority']])
            priority_label.pack(side='left', padx=5)
            
            # 目标文本
            text_color = self.current_theme['completed_fg'] if goal['completed'] else self.current_theme['fg']
            text_label = tk.Label(item_frame,
                                text=goal['text'],
                                bg=self.current_theme['bg'],
                                fg=text_color,
                                font=('微软雅黑', 10),
                                anchor='w',
                                justify='left')
            text_label.pack(side='left', fill='x', expand=True, padx=5)
            
            # 绑定右键菜单
            for widget in [item_frame, text_label]:
                widget.bind('<Button-3>', lambda e, g=goal: self.show_goal_menu(e, g))
        
        # 绑定鼠标滚轮事件
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        # 更新日期范围显示
        self.date_label.configure(text=self.get_date_range())
        
        # 更新分类按钮状态
        self.update_category_buttons()

    def handle_checkbox_click(self, goal, var):
        """处理复选框点击事件"""
        goal['completed'] = var.get()
        status = "完成" if goal['completed'] else "未完成"
        self.save_data()
        self.update_list()

    def bind_drag_events(self):
        """绑定拖动事件"""
        self.title_bar.bind('<Button-1>', self.start_drag)
        self.title_bar.bind('<B1-Motion>', self.on_drag)
        self.title_bar.bind('<ButtonRelease-1>', self.stop_drag)

    def start_drag(self, event):
        """开始拖动"""
        self.drag_data['x'] = event.x
        self.drag_data['y'] = event.y
        self.drag_data['dragging'] = True
        
        # 记录初始点击的全局坐标与窗口位置的偏移
        self.drag_data['offset_x'] = event.x_root - self.root.winfo_x()
        self.drag_data['offset_y'] = event.y_root - self.root.winfo_y()

    def on_drag(self, event):
        """拖动处理"""
        if self.drag_data['dragging']:
            # 获事件的全局坐标
            x_root = event.x_root
            y_root = event.y_root
            
            # 计算新位置（使用偏移量）
            x = x_root - self.drag_data['offset_x']
            y = y_root - self.drag_data['offset_y']
            
            # 获取屏幕尺寸
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # 窗口尺寸
            window_width = 300
            window_height = 30 if self.is_minimized else 520
            
            # 确保窗口不会超出屏幕边界
            x = max(0, min(x, screen_width - window_width))
            y = max(0, min(y, screen_height - window_height))
            
            # 更新窗口位置
            self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    def stop_drag(self, event):
        """停止拖动"""
        self.drag_data['dragging'] = False

    @log_operation
    def load_data(self):
        """加载数据"""
        try:
            if os.path.exists('goals.json'):
                with open('goals.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data:
                        logger.info('成功加载数据')
                        return data
                    else:
                        logger.warning('数据文件为空，创建新的数据结构')
                        return self._create_default_data()
            else:
                return self._create_default_data()
        except Exception as e:
            logger.error(f'数据加载失败: {str(e)}')
            return self._create_default_data()

    def _create_default_data(self):
        """创建默认的数据结构"""
        default_data = {
            'weekly': [
                {
                    'text': '1.完成myshell商品上架',
                    'completed': False,
                    'priority': 'low'
                },
                {
                    'text': '3.完成透明数据库系统',
                    'completed': False,
                    'priority': 'low'
                },
                {
                    'text': '4.ai宣传视频模块制作',
                    'completed': False,
                    'priority': 'low'
                },
                {
                    'text': '2.明年计划',
                    'completed': False,
                    'priority': 'medium'
                }
            ],
            'monthly': [],
            'yearly': []
        }
        try:
            with open('goals.json', 'w', encoding='utf-8') as f:
                json.dump(default_data, f, ensure_ascii=False, indent=2)
            logger.info('创建新的数据文件')
        except Exception as e:
            logger.error(f'创建数据文件失败: {str(e)}')
        return default_data

    @log_operation
    def save_data(self):
        """保存数据"""
        try:
            with open('goals.json', 'w', encoding='utf-8') as f:
                json.dump(self.goals, f, ensure_ascii=False, indent=2)
            logger.info('数据保存成功')
        except Exception as e:
            logger.error(f'数据保存失败: {str(e)}')
            raise

    def switch_category(self, category):
        """切换目标分类"""
        self.reset_activity_timer()  # 重置计时器
        self.current_category = category
        category_names = {'weekly': '本周', 'monthly': '本月', 'yearly': '本年'}
        logger.info(f'切换到{category_names[category]}目标列表')
        self.update_date_range()
        self.update_list()

    def run(self):
        """运行应用"""
        try:
            logger.info('启动目标管理器')
            self.root.mainloop()
        except KeyboardInterrupt:
            logger.info('用户中断程序')
        except Exception as e:
            logger.error(f'程序异常退出: {str(e)}')
            raise
        finally:
            logger.info('关闭目标管理器')

    def show_goal_menu(self, event, goal):
        """显示目标右键菜单"""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="编辑", command=lambda: self.edit_goal(goal))
        menu.add_command(label="删除", command=lambda: self.delete_goal(goal))
        menu.post(event.x_root, event.y_root)

    def edit_goal(self, goal):
        """编辑目标"""
        self.reset_activity_timer()  # 重置计时器
        edit_window = tk.Toplevel(self.root)
        edit_window.title(self.lang.get_text('dialog.edit_goal'))
        edit_window.geometry("300x200")
        edit_window.configure(bg=self.current_theme['bg'])
        
        # 设置模态窗口
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        # 文本输入框
        text_frame = tk.Frame(edit_window, bg=self.current_theme['bg'])
        text_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(text_frame, text="目标内容:", bg=self.current_theme['bg'],
                fg=self.current_theme['fg'], font=('微软雅黑', 10)).pack(anchor='w')
        
        text_var = tk.StringVar(value=goal['text'])
        entry = tk.Entry(text_frame, textvariable=text_var,
                        font=('微软雅黑', 10),
                        bg=self.current_theme['secondary_bg'],
                        fg=self.current_theme['fg'],
                        insertbackground=self.current_theme['fg'])
        entry.pack(fill='x', pady=5)
        
        # 优先级选择
        priority_frame = tk.Frame(edit_window, bg=self.current_theme['bg'])
        priority_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(priority_frame, text="优先级:", bg=self.current_theme['bg'],
                fg=self.current_theme['fg'], font=('微软雅黑', 10)).pack(anchor='w')
        
        priority_var = tk.StringVar(value=goal['priority'])
        priorities = [
            ('高', 'high', '🔴'),
            ('中', 'medium', '🟡'),
            ('低', 'low', '🟢')
        ]
        
        for text, value, icon in priorities:
            rb = tk.Radiobutton(priority_frame, text=f'{icon} {text}',
                              variable=priority_var, value=value,
                              bg=self.current_theme['bg'],
                              fg=self.current_theme['fg'],
                              selectcolor=self.current_theme['bg'],
                              font=('微软雅黑', 10))
            rb.pack(side='left', padx=10)
        
        # 按钮框架
        button_frame = tk.Frame(edit_window, bg=self.current_theme['bg'])
        button_frame.pack(side='bottom', pady=10)
        
        def save_changes():
            new_text = text_var.get().strip()
            if new_text:
                goal['text'] = new_text
                goal['priority'] = priority_var.get()
                self.save_data()
                self.update_list()
                edit_window.destroy()
        
        # 保存按钮
        tk.Button(button_frame, text="保存", command=save_changes,
                 bg=self.current_theme['primary'], fg='white',
                 font=('微软雅黑', 10), bd=0, padx=20, cursor='hand2').pack(side='left', padx=5)
        
        # 取消按钮
        tk.Button(button_frame, text="取消", command=edit_window.destroy,
                 bg=self.current_theme['secondary_bg'],
                 fg=self.current_theme['fg'],
                 font=('微软雅黑', 10), bd=0, padx=20, cursor='hand2').pack(side='left', padx=5)

    def delete_goal(self, goal):
        """删除目标"""
        self.reset_activity_timer()  # 重置计时器
        if messagebox.askyesno(
            self.lang.get_text('dialog.confirm_delete'),
            self.lang.get_text('dialog.confirm_delete_message')
        ):
            self.goals[self.current_category].remove(goal)
            self.save_data()
            self.update_list()

    def toggle_goal(self, goal, check_var):
        """切换目标完成状态"""
        self.reset_activity_timer()  # 重置计时器
        goal['completed'] = check_var.get()
        self.save_data()
        self.update_list()

    def toggle_theme(self, event):
        """切换主题"""
        self.reset_activity_timer()  # 重置计时器
        new_theme = "深色" if self.current_theme == Theme.DARK else "浅色"
        self.current_theme = Theme.DARK if self.current_theme == Theme.LIGHT else Theme.LIGHT
        self.root.configure(bg=self.current_theme['bg'])
        self.update_theme()
        self.save_theme()
        logger.info(f'切换{new_theme}主题')

    def update_theme(self):
        """更新主题颜色"""
        # 更新标题栏
        self.title_bar.configure(bg=self.current_theme['primary'])
        for widget in self.title_bar.winfo_children():
            widget.configure(bg=self.current_theme['primary'])
        
        # 更新按钮和输入框的颜色
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=self.current_theme['bg'])
                for child in widget.winfo_children():
                    if isinstance(child, (tk.Button, tk.Radiobutton, tk.Checkbutton)):
                        child.configure(bg=self.current_theme['bg'], 
                                     fg=self.current_theme['fg'])
        
        # 更新日期标签颜色
        if hasattr(self, 'date_label'):
            self.date_label.configure(bg=self.current_theme['bg'],
                                    fg=self.current_theme['fg'])
        
        # 更新列表样式
        style = ttk.Style()
        style.configure('Goal.TCheckbutton', 
                       background='white',
                       font=('微软雅黑', 11))
        
        self.update_list()

    def save_theme(self):
        """保存主题设置"""
        with open('settings.json', 'w') as f:
            json.dump({'theme': 'dark' if self.current_theme == Theme.DARK else 'light'}, f)

    def load_theme(self):
        """加载主题设置"""
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.current_theme = Theme.DARK if settings.get('theme') == 'dark' else Theme.LIGHT
        except:
            pass

    def on_mouse_move(self, event):
        """鼠标移动事件处理"""
        self.last_activity_time = time.time()
        if self.drag_data['dragging']:
            x = self.root.winfo_x() - self.drag_data['x'] + event.x
            y = self.root.winfo_y() - self.drag_data['y'] + event.y
            self.root.geometry(f"+{x}+{y}")
            self.drag_data['x'] = event.x
            self.drag_data['y'] = event.y

    def get_date_range(self):
        """获取当前分类的日期范围"""
        today = datetime.now()
        
        if self.current_category == 'weekly':
            # 获取本周的开始和结束日期
            monday = today - timedelta(days=today.weekday())
            sunday = monday + timedelta(days=6)
            return f"本周 ({monday.strftime('%Y-%m-%d')}至{sunday.strftime('%Y-%m-%d')})"
            
        elif self.current_category == 'monthly':
            # 获取本月的开始和结束日期
            first_day = today.replace(day=1)
            if today.month == 12:
                last_day = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                last_day = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
            return f"本月 ({first_day.strftime('%Y-%m-%d')}至{last_day.strftime('%Y-%m-%d')})"
            
        else:  # yearly
            # 获取本年的开始和结束日期
            first_day = today.replace(month=1, day=1)
            last_day = today.replace(month=12, day=31)
            return f"本年 ({first_day.strftime('%Y-%m-%d')}至{last_day.strftime('%Y-%m-%d')})"

    def update_date_range(self):
        """更新日期范围显示"""
        if hasattr(self, 'date_label'):
            self.date_label.config(text=self.get_date_range())

    def update_category_buttons(self):
        """更新分类按钮状态"""
        buttons = {
            'weekly': self.weekly_btn,
            'monthly': self.monthly_btn,
            'yearly': self.yearly_btn
        }
        
        for category, button in buttons.items():
            if category == self.current_category:
                button.configure(
                    bg=self.current_theme['primary'],
                    fg='white'
                )
            else:
                button.configure(
                    bg=self.current_theme['secondary_bg'],
                    fg=self.current_theme['fg']
                )

    def quit_app(self, event=None):
        """退出应用程序"""
        self.save_data()
        self.root.quit()

    def get_progress_stats(self):
        """获取目标完成进度统计"""
        total = len(self.goals[self.current_category])
        if total == 0:
            return 0, 0
        
        completed = sum(1 for goal in self.goals[self.current_category] if goal['completed'])
        percentage = (completed / total * 100) if total > 0 else 0
        
        return completed, percentage

    @log_operation
    def add_goal(self):
        """添加新目标"""
        self.reset_activity_timer()  # 重置计时器
        text = self.entry.get().strip()
        if not text:
            logger.warning('目标内容为空，取消添加')
            messagebox.showwarning("提示", "请输入目标内容")
            return
            
        try:
            # 记录添加前的状态
            logger.info(f'准备添加目标: {text} (优先级: {self.priority_var.get()})')
            
            # 添加目标
            self.goals[self.current_category].append({
                'text': text,
                'completed': False,
                'priority': self.priority_var.get()
            })
            
            # 清空输入框
            self.entry.delete(0, tk.END)
            
            # 保存数据
            self.save_data()
            
            # 更新显示
            self.update_list()
            
            # 记录成功信息
            logger.info(f'添加目标成功: [{self.current_category}] {text} (优先级: {self.priority_var.get()})')
            
        except Exception as e:
            logger.error(f'添加目标失败: {str(e)}')
            messagebox.showerror("错误", f"添加目标失败: {str(e)}")
            raise

    def reset_activity_timer(self):
        """重置活动计时器"""
        self.last_activity_time = time.time()

    def toggle_language(self, event=None):
        """切换语言"""
        self.lang.toggle_language()
        self.update_ui_text()
        logger.info(f'切换语言到: {self.lang.current_lang}')

    def update_ui_text(self):
        """更新界面文本"""
        # 更新窗口标题
        self.root.title(self.lang.get_text('app_title'))
        
        # 更新分类按钮
        self.weekly_btn.config(text=self.lang.get_text('weekly'))
        self.monthly_btn.config(text=self.lang.get_text('monthly'))
        self.yearly_btn.config(text=self.lang.get_text('yearly'))
        
        # 更新添加按钮
        self.add_btn.config(text=self.lang.get_text('add_button'))
        
        # 更新作者信息
        self.author_label.config(text=self.lang.get_text('author'))
        
        # 更新目标列表
        self.update_list()

if __name__ == '__main__':
    app = GoalTracker()
    app.run()   