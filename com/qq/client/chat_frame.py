# coding=utf-8
"""好友列表窗口"""

import datetime
import json
import threading

import wx

from com.qq.client.my_frame import *

class ChatFrame(MyFrame) :
    def __init__(self, friendsframe, user, friend):
        super().__init__(title='', size=(450, 400))

        self.friendsframe = friendsframe

        self.user = user
        self.friend = friend

        title = '{0}与{1}聊天中……'.format(user['user_name'], friend['user_name'])
        self.SetTitle(title)

        # 创建查看消息文本输入控件
        self.seemsg_tc = wx.TextCtrl(self.contentpanel,
                                     style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.seemsg_tc.SetFont(wx.Font(wx.Font(11, wx.FONTFAMILY_DEFAULT,
                                               wx.FONTSTYLE_NORMAL,
                                               wx.FONTWEIGHT_NORMAL, faceName='微软雅黑')))

        # 底部发消息面板
        bottompanel = wx.Panel(self.contentpanel, style=wx.DOUBLE_BORDER)

        bottomhbox = wx.BoxSizer()

        # 创建发送消息文本输入控件
        self.sendmsg_tc = wx.TextCtrl(bottompanel)
        # 为发送消息文本输入控件设置焦点
        self.sendmsg_tc.SetFocus()
        self.sendmsg_tc.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT,
                                        wx.FONTSTYLE_NORMAL,
                                        wx.FONTWEIGHT_NORMAL, faceName='微软雅黑'))

        # 创建发送消息的按钮
        sendmsg_btn = wx.Button(bottompanel,label="发送")
        self.Bind(wx.EVT_BUTTON, self.on_click, sendmsg_btn)

        bottomhbox.Add(self.sendmsg_tc, 5, wx.CENTER | wx.ALL | wx.EXPAND, border=5)
        bottomhbox.Add(sendmsg_btn, 1, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

        bottompanel.SetSizer(bottomhbox)

        # 创建整体box布局管理对象
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.seemsg_tc, 5, wx.CENTER | wx.ALL | wx.EXPAND, border=5)
        box.Add(bottompanel, 1, wx.CENTER | wx.ALL | wx.EXPAND, border=5)
        self.contentpanel.SetSizer(box)

        # 消息日志
        self.msglog = ''

        # 子线程运行状态
        self.isrunning = True
        # 创建一个子线程
        self.t1 = threading.Thread(target=self.thread_body)
        # 启动线程t1
        self.t1.start()

    def thread_body(self):
        # 当前线程对象
        while self.isrunning:
            try:
                # 从服务器端接受数据
                json_data, _ = client_socket.recvfrom(1024)
                # json解码
                json_obj = json.loads(json_data.decode())
                logger.info('CharFrame从服务器端接收数据：{0}'.format(json_obj))
                command = json_obj['command']
                
                # command不等于空值时执行
                if command is not None and command == COMMAND_REFRESH: # 刷新好友列表
                    # 获得好友列表
                    userids = json_obj['OnlineUserList']
                    # 刷新好友列表
                    self.friendsframe.refreshfriendlist(userids)

                # TODO 接收聊天消息
                else:
                    # 获得当前时间，并格式化
                    now = datetime.datetime.today()
                    strnow = now.strftime('%Y-%m-%d %H:%M:%S')
                    # 在消息查看框中显示信息
                    message = json_obj['message']
                    log = "#{0}#\n{1}对您说：{2}\n".format(strnow, self.friend['user_name'], message)
                    self.msglog += log
                    self.seemsg_tc.SetValue(self.msglog)
                    # 光标显示在最后一行
                    self.sendmsg_tc.SetInsertionPointEnd()

            except Exception:
                # 出现异常，休眠2秒，再接收数据
                # time.sleep(2)
                continue
    # TODO 发送信息
    def on_click(self, event):
        #  发送消息
        if self.sendmsg_tc.GetValue() != ' ':
            now = datetime.datetime.today()
            strnow = now.strftime('%Y-%m-%d %H:%M:%S')
            #  在消息查看框中显示消息
            msg = '#{0}#\n您对{1}说: {2}\n'.format(strnow,
                    self.friend['user_name'], self.sendmsg_tc.GetValue())
            self.msglog += msg
            self.seemsg_tc.SetValue(self.msglog)
            # 光标显示在最后一行
            self.seemsg_tc.SetInsertionPointEnd()

            # 向服务器端发送消息
            json_obj = {}
            json_obj['command'] = COMMAND_SENDMSG
            json_obj['user_id'] = self.user['user_id']
            json_obj['message'] = self.sendmsg_tc.GetValue()
            json_obj['receive_user_id'] = self.friend['user_id']

            # JSON编码
            json_str = json.dumps(json_obj)
            # 给服务器端发送数据
            client_socket.sendto(json_str.encode(), server_address)
            # 清空发送消息文本框
            self.sendmsg_tc.SetValue('')

    # TODO 接受信息
    # 重写 OnClose方法
    def OnClose(self,event):
        self.isrunning = False
        self.t1.join()
        self.Hide()
        # 重启好友列表窗口子线程
        self.friendsframe.resettread()
