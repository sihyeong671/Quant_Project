from django.core.exceptions import ValidationError
import pandas as pd

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from django.db.models.query import Prefetch
from django.db import transaction
from django.db.models import Q, F

from api.mixins import ApiAuthMixin, PublicApiMixin

from stockmanage.models import Company, FS_Account, SUB_Account, Daily_Price,\
    CustomFS_Account, CustomSUB_Account, UserCustomBS
from stockmanage.utils import getData, getCaseData
from stockmanage.serializers import UserCustomBSSerializer
from stockmanage.models import *



class CompanyNameApi(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        """
        현재 DB에 저장된 모든 Company의 stock_code와 name을 반환
        """
        company_list = Company.objects.all()
        data_list = []
        
        for com in company_list:
            company = {
                'name': com.corp_name,
                'code': com.stock_code,
            }
            data_list.append(company)
        
        
        data = {
            'company': data_list
        }
        
        return Response(data, status=status.HTTP_200_OK)                      


class AccountSearchApi(PublicApiMixin, APIView):
    def post(self, request, *args, **kwargs):
        """[Search Company Financial State]
        특정 회사의 연도, 분기, 재무제표 종류를 입력받아 검색.
        해당하는 모든 계정명과 서브계정명과 이에 따른 금액을 전달한다.
        
        Args:
            request (
                'code',
                'year',
                'quarter',
                'fs' = 'BS' 로 고정,
                'link',
                'fs',
            ): [key값과 필요한 정보들]
        """
        stock_code = request.data.get('code', '')
        year = request.data.get('year', '')
        year = int(year)
        quarter = request.data.get('quarter', '')
        link = request.data.get('link', '')
        fs = request.data.get('fs')
        
        account_list = FS_Account.objects.\
            prefetch_related('sub_account')\
            .filter(
                Q(fs_div__sj_div=fs) &
                Q(fs_div__lob__lob=link) & 
                Q(fs_div__lob__quarter__qt_name=quarter) & 
                Q(fs_div__lob__quarter__year__bs_year=year) & 
                Q(fs_div__lob__quarter__year__company__stock_code=stock_code)
            )
        
        try:
            unit = account_list[0].fs_div.fs_lob.unit
        except:
            raise NotFound
        
        fs_account_list = []
        
        for ac in account_list:
            sub_account_list = []
            for sub in ac.sub_account.all():
                subaccount = {
                    'name': sub.account_name,
                    'amount': sub.account_amount,
                    'coef': 1,
                }
                sub_account_list.append(subaccount)
            
            fsaccount = {
                'fsname': ac.account_name,
                'amount': ac.account_amount,
                'coef': 1,
                'sub_account': sub_account_list,
            }
            fs_account_list.append(fsaccount)
        
        data = {
            'account': fs_account_list,
            'unit': unit
        }
        
        return Response(data, status=status.HTTP_200_OK)


class CustomBSApi(ApiAuthMixin, APIView):
    def get(self, request, *args, **kwargs):
        """[retreive UserCustomBS]
        현재 유저의 Custom BS중에서 GET 방식으로 요청받은 title값을 통해 
        저장된 Custom BS 정보를 불러옴
        
        Args:
            URL query : ...?title=입력받은title값
        """
        
        custom_title = request.GET["title"]
        user = request.user.profile
        bs_queryset = UserCustomBS.objects\
            .prefetch_related(
                Prefetch('fs_account', queryset=CustomFS_Account.objects.all()),
                Prefetch('fs_account__sub_account', queryset=CustomSUB_Account.objects.all()))\
            .filter(
                Q(user=user) &
                Q(custom_title=custom_title)
            )
        
        serializer = UserCustomBSSerializer(bs_queryset, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """[Create Custom BS]
        계수를 임의로 설정한 BS값을 개인 저장소에 저장한다.
        
        Args:
            request (
                'code',
                'year',
                'title',
                'quarter',
                'fs' = 'BS' 로 고정,
                'link',
                'account',
            ): [key값과 필요한 정보들]

        """
        stock_code = request.data.get('code', '')
        year = request.data.get('year', '')
        custom_title = request.data.get('title', '')
        quarter = request.data.get('quarter', '')
        fs = request.data.get('fs', '')
        link = request.data.get('link', '')
        account_list = request.data.get('account')
        
        profile = request.user.profile
        
        try:
            userbs = UserCustomBS(
                custom_title=custom_title,
                stock_code=stock_code,
                bs_year=year,
                qt_name=quarter,
                lob=link,
                sj_div=fs,
                user=profile
            )
            userbs.save()
            
            for account in account_list:
                fsname = account['fsname']
                amount = account['amount']
                coef = account['coef']
                if coef == '':
                    coef = 1
                
                custom_fsaccount = CustomFS_Account(
                    custom_bs=userbs,
                    account_name=fsname,
                    account_amount=amount,
                    coef=coef
                )
                custom_fsaccount.save()
                
                for sub in account['sub_account']:
                    subname = sub['name']
                    subamount = sub['amount']
                    subcoef = sub['coef']
                    if subcoef == '':
                        subcoef = 1
                    
                    custom_subaccount = CustomSUB_Account(
                        pre_account=custom_fsaccount,
                        account_name=subname,
                        account_amount=subamount,
                        coef=subcoef
                    )
                    custom_subaccount.save()
            
            return Response({
                'message': 'Recieved succesfully',
                }, status=status.HTTP_200_OK)
        except:
            return Response({
                'message': "Recieve failed",
            }, status=status.HTTP_402_PAYMENT_REQUIRED)
        
    def delete(self, request, *args, **kwargs):
        target_title = request.data.get('title', '')
        
        if not target_title:
            return Response({
                'message': "Recieve failed",
            }, status=status.HTTP_402_PAYMENT_REQUIRED)
        
        target = UserCustomBS.objects.filter(
            Q(custom_title=target_title) &
            Q(user=request.user.profile)
        )
        
        if not target.exists():
            return Response({
                "message": "Custom BS not exists"
            }, status=status.HTTP_404_NOT_FOUND)
        
        target.delete()
        
        return Response({
            "message": "Delete succcess"
        }, status=status.HTTP_200_OK)
            

class DailyPriceApi(PublicApiMixin, APIView):
    def post(self, request, *args, **kwargs):
        """
        'code': ['원하는 stock_code 1', '원하는 stock_code 2', ...]
        """
        company_code = request.data.get('code', '')
        
        if not isinstance(company_code, list):
            company_code = list(company_code)
        
        data = {}
        
        for code in company_code:
            company = Company.objects.filter(stock_code=code)
            
            if not company.exists():
                return Response({
                    "message": "Company not exists"
                }, status=status.HTTP_404_NOT_FOUND)
            
            company = company.first()
            
            stocks = Daily_Price.objects.filter(company__id=company.id).order_by('date')
            
            data[company.corp_name] = getData(stocks)
        
        return Response(data, status=status.HTTP_200_OK)
    

class RankApi(PublicApiMixin, APIView):
    def post(self, request, *args, **kwargs):
        """
        case(
            1: 상위
            0: 하위
            
            3: 이상
            2: 이하
        )
        
        rank(
            1: 오름차순
            0: 내림차순
        )
        
        case : [["ROE", 1(상위), 20(float)], ["ROA", 3, 0.5], ]
        rank: [["ROE", 0(오름차순):int], ["PBR", 1(내림차순):int]]
        islink : 연결(True)/일반(False) (기본: 연결, 없으면 일반) -> boolean
        """
        
        try:
            case_list = request.data.get('case', '')
            rank_list = request.data.get('rank', '')
            islink = request.data.get('islink', '')
            print("========")
            print(case_list)
            print(rank_list)
            print(islink)
            print("========")
        except:
            return Response({
                "message": "Payload Error",
            }, status=status.HTTP_402_PAYMENT_REQUIRED)
            
        try:
            # 최근 year 찾기
            condition = Q(exist=1)
            
            recent_lob = FS_LoB.objects.\
                select_related(
                    'quarter',
                    'quarter__year',
                ).\
                filter(condition).\
                order_by('-quarter__year__bs_year').first()
                
            recent_year = recent_lob.quarter.year.bs_year
            
            print("recent year : ", recent_year)
            condition.add(Q(quarter__year__bs_year=recent_year), Q.AND)
            
            recent_lob = FS_LoB.objects.\
                select_related(
                    'quarter',
                    'quarter__year'
                ).\
                filter(
                    condition
                )
            
            # 최근 quarter 찾기
            ## 1분기:11013 2분기:11012 3분기보고서:11014 사업보고서:11011
            recent_quarter = None
            
            for lob in recent_lob[:5]:
                if lob.quarter.qt_name == "11011":
                    recent_quarter = lob.quarter.qt_name
                    break
                elif lob.quarter.qt_name == "11014":
                    recent_quarter = lob.quarter.qt_name
                elif lob.quarter.qt_name == "11012" and \
                    (recent_quarter == None or recent_quarter == "11013"):
                    recent_quarter = lob.quarter.qt_name
                elif lob.quarter.qt_name == "11013" and recent_quarter == None:
                    recent_quarter = lob.quarter.qt_name
            
            print("recent quarter : ", recent_quarter)
            condition.add(Q(quarter__qt_name=recent_quarter), Q.AND)
            
        except:
            return Response({
                "message": "Cannot get recent quarter",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        try:
            # 조건을 통해서 알맞은 df추출
            casedf = pd.DataFrame()
            
            queryset = FS_LoB.objects.select_related(
                'quarter__year__company'
            ).annotate(
                company_name=F("quarter__year__company__corp_name")
            )
            
            if islink:
                condition.add(Q(lob="CFS"), Q.AND)
            else:
                condition.add(Q(lob="OFS"), Q.AND)
            
            if not case_list:
                queryset = queryset.filter(
                    condition
                ).values()
                    
                casedf = pd.DataFrame(list(queryset))
            
            else:
                for case in case_list:
                    ndf = getCaseData(case, condition, queryset)
                    if casedf.empty:
                        casedf = ndf
                    else:
                        pd.concat([casedf, ndf])
                            
                    casedf.drop_duplicates()
            
        except:
            return Response({
                "message": "Cannot get case Dataframe",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        try:
            if casedf.empty:
                return Response({}, status=status.HTTP_200_OK)
                
            nan = -1000000000
            # 추출한 df를 통해서 순위 조건에 맞게 json 만들어서 반환
            column_list = ['company_name']
            for c in case_list:
                if c == []:
                    break
                column_list.append(c[0])
            
            for rank in rank_list:
                casedf.sort_values(by=[rank[0]], ascending=rank[1], inplace=True)
                if rank[0] not in column_list:
                    column_list.append(rank[0])
            
            rankdf = casedf[column_list]
            rankdf["rank"] = list(range(1, len(rankdf)+1))
            rankdf = rankdf.reindex(columns=["rank"] + column_list)
            rankdf = rankdf.fillna(nan)
            
            data = rankdf.apply(lambda row: row.to_dict(), axis=1)
            return Response(data, status=status.HTTP_200_OK)
            
        except:
            return Response({
                "message": "Cannot extract rank dataframe",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class CompanyFSAPi(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        """
        company : 삼성전자 -> str
        
        return 
        {
            
        }
        """