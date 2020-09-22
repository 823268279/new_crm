# -*- coding: utf-8 -*-
__author__ = "wowo"


import datetime
from py._xmlgen import html
import pytest
import requests
import random

from comm.comm_way import Way#公共方法
comm_way=Way()


# 添加接口地址与项目名称
def pytest_configure(config):
    config._metadata["项目名称"] = "NEW_CRM_v1.0"
    config._metadata['测试地址'] = 'http://api.newcrm.group.weixin.wuerp.com'
# 添加所属部门与测试人员
@pytest.mark.optionalhook
def pytest_html_results_summary(prefix):
    prefix.extend([html.p("所属部门: 测试部")])
    prefix.extend([html.p("测试人员: wowo")])



#获取请求头
@pytest.fixture(scope='session')    
def session():
    url='http://wcrmmanagement.weixin.wuerp.com/Login/Login'
    data={
            "txtName":"miscs3",
            "txtPwd":"111111",
            "txtCode":"1234",
            "date":""
            }
    try:
        session=requests.session()
        response=session.post(url=url,data=data)
        response_json = comm_way.response_dispose(response.json())
        print(response_json)
        print('登录成功')
        assert response.status_code == 200
        assert response_json['Success'] == True
        return session
    except:
        raise


#web端的配置
@pytest.fixture(scope='session')   
def manage():
    data={
        "username":"miscs3",
        "password":"111111",
        "url":'http://wcrmmanagement.weixin.wuerp.com%s'
        }
    return data


#获取当前时间
@pytest.fixture(scope='function')  
def now_time():
    data={}
    data['ymd']=datetime.datetime.now().strftime('%Y-%m-%d')
    data['ymd_hms']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['StDt']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['EnDt']=(datetime.datetime.now()+datetime.timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')
    data['later']=(datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    return data

#商品资料
@pytest.fixture(scope='function')  
def commodity_data_random():
    data={}
    a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z']
    b = ['袋','包','盒','瓶','件','箱','个']
    c = ['黑龙江','山东','河南','湖北','山西','安徽','湖南','陕西','福建','吉林','四川','甘肃','江苏','云南','贵州',
            '江西','浙江','海南','辽宁','台湾','河北','青海','广东']
    #赠品编码
    data['GdsID']='%s%s' % (sum(random.sample(range(10000,90000),4)),sum(random.sample(range(100,900000),4)))
    #赠品品牌
    data['Fctry']='赠品品牌%s%s' % (random.choice(a),sum(random.sample(range(100,1000),2)))
    #赠品名称
    data['Name']='赠品名称%s%s' % (random.choice(a),sum(random.sample(range(100,1000),2)))
    #赠品规格
    data['Spc']='%sg' % sum(random.sample(range(50,400),2))
    #赠品单位
    data['Unit']=random.choice(b)
    #赠品进货价
    purchasing_price = int(sum(random.sample(range(2000,7000),2)))
    data['PurPrc']=purchasing_price
    #赠品零售价
    data['SalPrc']=purchasing_price + sum(random.sample(range(500,2000),2))
    #赠品产地
    data['Plc']=random.choice(c)
    return data

#随机活动数据
@pytest.fixture(scope='function') 
def activity_data_random():
    data={}
    a = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z']
    data['Name'] = '会员活动%s%s%s%s'% (random.choice(a),random.choice(a),sum(random.sample(range(10,100),2)),sum(random.sample(range(10,100),2)))
    data['Parval'] = sum(random.sample(range(1000,3000),1)) # 兑换线
    data['Amt'] = sum(random.sample(range(3000,7000),1)) # 赠送积分
    return data

#随机会员数据
@pytest.fixture(scope='function')   
def menber_data_random():
    data={}
    a = ['01','02','03','04']
    b = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                'U', 'V', 'W', 'X', 'Y', 'Z']
    c = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z']
    #openid
    x = '%s%s%s%s%s%s%s-'%(random.choice(b),random.choice(b),random.choice(b),random.choice(b),random.choice(b),random.choice(b),random.choice(b))
    y = '%s%s%s-%s%s%s%s'%(random.choice(c),random.choice(c),random.choice(c),random.choice(c),random.choice(c),random.choice(c),random.choice(c))
    z = '%s%s%s%s%s-%s%s'%(random.choice(b),random.choice(b),random.choice(b),random.choice(b),random.choice(b),random.choice(b),random.choice(b))
    data['OpnID']='%s%s%s'%(x,y,z)
    data['UnionID']='%s%s%s'%(x,y,z)
    #卡类型
    data['VipTpID']=random.choice(a)  
    #姓名
    q1 = '%s%s' % (random.choice(b),random.choice(b))
    q2 = '%s%s%s%s%s' % (random.choice(c),random.choice(c),random.choice(c),random.choice(c),random.choice(c))
    data['Name']='%s%s' % (q1,q2)
    #手机
    data['Tel']='13%s%s' % (sum(random.sample(range(10000,100000),1)),sum(random.sample(range(1000,10000),1)))
    #生日
    e1 = '19%s'% (sum(random.sample(range(10,100),1)))
    e2 = '0%s'% sum(random.sample(range(1,10),1))
    e3 = '%s'% sum(random.sample(range(10,29),1))
    data['Brth']='%s-%s-%s'% (e1,e2,e3)
    #身份证
    r1 = '%s'% sum(random.sample(range(1000,10000),1)) 
    r2 = '%s%s%s'% (e1,e2,e3)
    r3 = '%s'% sum(random.sample(range(1000,10000),1)) 
    data['IDntNmb']='51%s%s%s'% (r1,r2,r3)
    return data

# 随机充值金额
@pytest.fixture(scope='module')   
def top_up_data_random():
    data={}
    data['SumParval'] = sum(random.sample(range(1000,10000),2))
    return data

# 随机调整积分
@pytest.fixture(scope='module')   
def integral_adjustment_data_random():
    data={}
    data['IntgModi'] = sum(random.sample(range(10000,700000),2))
    return data

#随机优惠券数据
@pytest.fixture(scope='module')   
def ticket_data_random():
    data={}
    # 券ID
    TknID = sum(random.sample(range(100000,1000000),2))
    # 满送金额线
    ConsumeMoney = random.choice(range(200,500))
    # 满送券面额
    Tknvl = random.choice(range(50,150))
    # 券名称
    name = '消费%s,即可使用' % (ConsumeMoney)
    # 送券描述
    SndRul = '消费大于等于%s,即可使用面额为%s的优惠券' % (ConsumeMoney,Tknvl)
    data['ConsumeMoney']=ConsumeMoney
    data['Tknvl']=Tknvl
    data['Name']=name
    data['SndRul']=SndRul
    data['TknID']=TknID
    return data

# random parking data
@pytest.fixture(scope='function')   
def parking_data_random():
    data={}
    #停车场编号
    data['ParkID']=sum(random.sample(range(10000000,999999999),4))
    #故障热线
    data['Tel']='13%s%s' % (sum(random.sample(range(10000,100000),1)),sum(random.sample(range(1000,10000),1)))
    return data

# random car data
@pytest.fixture(scope='function') 
def car_data_random():
    a = ['法拉利','兰博基尼','大众','丰田','马自达','别克','雪佛兰','福特','标志','现代','奔驰','奥迪','宝马','比亚迪']
    b = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    data={}
    #车辆编号
    data['CarID'] = '川Y%s%s%s'% (random.choice(b),random.choice(b),sum(random.sample(range(300),3)))
    data['carTp'] = random.choice(a)
    return data

# # mysql random select table:commodity_data
# @pytest.fixture(scope='session')    
# def commodity_data_random():
#     return comm_way.sql_select_commodity_data('commodity_data')


# random park order data
@pytest.fixture(scope='function') 
def park_order_data_random():
    data={}
    # 停车订单号
    data['BllNo']=sum(random.sample(range(10000000,999999999),4))
    data['JoinDt']=(datetime.datetime.now()-datetime.timedelta(hours=random.choice(range(1,24)))).strftime('%Y-%m-%d %H:%M:%S')
    return data

# random store data
@pytest.fixture(scope='function') 
def store_data_random():
    data={}
    # store code
    data['StoreID']=sum(random.sample(range(10000000,999999999),4))
    # telephone number
    data['Tel']='13%s%s' % (sum(random.sample(range(10000,100000),1)),sum(random.sample(range(1000,10000),1)))
    return data

# random putaway activity data
@pytest.fixture(scope='function') 
def putaway_activity_data_random():
    data={}
    # bllno_number
    data['BllNo']=sum(random.sample(range(10000000,999999999),4))
    # activity name
    data['Name']='上架活动%s'% sum(random.sample(range(100,700),2))
    # exchange integral
    data['FcttsIntg']=sum(random.sample(range(5000,20000),2))
    return data


# 收银机请求头
@pytest.fixture(scope='function') 
def cash_register_header():
    hdr_json = {
                  "hdr": {
                        "row": {
                              "command": "0",#指令
                              "postype": "0",#商城类型
                              "corpid": "200002",#企业编号
                              "organ": "0000",#机构
                              "posid": "POS006",#收银机编号
                              "billid": "",#消费小票号
                              "receid": "1001",#门店
                              "credential": "28ee304a-8aae-11ea-aa9f-00e04c361826",#收银机标识符
                              "keyid": "",
                              "types": "1"
                        }
                  }
            }
    return hdr_json








# mysql select gift_data
@pytest.fixture(scope='session')    
def gift_data():
    return comm_way.sql_select('gift_data')

# mysql select register_activity_gift_data
@pytest.fixture(scope='session')    
def register_activity_gift_data():
    return comm_way.sql_select('register_activity_gift_data')

# mysql select register_activity_integral_data
@pytest.fixture(scope='session')    
def register_activity_integral_data():
    return comm_way.sql_select('register_activity_integral_data')

# mysql select member_register_data
@pytest.fixture(scope='session')    
def member_register_data():
    return comm_way.sql_select('member_register_data')


# mysql select vip_data
@pytest.fixture(scope='session')    
def vip_data():
    return comm_way.sql_select('vip_data')

# mysql select vipcard_data
@pytest.fixture(scope='session')    
def vipcard_data():
    return comm_way.sql_select('vipcard_data')

# mysql select top_up_activity_gift_data
@pytest.fixture(scope='session')    
def top_up_activity_gift_data():
    return comm_way.sql_select('top_up_activity_gift_data')

# mysql select top_up_activity_integral_data
@pytest.fixture(scope='session')    
def top_up_activity_integral_data():
    return comm_way.sql_select('top_up_activity_integral_data')


# mysql select member_top_up_data
@pytest.fixture(scope='session')    
def member_top_up_data():
    return comm_way.sql_select('member_top_up_data')

# mysql select integral_adjustment_data
@pytest.fixture(scope='session')    
def integral_adjustment_data():
    return comm_way.sql_select('integral_adjustment_data')

# mysql select member_account
@pytest.fixture(scope='session')    
def member_account():
    return comm_way.sql_select('member_account')


# mysql select exchange_activity_data_a
@pytest.fixture(scope='session')    
def exchange_activity_data_a():
    return comm_way.sql_select('exchange_activity_data_a')

# mysql select exchange_activity_data_b
@pytest.fixture(scope='session')    
def exchange_activity_data_b():
    return comm_way.sql_select('exchange_activity_data_b')


# mysql select integral_exchange_data_a
@pytest.fixture(scope='session')    
def integral_exchange_data_a():
    return comm_way.sql_select('integral_exchange_data_a')


# mysql select member_freeze_data
@pytest.fixture(scope='function')    
def member_freeze_data():
    return comm_way.sql_select('member_freeze_data')