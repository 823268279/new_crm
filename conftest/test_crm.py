# -*- coding: utf-8 -*-
__author__ = "wowo"



import random
from comm.comm_way import Way#公共方法
comm_way=Way()



# 机构
def test_get_organization(manage,session):
    data={}
    try:
        response=session.post(url=manage['url'] % '/Basics/CpnOrg/GetTree',data=data)
        response_json = comm_way.response_dispose(response.json())
        print(response_json['Message'])
        assert response.status_code == 200
        assert response_json['Success'] == True    
        print(response_json['Data']['Data'])                 
    except:
            raise

# 赠品
class Test_gift():
    # add
    def test_add_gift(self,manage,session,commodity_data_random):
        data={}
        try:
            data["model[GdsID]"] = commodity_data_random['GdsID']
            data["model[Name]"] = commodity_data_random['Name']
            data["model[SalPrc]"] = commodity_data_random['SalPrc']
            data["model[PurPrc]"] = commodity_data_random['PurPrc']
            data["model[Spc]"] = commodity_data_random['Spc']
            data["model[Bcd]"] = commodity_data_random['GdsID']
            data["model[HlpCd]"] = ''
            data["model[Unit]"] = commodity_data_random['Unit']
            data["model[Plc]"] = commodity_data_random['Plc']
            data["model[Fctry]"] = commodity_data_random['Fctry']
            data["model[Source]"] = ''
            data["model[BndInfo]"] = ''
            data["model[ImgUrl]"] = ''
            data["model[Dsc]"] = ''
            data["model[Brf]"] = 'apitest'
            data["type"] = '1'
            response=session.post(url=manage['url'] % '/Basics/CpnGft/Add',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json)
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True    
        except:
                raise
    # select page
    def test_get_gift_data_page(self,session,manage):
        data={'dtGridPager': '{"errorMsg":"","isExport":false,"pageSize":10,"startRecord":0,"nowPage":1,"recordCount":88,"pageCount":9,"parameters":{"GdsID":"","Name":""},"fastQueryParameters":{},"advanceQueryConditions":[],"advanceQuerySorts":[]}'}
        try:
            response=session.post(url=manage['url'] % '/Basics/CpnGft/CpnGftQueryList',data=data)
            response_json = comm_way.response_dispose(response.json())
            assert response.status_code == 200
            assert response_json['Issuccess'] == True    
            if response_json['Exhibitdatas']:
                comm_way.sql_insert('gift_data',response_json['Exhibitdatas'][0])
                for i in response_json['Exhibitdatas']:
                    print(i)
            else:
                print('没有商品')
        except:
                raise
# 注册活动送实物
class Test_register_activity_gift():
    # add
    def test_add_register_activity(self,manage,session,activity_data_random,menber_data_random,now_time,gift_data):
        data={}
        try:
            data['t[Name]'] = activity_data_random['Name']
            data['t[VipTps]'] = menber_data_random['VipTpID']
            data['t[PrmtTyp]'] = '1'
            data['t[StDt]'] = now_time['StDt']
            data['t[EnDt]'] = now_time['EnDt']
            data['t[Brf]'] = 'apitest'
            data['Vipdtl[0][Tp]'] = '2'
            data['Vipdtl[0][GdsID]'] = gift_data['GdsID']
            data['Vipdtl[0][Name]'] = gift_data['Name']
            data['Vipdtl[0][Parval]'] = gift_data['SalPrc'] 
            data['Vipdtl[0][Qty]'] = '2'
            data['Vipdtl[0][Amt]'] = '0'
            data['Vipdtl[0][Brf]'] = 'apitest'
            data['Vipdtl[0][CanlFlg]'] = 'F'
            response=session.post(url=manage['url'] % '/Basics/VipPrmt/Add',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True    
        except:
            raise
    # select page
    def test_get_register_activity_page(self,manage,session):
        data={'dtGridPager':'{"errorMsg":"","isExport":false,"pageSize":10,"startRecord":0,"nowPage":1,"recordCount":-1,"pageCount":-1,"parameters":{},"fastQueryParameters":{},"advanceQueryConditions":[],"advanceQuerySorts":[]}'}
        try:
            response=session.post(url=manage['url'] % '/Basics/VipPrmt/VipPrmtQueryList',data=data)
            response_json = comm_way.response_dispose(response.json())
            assert response.status_code == 200
            assert response_json['Issuccess'] == True   
            if response_json['Exhibitdatas']:
                print(response_json['Exhibitdatas'][0])
                comm_way.sql_insert('register_activity_gift_data',response_json['Exhibitdatas'][0])
                for i in response_json['Exhibitdatas']:
                    print(i)
            else:
                print('没有活动')
        except:
            raise
    # check
    def test_check_register_activity(self,manage,session,register_activity_gift_data):
        data={}
        try:
            data={
                "bllNo":"",
                "examineStt":"50"}

            data['bllNo'] = register_activity_gift_data['BllNo']
            data['examineStt'] = '50'
            response=session.post(url=manage['url'] % '/Basics/VipPrmt/ToExamine',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise

# 注册活动送积分
class Test_register_activity_integral():
    # add
    def test_add_register_activity(self,manage,session,now_time,register_activity_gift_data,activity_data_random):
        data={}
        try:
            while True:
                data['t[VipTps]']= random.choice(['01','02','03','04'])
                if data['t[VipTps]'] == register_activity_gift_data['VipTps']:
                    continue
                else:
                    break
            data['t[Name]'] = activity_data_random['Name']
            data['t[StDt]'] = now_time['StDt']
            data['t[EnDt]'] = now_time['EnDt']
            data['t[PrmtTyp]'] = '1'
            data['t[Brf]'] = 'apitest'
            data['Vipdtl[0][Tp]'] = '3'
            data['Vipdtl[0][GdsID]'] = ''
            data['Vipdtl[0][Name]'] = '积分'
            data['Vipdtl[0][Parval]'] = '0'
            data['Vipdtl[0][Qty]'] = '0'
            data['Vipdtl[0][CanlFlg]'] = 'F'
            data['Vipdtl[0][Amt]'] = activity_data_random['Amt']
            data['Vipdtl[0][Brf]'] = 'apitest'
            response=session.post(url=manage['url'] % '/Basics/VipPrmt/Add',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise
    # select page
    def test_get_register_activity_page(self,manage,session):
        data={'dtGridPager':'{"errorMsg":"","isExport":false,"pageSize":10,"startRecord":0,"nowPage":1,"recordCount":-1,"pageCount":-1,"parameters":{},"fastQueryParameters":{},"advanceQueryConditions":[],"advanceQuerySorts":[]}'}
        try:
            response=session.post(url=manage['url'] % '/Basics/VipPrmt/VipPrmtQueryList',data=data)
            response_json = comm_way.response_dispose(response.json())
            assert response.status_code == 200
            assert response_json['Issuccess'] == True   
            if response_json['Exhibitdatas']:
                comm_way.sql_insert('register_activity_integral_data',response_json['Exhibitdatas'][0])
                for i in response_json['Exhibitdatas']:
                    print(i)
            else:
                print('没有活动')
        except:
            raise
    # check
    def test_check_register_activity(self,manage,session,register_activity_integral_data):
        data={}
        try:
            data={
                "bllNo":"",
                "examineStt":"50"}

            data['bllNo'] = register_activity_integral_data['BllNo']
            data['examineStt'] = '50'
            response=session.post(url=manage['url'] % '/Basics/VipPrmt/ToExamine',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise

# 注册会员
class Test_member_register():
    # add
    def test_add_member_register(self,manage,session,menber_data_random,register_activity_gift_data):
        data={}
        data_sublist={}
        try:
            data_sublist['VipTpID'] = register_activity_gift_data['VipTps']
            data_sublist['CrdTpid'] = '000'
            data_sublist['PrmtNo'] = register_activity_gift_data['BllNo']
            data_sublist['Name'] = menber_data_random['Name']
            data_sublist['Tel'] = menber_data_random['Tel']
            data_sublist['IDntTp'] = ''
            data_sublist['IDntNmb'] = menber_data_random['IDntNmb']
            data_sublist['Brth'] = menber_data_random['Brth']
            data_sublist['Sex'] = '0'
            data['RgstInfo'] = str(data_sublist)
            data['ExAtr'] = ''
            print(data)
            response=session.post(url=manage['url'] % '/Member/VipRgst/Add',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise
    # select page
    def test_get_member_register_page(self,manage,session):
        data={'dtGridPager':'{"errorMsg":"","isExport":false,"pageSize":10,"startRecord":0,"nowPage":1,"recordCount":37,"pageCount":4,"parameters":	{"BllNo":"","Cashier":""},"fastQueryParameters":{},"advanceQueryConditions":[],"advanceQuerySorts":[]}'}
        try:
            response=session.post(url=manage['url'] % '/Member/VipRgst/QueryList',data=data)
            response_json = comm_way.response_dispose(response.json())
            assert response.status_code == 200
            assert response_json['Issuccess'] == True   
            if response_json['Exhibitdatas']:
                comm_way.sql_insert('member_register_data',response_json['Exhibitdatas'][0])
                for i in response_json['Exhibitdatas']:
                    print(i)
            else:
                print('没有活动')
        except:
            raise
    # check
    def test_check_member_register(self,manage,session,member_register_data):
        data={}
        try:
            data={
                "bllNo":"#bllno",
                "examineStt":"50"
             }
            data['bllNo'] = member_register_data['BllNo']
            data['examineStt'] = '50'
            response=session.post(url=manage['url'] % '/Member/VipRgst/ToExamine',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise
# 查询会员资料
class Test_get_member_data():
    # To tel get member data
    def test_get_vip_data(self,manage,session,member_register_data):
        data={'dtGridPager':'{"errorMsg":"","isExport":false,"pageSize":10,"startRecord":400,"nowPage":1,"recordCount":1,"pageCount":1,"parameters":{"Name":"","NickName":"","Tel":"#Tel","CrdNo":"","VipID":""},"fastQueryParameters":{},"advanceQueryConditions":[],"advanceQuerySorts":[]}'}
        try:
            data['dtGridPager']=data['dtGridPager'].replace('#Tel',member_register_data['Tel'])
            print(data)
            response=session.post(url=manage['url'] % '/Basics/Gst/SlecetGstpagingInfo',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json)
            assert response.status_code == 200
            assert response_json['Issuccess'] == True   
            comm_way.sql_insert('vip_data',response_json['Exhibitdatas'][0])
        except:
            raise
    # To CrdID get vipcard data
    def test_get_vipcard_data(self,manage,session,vip_data):
        data={'dtGridPager':'{"errorMsg":"","isExport":false,"pageSize":10,"startRecord":0,"nowPage":1,"recordCount":-1,"pageCount":-1,"parameters":{"GstID":"#GstID"},"fastQueryParameters":{},"advanceQueryConditions":[],"advanceQuerySorts":[]}'}
        try:
            data['dtGridPager']=data['dtGridPager'].replace('#GstID',vip_data['ID'])
            response=session.post(url=manage['url'] % '/Basics/VipCrd/QueryList',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json)
            assert response.status_code == 200
            assert response_json['Issuccess'] == True   
            comm_way.sql_insert('vipcard_data',response_json['Exhibitdatas'][0])
        except:
            raise

# 储值活动送实物
class Test_top_up_activity_gift():
    # add
    def test_add_top_up_activity(self,manage,session,now_time,activity_data_random,vip_data,vipcard_data,gift_data):
        data={}
        try:
            data['model[BllNo]'] = ''
            data['model[PrmtTyp]'] = '1'
            data['model[AtmStt]'] = 'F'
            data['model[UseOrgID]'] = vipcard_data['OrgID']
            data['model[Name]'] = activity_data_random['Name']
            data['model[VipTps]'] = vip_data['VipTpID']
            data['model[StDt]'] = now_time['StDt']
            data['model[EnDt]'] = now_time['EnDt']
            data['model[Brf]'] = 'apitest'
            data['lvl[0][Parval]'] = '0'                            #储值线
            data['lvl[0][Rdx]'] = '1'                            #储值线
            data['lvl[0][Brf]'] = 'apitest'                            #储值线
            data['gft[0][GdsID]'] = gift_data['GdsID']
            data['gft[0][Name]'] = gift_data['Name']
            data['gft[0][Parval]'] = gift_data['SalPrc']
            data['gft[0][Amt]'] = gift_data['SalPrc']
            data['gft[0][GrdRdx]'] = '1'
            data['gft[0][RonDom]'] = ''
            data['gft[0][Tp]'] = '2'
            data['gft[0][Brf]'] = 'apitest'
            data['gft[0][UseOrd]'] = '0'
            data['gft[0][Qty]'] = 'F'
            response=session.post(url=manage['url'] % '/Storvl/RchgPrmt/Add',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise
    # select page
    def test_get_top_up_activity_page(self,manage,session):
        data={'dtGridPager':'{"errorMsg":"","isExport":false,"pageSize":10,"startRecord":0,"nowPage":1,"recordCount":-1,"pageCount":1,"parameters":{},"fastQueryParameters":{},"advanceQueryConditions":[],"advanceQuerySorts":[]}'}
        try:
            response=session.post(url=manage['url'] % '/Storvl/RchgPrmt/QueryList',data=data)
            response_json = comm_way.response_dispose(response.json())
            assert response.status_code == 200
            assert response_json['Issuccess'] == True   
            if response_json['Exhibitdatas']:
                comm_way.sql_insert('top_up_activity_gift_data',response_json['Exhibitdatas'][0])
                for i in response_json['Exhibitdatas']:
                    print(i)
            else:
                print('没有充值活动')
        except:
            raise
    # check
    def test_check_top_up_activity(self,manage,session,top_up_activity_gift_data):
        data={}
        try:
            data={}
            data['bllNo'] = top_up_activity_gift_data['BllNo']
            data['stt'] = '50'
            response=session.post(url=manage['url'] % '/Storvl/RchgPrmt/ToExamine',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise
# 储值活动送积分
class Test_top_up_activity_integral():
    # add
    def test_add_top_up_activity(self,manage,session,activity_data_random,now_time,vip_data,vipcard_data):
        data={}
        try:
            data['model[BllNo]'] = ''
            data['model[Name]'] = activity_data_random['Name']
            data['model[PrmtTyp]'] = '1'
            data['model[AtmStt]'] = 'F'
            data['model[UseOrgID]'] = vipcard_data['OrgID']
            data['model[VipTps]'] = vip_data['VipTpID']
            data['model[StDt]'] = now_time['StDt']
            data['model[EnDt]'] = now_time['EnDt']
            data['model[Brf]'] = 'apitest'
            data['lvl[0][Rdx]'] = '1'
            data['lvl[0][Brf]'] = 'apitest'
            data['lvl[0][Parval]'] = activity_data_random['Parval']
            data['gft[0][Amt]'] = activity_data_random['Amt']
            data['gft[0][GrdRdx]'] = '1'
            data['gft[0][RonDom]'] = ''
            data['gft[0][Tp]'] = '3'
            data['gft[0][Brf]'] = 'apitest'
            data['gft[0][UseOrd]'] = '0'
            data['gft[0][InsTp]'] = '0'
            response=session.post(url=manage['url'] % '/Storvl/RchgPrmt/Add',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise
    # select
    def test_get_top_up_activity_page(self,manage,session):
        data={'dtGridPager':'{"errorMsg":"","isExport":false,"pageSize":10,"startRecord":0,"nowPage":1,"recordCount":-1,"pageCount":1,"parameters":{},"fastQueryParameters":{},"advanceQueryConditions":[],"advanceQuerySorts":[]}'}
        try:
            response=session.post(url=manage['url'] % '/Storvl/RchgPrmt/QueryList',data=data)
            response_json = comm_way.response_dispose(response.json())
            assert response.status_code == 200
            assert response_json['Issuccess'] == True   
            if response_json['Exhibitdatas']:
                comm_way.sql_insert('top_up_activity_integral_data',response_json['Exhibitdatas'][0])
                for i in response_json['Exhibitdatas']:
                    print(i)
            else:
                print('没有充值活动')
        except:
            raise
    # check
    def test_check_top_up_activity(self,manage,session,top_up_activity_integral_data):
        data={}
        try:
            data={}
            data['bllNo'] = top_up_activity_integral_data['BllNo']
            data['stt'] = '50'
            response=session.post(url=manage['url'] % '/Storvl/RchgPrmt/ToExamine',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise
# 会员充值
class Test_member_top_up():
    # add
    def test_add_member_top_up(self,manage,session,vipcard_data,top_up_activity_gift_data,top_up_data_random):
        data={}
        try:
            data['model[BllNo]'] = ''
            data['model[AtmStt]'] = 'F'
            data['model[AccsTyp]'] = '2'
            data['model[VipID]'] = vipcard_data['VipID']
            data['model[CrdNo]'] = vipcard_data['CrdNo']
            data['model[CrdID]'] = vipcard_data['CrdID']
            data['model[GstID]'] = vipcard_data['GstID']
            data['model[PrmtNo]'] = top_up_activity_gift_data['BllNo']
            data['model[SumParval]'] = top_up_data_random['SumParval']
            data['model[RcvAmt]'] = top_up_data_random['SumParval']
            data['model[Parval]'] = top_up_data_random['SumParval']
            data['model[Brf]'] = 'apitest'
            response=session.post(url=manage['url'] % '/Storvl/Rchg/Add',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise
    # select
    def test_get_member_top_up_page(self,manage,session):
        data={'dtGridPager':'{"errorMsg":"","isExport":false,"pageSize":10,"startRecord":0,"nowPage":1,"recordCount":78,"pageCount":8,"parameters":{"BllNo":"","Stt":""},"fastQueryParameters":{},"advanceQueryConditions":[],"advanceQuerySorts":[]}'}
        try:
            response=session.post(url=manage['url'] % '/Storvl/Rchg/QueryList',data=data)
            response_json = comm_way.response_dispose(response.json())
            assert response.status_code == 200
            assert response_json['Issuccess'] == True   
            if response_json['Exhibitdatas']:
                comm_way.sql_insert('member_top_up_data',response_json['Exhibitdatas'][0])
                for i in response_json['Exhibitdatas']:
                    print(i)
            else:
                print('没有充值单')
        except:
            raise
    # check
    def test_check_member_top_up(self,manage,session,member_top_up_data):
        data={}
        try:
            data['bllNo'] = member_top_up_data['BllNo']
            data['stt'] = '50'
            response=session.post(url=manage['url'] % '/Storvl/Rchg/ToExamine',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise

# 积分调整单
class Test_integral_adjustment():
    # add
    def test_add_integral_adjustment(self,manage,session,vipcard_data,integral_adjustment_data_random):
        data={}               
        try:
            data['IntgAva'] = '0'
            data['AccOrgID'] = vipcard_data['OrgID']
            data['VipID'] = vipcard_data['VipID']
            data['GstID'] = vipcard_data['GstID']
            data['IntgModi'] = integral_adjustment_data_random['IntgModi']
            data['IntgModirs'] = '1'
            data['Brf'] = 'apitest'
            response=session.post(url=manage['url'] % '/Basics/IntgCrtn/IntgCrtnAdd',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise
    # select page
    def test_get_integral_adjustment_page(self,manage,session):
        data={'dtGridPager':'{"errorMsg":"","isExport":false,"pageSize":10,"startRecord":0,"nowPage":1,"recordCount":-1,"pageCount":-1,"parameters":{},"fastQueryParameters":{},"advanceQueryConditions":[],"advanceQuerySorts":[]}'}
        try:
            response=session.post(url=manage['url'] % '/Basics/IntgCrtn/SlecetIntgCrtnpagingInfo',data=data)
            response_json = comm_way.response_dispose(response.json())
            assert response.status_code == 200
            assert response_json['Issuccess'] == True   
            if response_json['Exhibitdatas']:
                comm_way.sql_insert('integral_adjustment_data',response_json['Exhibitdatas'][0])
                for i in response_json['Exhibitdatas']:
                    print(i)
            else:
                print('没有充值单')
        except:
            raise
    # check
    def test_check_integral_adjustment(self,manage,session,integral_adjustment_data):
        data={}
        try:
            data['bllNo'] = integral_adjustment_data['BllNo']
            data['stt'] = '50'
            response=session.post(url=manage['url'] % '/Basics/IntgCrtn/ToExamine',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise

# 会员积分兑换活动——送实物
class Test_exchange_activity_gift():
    # add
    def test_add_exchange_activity(self,manage,session,now_time,vip_data,vipcard_data,gift_data,activity_data_random):
        data={}
        try:
            data['t[BllNo]'] = ''
            data['t[OrgID]'] = vipcard_data['OrgID']
            data['t[Name]'] = activity_data_random['Name']
            data['t[BllType]'] = '0'
            data['t[ProfitTyp]'] = '1'
            data['t[ShopType]'] = '2'
            data['t[VipTpID]'] = vip_data['VipTpID']
            data['t[StDt]'] = now_time['StDt']
            data['t[EnDt]'] = now_time['EnDt']
            data['t[CshTm]'] = '4'
            data['t[Brf]'] = 'apitest'
            data['list[0][Lvl]'] = '1'
            data['list[0][StepVal]'] = '0'
            data['list[0][Bestowal]'] = gift_data['GdsID']
            data['list[0][Name]'] = gift_data['Name']
            data['list[0][Amt]'] = activity_data_random['Amt']
            data['list[0][ChangeMoney]'] = '0'
            data['t[EnDt]'] = now_time['EnDt']
            data['list[0][Brf]'] = 'apitest'
            response=session.post(url=manage['url'] % '/IntgCsh/Add',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise
    # select page
    def test_get_exchange_activity_page(self,manage,session):
        data={'dtGridPager':'{"errorMsg":"","isExport":false,"pageSize":10,"startRecord":0,"nowPage":1,"recordCount":-1,"pageCount":-1,"parameters":{},"fastQueryParameters":{},"advanceQueryConditions":[],"advanceQuerySorts":[]}'}
        try:
            response=session.post(url=manage['url'] % '/IntgCsh/QueryList',data=data)
            response_json = comm_way.response_dispose(response.json())
            assert response.status_code == 200
            assert response_json['Issuccess'] == True   
            if response_json['Exhibitdatas']:
                comm_way.sql_insert('exchange_activity_data_a',response_json['Exhibitdatas'][0])
                for i in response_json['Exhibitdatas']:
                    print(i)
            else:
                print('没有兑换活动')
        except:
            raise
    # select
    def test_get_exchange_activity(self,manage,session,exchange_activity_data_a):
        data={}
        try:
            data['BllNo'] = exchange_activity_data_a['BllNo']
            response=session.post(url=manage['url'] % '/IntgCsh/GetSingleData',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json)
            assert response.status_code == 200
            assert response_json['Success'] == True   
            if response_json['Data']['List']:
                comm_way.sql_insert('exchange_activity_data_b',response_json['Data']['List'][0])
                for i in response_json['Data']['List']:
                    print(i)
            else:
                print('没有兑换活动')
        except:
            raise
    # check
    def test_check_exchange_activity(self,manage,session,exchange_activity_data_a):
        data={}
        try:
            data['billNos'] = exchange_activity_data_a['BllNo']
            data['examineStt'] = '50'
            response=session.post(url=manage['url'] % '/Basics/IntgCsh/ToExamine',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise

# 会员账户
class Test_member_account():
    # select
    def test_vip_account(self,manage,session,vipcard_data):
        data={'dtGridPager':'{"errorMsg":"","isExport":false,"pageSize":10,"startRecord":0,"nowPage":1,"recordCount":1,"pageCount":1,"parameters":{"NickName":"","Tel":"","Name":"","VipID":"#vipid"},"fastQueryParameters":{},"advanceQueryConditions":[],"advanceQuerySorts":[]}'}
        try:
            data['dtGridPager']=data['dtGridPager'].replace('#vipid',vipcard_data['VipID'])
            response=session.post(url=manage['url'] % '/Basics/CpnVip/SlecetCpnVippagingInfo',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json)
            assert response.status_code == 200
            assert response_json['Issuccess'] == True 
            if response_json['Exhibitdatas']:
                comm_way.sql_insert('member_account',response_json['Exhibitdatas'][0])  
                for i in response_json['Exhibitdatas']:
                    print(i)
            else:
                print('没有会员账户')
            
        except:
            raise

# 积分兑换
class Test_integral_exchange_gift():
    # add
    def test_add_integral_exchange(self,manage,session,vipcard_data,member_account,exchange_activity_data_b):
        data={} 
        try:
            data['t[OrgID]'] = vipcard_data['OrgID']
            data['t[VipID]'] = vipcard_data['VipID']
            data['t[GstID]'] = vipcard_data['GstID']
            data['t[CrdNo]'] = vipcard_data['CrdNo']
            data['t[CrdID]'] = vipcard_data['CrdID']
            data['t[VipTpID]'] = vipcard_data['VipTpID']
            if member_account['IntgAva']:
                data['t[IntgAva]'] = int(float(member_account['IntgAva']))   #积分余额
            else:
                data['t[IntgAva]'] = 0
            data['t[SumIntg]'] = int(float(exchange_activity_data_b['Amt']))*2   #扣除积分
            data['t[SumTknMoney]'] = '0'
            data['t[SumChgMoney]'] = '0'
            data['t[Brf]'] = 'apitest'
            data['list[0][BllNo]'] = exchange_activity_data_b['BllNo']       #返利活动编号
            data['list[0][Lvl]'] = '1'
            data['list[0][CpnID]'] = exchange_activity_data_b['CpnID']  
            data['list[0][IntgCshBllNo]'] = exchange_activity_data_b['BllNo']    #返利活动编号
            data['list[0][Bestowal]'] = exchange_activity_data_b['Bestowal']     #兑换商品编号
            data['list[0][Name]'] = exchange_activity_data_b['Name']     #兑换实物名称
            data['list[0][Amt]'] = exchange_activity_data_b['Amt'] #活动兑换积分   
            data['list[0][UseIntg]'] = int(float(exchange_activity_data_b['Amt']))*2   #应扣积分
            data['list[0][Qty]'] = '2'  #兑换数量
            data['list[0][TknID]'] = ''
            data['list[0][TknAmt]'] = '0'
            data['list[0][StepVal]'] = '0'
            data['list[0][ProfitPer]'] = '0'
            data['list[0][TStDt]'] = ''
            data['list[0][TEdDt]'] = ''
            data['list[0][UseOrgID]'] = ''
            data['list[0][ChangeMoney]'] = '0'
            data['list[0][IntgCshLvl]'] = '1'
            data['list[0][BillType]'] = '1'
            data['list[0][ChgMoney]'] = '0'
            data['list[0][CanlFlg]'] = 'F'
            data['list[0][Brf]'] = 'apitest'
            data['list[0][Rdx]'] = '1'
            print(data)
            response=session.post(url=manage['url'] % '/Card/IntgExChange/Add',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise
    # select page
    def test_get_integral_exchange_page(self,manage,session):
        data={'dtGridPager':'{"errorMsg":"","isExport":false,"pageSize":10,"startRecord":0,"nowPage":1,"recordCount":184,"pageCount":19,"parameters":{"BllNo":"","Stt":""},"fastQueryParameters":{},"advanceQueryConditions":[],"advanceQuerySorts":[]}'}
        try:
            response=session.post(url=manage['url'] % '/IntgExChange/QueryList',data=data)
            response_json = comm_way.response_dispose(response.json())
            assert response.status_code == 200
            assert response_json['Issuccess'] == True   
            if response_json['Exhibitdatas']:
                comm_way.sql_insert('integral_exchange_data_a',response_json['Exhibitdatas'][0])
                for i in response_json['Exhibitdatas']:
                    print(i)
            else:
                print('没有兑换单')
        except:
            raise
    # select
    def test_get_integral_exchange(self,manage,session,integral_exchange_data_a):
        data={}
        try:
            data['bllNo'] = integral_exchange_data_a['BllNo']
            response=session.post(url=manage['url'] % '/IntgExChange/GetSingleData',data=data)
            response_json = comm_way.response_dispose(response.json())
            assert response.status_code == 200
            assert response_json['Success'] == True   
            if response_json['Data']['List']:
                comm_way.sql_insert('integral_exchange_data_b',response_json['Data']['List'][0])
                for i in response_json['Data']['List']:
                    print(i)
            else:
                print('没有兑换单')
        except:
            raise
    # check
    def test_check_integral_exchange(self,manage,session,integral_exchange_data_a):
        data={}
        try:
            data['billNos'] = integral_exchange_data_a['BllNo']
            data['examineStt'] = '50'
            response=session.post(url=manage['url'] % '/IntgExChange/ToExamine',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise

# 积分统计
class Test_integral_sum():
    # select
    def test_get_integral_sum(self,manage,session,vip_data):
        data={'dtGridPager':'{"errorMsg":"","isExport":false,"pageSize":20,"startRecord":0,"nowPage":1,"recordCount":1,"pageCount":1,"parameters":{"Tel":"#Tel","Name":"","CrdNo":"","VipTpID":""},"fastQueryParameters":{},"advanceQueryConditions":[],"advanceQuerySorts":[]}'}
        try:
            data['dtGridPager']=data['dtGridPager'].replace('#Tel',vip_data['Tel'])
            response=session.post(url=manage['url'] % '/Basics/Intg/SlecetIntgpagingInfo',data=data)
            response_json = comm_way.response_dispose(response.json())
            assert response.status_code == 200
            assert response_json['Issuccess'] == True   
        except:
            raise

    
# 会员冻结
class Test_member_freeze():
    # add 
    def test_add_member_freeze(self,manage,session,vipcard_data):
        data={}
        try:
            data['vipID'] = vipcard_data['VipID']
            data['stt'] = '1'
            response=session.post(url=manage['url'] % '/Basics/CpnVip/BatchFrozenCpnVip',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise
    # select page
    def test_get_member_freeze_page(self,manage,session,vipcard_data):
        data={'dtGridPager':'{"errorMsg":"","isExport":false,"pageSize":10,"startRecord":0,"nowPage":1,"recordCount":18,"pageCount":2,"parameters":{"BllNo":"","Stt":"","VipTpID":""},"fastQueryParameters":{},"advanceQueryConditions":[],"advanceQuerySorts":[]}'}
        try:
            response=session.post(url=manage['url'] % '/Basics/VipStt/QueryList',data=data)
            response_json = comm_way.response_dispose(response.json())
            assert response.status_code == 200
            assert response_json['Issuccess'] == True   
            if response_json['Exhibitdatas']:
                comm_way.sql_insert('member_freeze_data',response_json['Exhibitdatas'][0])
                for i in response_json['Exhibitdatas']:
                    print(i)
            else:
                print('没有会员维护单')
        except:
            raise
        
    # check
    def test_check_member_freeze(self,manage,session,member_freeze_data):
        data={}
        try:
            data['billNo'] = member_freeze_data['BllNo']
            data['examineStt'] = '50'
            response=session.post(url=manage['url'] % '/Basics/VipStt/ToExamine',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise

# 会员解冻
class Test_member_unfreeze():
    # add
    def test_add_member_unfreeze(self,manage,session,vipcard_data):
        data={}
        try:
            data['vipID'] = vipcard_data['VipID']
            data['stt'] = '0'
            response=session.post(url=manage['url'] % '/Basics/CpnVip/BatchFrozenCpnVip',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise
    # select page
    def test_get_member_unfreeze_page(self,manage,session,vipcard_data):
        data={'dtGridPager':'{"errorMsg":"","isExport":false,"pageSize":10,"startRecord":0,"nowPage":1,"recordCount":18,"pageCount":2,"parameters":{"BllNo":"","Stt":"","VipTpID":""},"fastQueryParameters":{},"advanceQueryConditions":[],"advanceQuerySorts":[]}'}
        try:
            response=session.post(url=manage['url'] % '/Basics/VipStt/QueryList',data=data)
            response_json = comm_way.response_dispose(response.json())
            assert response.status_code == 200
            assert response_json['Issuccess'] == True   
            if response_json['Exhibitdatas']:
                comm_way.sql_insert('member_freeze_data',response_json['Exhibitdatas'][0])
                for i in response_json['Exhibitdatas']:
                    print(i)
            else:
                print('没有会员维护单')
        except:
            raise
    # 审核
    def test_check_member_unfreeze(self,manage,session,member_freeze_data):
        data={}
        try:
            data['billNo'] = member_freeze_data['BllNo']
            data['examineStt'] = '50'
            response=session.post(url=manage['url'] % '/Basics/VipStt/ToExamine',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise


# 终止活动
class Test_stop_activity():
    # 终止注册送实物
    def test_stop_register_activity_gift(self,manage,session,register_activity_gift_data):
        data={}
        try:
            data['t[FlwStt]'] = '-1'
            data['t[BllNo]'] = register_activity_gift_data['BllNo']
            response=session.post(url=manage['url'] % '/Basics/VipPrmt/FlwUpdate',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise
    # 终止注册送积分
    def test_stop_register_activity_integral(self,manage,session,register_activity_integral_data):
        data={}
        try:
            data['t[FlwStt]'] = '-1'
            data['t[BllNo]'] = register_activity_integral_data['BllNo']
            response=session.post(url=manage['url'] % '/Basics/VipPrmt/FlwUpdate',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise
    # 终止储值送实物
    def test_stop_top_up_activity_gift(self,manage,session,top_up_activity_gift_data):
        data={}
        try:
            data['t[FlwStt]'] = '-1'
            data['t[BllNo]'] = top_up_activity_gift_data['BllNo']
            response=session.post(url=manage['url'] % '/Storvl/RchgPrmt/FlwUpdate',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise
    # 终止储值送积分
    def test_stop_top_up_activity_integral(self,manage,session,top_up_activity_integral_data):
        data={}
        try:
            data['t[FlwStt]'] = '-1'
            data['t[BllNo]'] = top_up_activity_integral_data['BllNo']
            response=session.post(url=manage['url'] % '/Storvl/RchgPrmt/FlwUpdate',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise
    # 终止积分兑换
    def test_stop_exchange_activity(self,manage,session,exchange_activity_data_a):
        data={}
        try:
            data['t[FlwStt]'] = '-1'
            data['t[BllNo]'] = exchange_activity_data_a['BllNo']
            response=session.post(url=manage['url'] % '/Basics/IntgCsh/FlwUpdate',data=data)
            response_json = comm_way.response_dispose(response.json())
            print(response_json['Message'])
            assert response.status_code == 200
            assert response_json['Success'] == True   
        except:
            raise
    # 

# 收银机验证
# def test_cash_register(session,cash_register_header):
#     json={
#             "hdr": "",  #请求头
#             "card": "", #卡信息
#             "account": "",  #卡账户
#             "integralInfo": "", #积分账户
#             "SysTyp": "mis"
#         }
#     try:
#             json['hdr'] = comm_way.dicttoxml(cash_register_header)
#             response = session.post("https://hugiyqq1ji.execute-api.cn-northwest-1.amazonaws.com.cn/WucrmValid/wucrm",json=json)
#             print(response)
#             # response_json = comm_way.response_dispose(response.json())
#             # print(response_json['Message'])
#             assert response.status_code == 200
#             # assert response_json['Success'] == True   
#     except:
#         raise

def test_1(member_account):
    x=member_account
    print(x['IntgAva'])
    # x['IntgAva']=2323.1
    if x['IntgAva']:
        z=(float(x['IntgAva']))
        print(z)
    else:
        z=0.0
        print(z)
