#coding=utf-8
from django.shortcuts import render
from models import *
from django.core.paginator import Paginator
from haystack.generic_views import SearchView

# Create your views here.
def index(request):
    goods_list=[]
    #查询分类对象
    #查询每个分类中最新的四个商品
    #查询每个分类中最火的四个商品
    type_list=TypeInfo.objects.all()
    for t1 in type_list:
        nlist = t1.goodsinfo_set.order_by('-id')[0:4]
        clist = t1.goodsinfo_set.order_by('-gclick')[0:4]
        goods_list.append({'t1':t1, 'nlist':nlist, 'clist':clist})
    context={'title':'首页', 'glist':goods_list, 'cart':'1'}
    return render(request,'df_goods/index.html',context)

def goods_list(request,tid,pindex,orderby):
    try:
        t1 = TypeInfo.objects.get(pk=int(tid))
        new_list = t1.goodsinfo_set.order_by('-id')[0:2]
        #指定排序规则
        orderby_str='-id'
        desc='1'
        if orderby=='2':#根据价格排序
            #指定排序规则，升还是降
            desc=request.GET.get('desc','1')
            if desc=='1':
                orderby_str='-gprice'
            else:
                orderby_str='gprice'
        elif orderby=='3':#根据点击量排序
            orderby_str='-gclick'
        glist = t1.goodsinfo_set.order_by(orderby_str)

        paginator = Paginator(glist,10)
        pindex1 = int(pindex)
        if pindex<1:
            pindex1=1
        elif pindex1>paginator.num_pages:
            pindex1=paginator.num_pages
        page=paginator.page(pindex1)
        context = {'title':'商品列表页', 'cart':'1', 't1':t1, 'new_list':new_list, 'page':page}
        return render(request, 'df_goods/list.html', context)
    except:
        return render(request, '404.html')

def detail(request,id):
    try:
        goods=GoodsInfo.objects.get(pk=int(id))
        goods.gclick+=1
        goods.save()
        new_list=goods.gtype.goodsinfo_set.order_by('-id')[0:2]
        context={'title':'商品详细页', 'cart':'1', 'goods':goods, 'new_list':new_list}
        response=render(request, 'df_goods/detail.html', context)
        #保存最近浏览[1,2,3,4,5]<==>'1,2,3,4,5'  ','.join()  .split()
        #步骤：先读取已经存在的-》进行拼接-》输出
        gids=request.COOKIES.get('goods_ids','').split(',')
        #判断这个编号是否存在，如果存在则删除，然后再加到最前面
        if id in gids:
            gids.remove(id)
        gids.insert(0,id)
        #如果超过5个，则删除最后一个
        if len(gids)>6:
            gids.pop()
        response.set_cookie('goods_ids', ','.join(gids), max_age=60*60*24*7)

        return response
    except:
        return render(request, '404.html')

class MySearchView(SearchView):
    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        context['cart']='1'
        page_range=[]
        page = context.get('page_obj')
        if page.paginator.num_pages<5:
            page_range=page.paginator.page_range
        elif page.number<=2:
            page_range=range(1,6)
        elif page.number>=page.paginator.num_pages-1:#倒数第1，2页
            page_range=range(page.paginator.num_pages-4, page.paginator.num_pages+1)
        else:# 3 4 5 6 7
            page_range=range(page.number-2, page.number+3)
        context['page_range']=page_range
        return context