# coding=utf-8
import wx

from com.qq.client.login_frame import *
from com.qq.client.my_frame import *
import json

from com.qq.server.reg_dao import RegDao

"""定义Frame窗口基类"""
class RegFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='用户注册', size=(340, 260))

        #super().__init__(parent=None, title='用户注册')
        # wx.Frame.__init__(self, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
        #                   size=wx.Size(444, 317), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        # 设置窗口图标
        ico = wx.Icon('resources/icon/qq1.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
        # wx.DefaultSize wx.Size(340, 255)
        #self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.Colour(248, 187, 253))
        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"欢迎注册账号", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        self.m_staticText1.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))

        bSizer2.Add(self.m_staticText1, 0, wx.ALL, 5)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"开心每一天o(*￣▽￣*)ブ", wx.DefaultPosition, wx.DefaultSize,
                                           0)
        self.m_staticText2.Wrap(-1)
        bSizer2.Add(self.m_staticText2, 0, wx.ALL, 5)

        bSizer1.Add(bSizer2, 1, wx.EXPAND, 5)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        self.accname_txt = wx.TextCtrl(self, wx.ID_ANY, u"昵称", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer3.Add(self.accname_txt, 0, wx.ALL | wx.EXPAND, 5)

        self.accountid_txt = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer3.Add(self.accountid_txt, 0, wx.ALL | wx.EXPAND, 5)

        self.password_txt = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD)
        bSizer3.Add(self.password_txt, 0, wx.ALL | wx.EXPAND, 5)

        gSizer1 = wx.GridSizer(0, 2, 0, 0)

        gSizer1.SetMinSize(wx.Size(-1, 30))
        Icon = [u"18", u"23", u"25", u"28", wx.EmptyString]
        self.m_choice2 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, Icon, 0)
        self.m_choice2.SetSelection(0)
        gSizer1.Add(self.m_choice2, 0, wx.EXPAND, 5)

        self.m_Text3 = wx.StaticText(self, wx.ID_ANY, u"头像选择", wx.DefaultPosition, wx.DefaultSize, 0)

        gSizer1.Add(self.m_Text3, 0, wx.ALIGN_CENTER, 5)

        bSizer3.Add(gSizer1, 1, wx.ALL|wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        m_btn1 = wx.Button(self, wx.ID_ANY, u"立即注册", wx.Point(-1, -1), wx.DefaultSize, 0 | wx.NO_BORDER)
        m_btn1.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False))
        m_btn1.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.Bind(wx.EVT_BUTTON, self.reg_btn_onclick, m_btn1)


        bSizer3.Add(bSizer4, 1, wx.EXPAND, 5)

        bSizer1.Add(bSizer3, 1, wx.EXPAND, 5)
        bSizer4.Add(m_btn1, 0, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

    def reg_btn_onclick(self, user):
        """注册按钮事件处理"""

        accname = self.accname_txt.GetValue()
        account = self.accountid_txt.GetValue()
        password = self.password_txt.GetValue()
        Icon = self.Icon.GetValue()
        users = self.regUser(accname, account, password, Icon)
        print(users)

        if users is not None:
            logger.info('注册成功.')
            next_frame = LoginFrame(users)     # 界面跳转
            next_frame.Show()
            self.Hide()
        else:
            logger.info('注册失败')
            dlg= wx.MessageDialog(self, '您QQ号码重复或格式不规范',
                                  ' 注册失败 ',
                                  wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

    def regUser(self, accname, userid, password):
        """客户端向服务器端发送注册请求"""

        json_obj = {}
        json_obj['command'] = COMMAND_REGUSER
        json_obj['user_id'] = userid
        json_obj['user_pwd'] = password
        json_obj['user_name'] = accname

        # JSON编码
        json_str = json.dumps(json_obj)

        # 向服务器端发送数据
        client_socket.sendto(json_str.encode(), server_address)
        logger.info("client发送的信息：{0}".format(server_address))

        # 从服务器器端接收数据
        json_data, _ = client_socket.recvfrom(1024)
        # JSON解码
        json_obj = json.loads(json_data.decode())
        logger.info('从服务器端接收数据: {0}'.format(json_obj))

        if json_obj['result'] == '0':
            # 注册成功
            return json_obj

class App(wx.App):

    def OnInit(self):
        # 创建窗口对象
        frame = RegFrame()
        frame.Show()
        return True

if __name__ == '__main__':
    app = App()
    app.MainLoop()  # 进入主事件循环
