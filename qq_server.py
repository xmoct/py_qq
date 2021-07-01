#coding=utf-8
import logging
import socket
import json

from com.qq.server.reg_dao import RegDao
from com.qq.server.user_dao import UserDao

import traceback as tb

logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(threadName)s - '
                               '%(name)s - %(funcName)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)      # 1
# 服务器端IP
#SERVER_IP = '127.0.0.1'
#SERVER_IP = '192.168.1.106'
SERVER_IP = ''  # 接收所有的请求地址
# 服务器端口号
SERVER_PORT = 8888

# 操作命令代码
COMMAND_LOGIN = 1           # 登录命令       # 2
COMMAND_LOGOUT = 2          # 下线命令
COMMAND_SENDMSG = 3         # 发信息命令
COMMAND_REFRESH = 4         # 刷新好友列表命令     # 3
COMMAND_REGUSER = 5         # 注册命令
COMMAND_FILE = 6            # 发送文件命令
COMMAND_ADDFRIEND = 7       # 添加好友命令
COMMAND_AGREE = 8           # 同意添加命令
COMMAND_REFUSE = 9          # 拒绝添加命令
COMMAND_CHANGESTATE = 10    # 更改状态命令
COMMAND_DELFRIEND = 11      # 删除好友

# 所有引进登录的客户端信息
clientlist = []

# 初始化UDP Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))

logger.info('服务器端启动，监听自己的{1}端口{0}...'.format(SERVER_PORT, SERVER_IP))
# 创建字节序列对象，作为接受数据的缓冲区
buffer = []

# 主循环 等待客户端请求-接收到请求-处理-返回数据客户端
while True:
    # TODO 服务器端处理
    try:
        # 接受数据包
        data, client_address = server_socket.recvfrom(1024)
        json_obj = json.loads(data.decode())
        logger.info('服务器端接受客户端，消息：{0}'.format(json_obj))
        
        # 取出客户端传递过来的 操作命令
        command = json_obj['command']

        if command == COMMAND_LOGIN:    # 用户登录过程
            # TODO 用户登录过程
            # 通过用户Id查询用户信息
            userid = json_obj['user_id']
            userpwd = json_obj['user_pwd']
            logger.debug('user_id:{0} user_pwd:{1}'.format(userid, userpwd))

            dao = UserDao()
            user = dao.findbyid(userid)
            logger.info(user)

            # 判断客户端发送过来的密码与数据库的密码是否一致
            if user is not None and user['user_pwd'] == userpwd:    # 登录成功
                # 登录成功
                logger.info('登录成功')
                # 创建保存用户登录信息的二元组
                clientinfo = (userid, client_address)

                # 用户登录信息添加到clientinfo
                clientlist.append(clientinfo)

                json_obj = user
                json_obj['result'] = '0'
                
                # 取出好友用户列表
                dao = UserDao()
                friends = dao.findfriends(userid)
                # 返回clientinfo中userid列表
                cinfo_userids = map(lambda it: it[0], clientlist)

                for friend in friends:
                    fid = friend['user_id']
                    # 添加好友状态，‘1’在线，‘0’离线
                    friend['online'] = '0'
                    if fid in cinfo_userids:    # 用户登录
                        friend['online'] = '1'

                json_obj['friends'] = friends
                logger.info('服务器端发送用户成功，消息：{0}'.format(json_obj))

                #  编码json
                json_str = json.dumps(json_obj)
                # 给客户端发送消息
                server_socket.sendto(json_str.encode(), client_address)
            else:   # 登录失败
                json_obj = {}
                json_obj['result'] = '-1'
                # json编码
                json_str = json.dumps(json_obj)
                # 给客户端
                server_socket.sendto(json_str.encode(), client_address)

        elif command == COMMAND_SENDMSG:    # 用户发送消息
            # TODO 用户消息
            # 获得好友Id
            fduserid = json_obj['receive_user_id']
            # 向客户端发送数据
            # 在clientlist中查找好友Id
            filter_clientinfo = filter(lambda it: it[0] == fduserid, clientlist)
            clientinfo = list(filter_clientinfo)
            print(clientinfo)
            print(clientlist)
            print(len(clientinfo))
            if len(clientinfo) == 1:
                _, client_address = clientinfo[0]

                # 服务器端转发消息给客户端
                # JSON编码
                json_str = json.dumps(json_obj)
                server_socket.sendto(json_str.encode(), client_address)

        elif command == COMMAND_REGUSER:
            # 注册用户Id
            userid = json_obj['user_id']
            userpwd = json_obj['user_pwd']
            username = json_obj['user_name']
            logger.debug('user_id:{0} user_pwd:{1}'.format(userid, userpwd))

            dao = RegDao()
            user = dao.getQQcode(userid, userpwd, username)
            logger.info(user)

            # 判断客户端发送过来的密码与数据库的密码是否一致
            if user is not None:    # 开始注册成功
                # 登录成功
                logger.info('注册成功')
                # 创建保存用户登录信息的二元组
                clientinfo = (userid, client_address)
                #  编码json
                json_str = json.dumps(json_obj)
                # 给客户端发送消息
                server_socket.sendto(json_str.encode(), client_address)

        elif command == COMMAND_LOGOUT:
            # TODO用户发送消息
            # 获得用户Id
            userid = json_obj['user_id']
            for clientinfo in clientlist:
                cuserid, _ = clientinfo
                if cuserid == userid:
                    # 从clientlist 列表中删除用户
                    clientlist.remove(clientinfo)
                    break

            logger.info(clientlist)
        # TODO刷新用户消息
        # 如果clientlist中没有元素则跳到下次循环
        if len(clientlist) == 0:
            continue
        
        json_obj = {}
        json_obj['command'] = COMMAND_REFRESH
        usersid_map = map(lambda it: it[0],clientlist)
        useridlist = list(usersid_map)
        json_obj['OnlineUserList'] = useridlist

        for clientinfo in clientlist:
            _, address = clientinfo
            # json编码
            json_str = json.dumps(json_obj)
            # 给客户端发送数据
            server_socket.sendto(json_str.encode(), address)

    except Exception:
        tb.print_exc()
        logger.info('timed out')
