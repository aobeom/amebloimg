# amebloimg

## 简介
通过ameblo博主的首页获取该博主的文章图片。

## 使用方法
输入ameblo博主的主页地址。

## 举例
```shell
$ python amebloimg.py
Blog Index Url: http://ameblo.jp/ayaka-miyoshi/
Date(YYYYMM-YYYYMM): 201506-201601
```
Date严格按照以下四种格式使用：

+ -YYYYMM (-201706)
+ YYYYMM- (201606-)
+ YYYYMM-YYYYMM (201606-201706)
+ YYYYMM (201706)

第一种格式：慎重使用，由于没有统一获取博主起始时间的方法，故开始时间设定为200501（相当于201501-此刻），只适用于更新少的博主  
第二种格式：设定时间到此刻时间   
第三种格式：推荐使用，一个时间范围，可以逐步向前分段使用  
第四种格式：只适用一个月
