# coding=utf-8

"""定义Frame窗口基类"""
import logging
import socket
import sys

import wx

logger = logging.getLogger(__name__)      # 1

# 服务器IP
#SERVER_IR = input("请输入server地址：")
SERVER_IR = "192.168.1.108"
#SERVER_IR = '127.0.0.1'
# 服务器端口号
SERVER_PORT = 8888

# 服务器端地址
server_address = (SERVER_IR,SERVER_PORT)

# 操作命令代码
COMMAND_LOGIN = 1  # 登录命令       # 2
COMMAND_LOGOUT = 2  # 下线命令
COMMAND_SENDMSG = 3  # 发信息命令
COMMAND_REFRESH = 4  # 刷新好友列表命令     # 3
COMMAND_REGUSER = 5  # 注册命令
COMMAND_FILE = 6  # 发送文件命令
COMMAND_ADDFRIEND = 7  # 添加好友命令
COMMAND_AGREE = 8  # 同意添加命令
COMMAND_REFUSE = 9  # 拒绝添加命令
COMMAND_CHANGESTATE = 10  # 更改状态命令
COMMAND_DELFRIEND = 11  # 删除好友

# 初始化UDP Socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)   # 4
# 设置超时2秒，不在等待接受数据
client_socket.settimeout(2)      # 5

class MyFrame( wx.Frame ):

    def __init__(self, title, size):
        super().__init__(parent=None, title=title, size=size,
                        style=wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX)
        # 设置窗口居中
        self.Centre()
        # 设置Frame窗口内容面板
        self.contentpanel = wx.Panel(parent=self)
 
        ico = wx.Icon('resources/icon/qq1.ico', wx.BITMAP_TYPE_ICO)
        # 设置窗口图标
        self.SetIcon(ico)
        # 设置窗口的最大和最小尺寸
        self.SetSizeHints(size,size)
        self.Bind(wx.EVT_CLOSE,self.OnClose)
    
    def OnClose(self, event):
        # 退出系统
        self.Destroy()
        client_socket.close()
        sys.exit(0)


# 一到五是窗口模块定义的变量，2和3是定义操作命令代码，4是窗口创建基于UDP SOCKET的对象，5是设置socket的超时时间
