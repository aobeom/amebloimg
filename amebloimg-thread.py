# -*- coding: UTF-8 -*-
# @author AoBeom
# @create date 2017-12-25 05:32:54
# @modify date 2017-12-25 05:32:54
# @desc [ameblog images downloader]
import argparse
import datetime
import json
import os
import re
import sys
import time
from multiprocessing.dummy import Pool as ThreadPool

import requests


class ameblo(object):
    def __init__(self, url):
        self.TIME = time.strftime(
            '%Y%m%d%H%M%S', time.localtime(time.time()))
        self.url = url
        self.owner = self.url.split("/")[3]
        self.dirs = self.owner + "_" + self.TIME
        self.logs = "Error_" + self.TIME + ".log"
        self.log404 = "log404_" + self.TIME + ".log"
        self.nglog = "invalid_" + self.TIME + ".log"
        self.retry = "retry_" + self.TIME + ".log"

    # requests统一处理
    def __requests(self, url, headers=None, params=None, timeout=30):
        if headers:
            headers = headers
        else:
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"}
        if params is None:
            try:
                response = requests.get(url, headers=headers, timeout=timeout)
            except Exception as e:
                raise e
        else:
            try:
                response = requests.get(
                    url, headers=headers, params=params, timeout=timeout)
            except Exception as e:
                raise e
        return response

    # 错误提示统一处理
    def __amebloInfos(self, value):
        infos = {
            "format_all": "Please use this date format.\r\n[YYYYMM-YYYYMM],[-YYYYMM],[YYYYMM-]",
            "format_len": "Date Format Error.",
            "compare": "The end time must be greater than the start time.",
            "url_invaild": "Invaild para.",
            "url_link": "Link error",
            "building": "Beginning in 2005"
        }
        print infos.get(value, "infomations")
        raw_input("Press Enter to exit.")
        sys.exit()

    # 日期格式检查 amebloEntryList
    def __isValidDate(self, date):
        try:
            # 月份必须是两位数
            if len(date) == 6:
                time.strptime(date, "%Y%m")
                return True
        except BaseException:
            return False

    # 年月拆分 amebloEntryList
    def __dateCut(self, date):
        year = int(date[0:4])
        month = int(date[4:])
        return year, month

    # 输入地址检查
    def __urlCheck(self):
        url = self.url
        # 匹配http和https
        rule = "http[s]?://ameblo.jp.*"
        if len(re.findall(rule, url)):
            if url.endswith("/"):
                url = url.strip("/")
            else:
                url = url
        else:
            self.__amebloInfos("url_invaild")
        return url

    # 相册url拼接 amebloEntryList
    def __amebloJoin(self, *args):
        para = args
        date = ""
        para_len = len(para)
        if para_len == 2:
            date = "/imagelist-" + \
                str(para[0]) + str(para[1]).zfill(2) + ".html"
        elif para_len == 1:
            date = "/imagelist-" + str(para[0]) + ".html"
        else:
            self.__amebloInfos("url_link")
        return date

    # 相册url生成器
    def amebloEntryMain(self, dates):
        newDates = []
        # 判断时间范围
        if dates:
            # 是否按 - 分隔的时间范围
            if "-" in dates:
                # 分离起止时间
                sta = dates.split("-")[0]
                end = dates.split("-")[-1]
                if end != "" and sta > end:
                    self.__amebloInfos("compare")
                else:
                    # 起止时间都存在
                    if self.__isValidDate(sta) and self.__isValidDate(end):
                        s_year, s_month = self.__dateCut(sta)
                        e_year, e_month = self.__dateCut(end)
                        # 判断开始时间是否大于ameblo成立时间
                        if s_year > 2004:
                            # 同一年则只填充月份
                            if s_year == e_year:
                                for month in range(s_month, e_month + 1):
                                    newDates.append(
                                        self.__amebloJoin(s_year, month))
                            else:
                                # 填充起止之间的年月
                                for smonth in range(s_month, 13):
                                    newDates.append(
                                        self.__amebloJoin(s_year, smonth))
                                for myear in range(s_year + 1, e_year):
                                    for mmonth in range(1, 13):
                                        newDates.append(
                                            self.__amebloJoin(myear, mmonth))
                                for emonth in range(1, e_month + 1):
                                    newDates.append(
                                        self.__amebloJoin(e_year, emonth))
                            return newDates
                        else:
                            self.__amebloInfos("building")
                    # 只有结束时间
                    elif sta == "" and self.__isValidDate(end):
                        s_year = 2005
                        e_year, e_month = self.__dateCut(end)
                        if s_year == e_year:
                            for month in range(1, e_month + 1):
                                newDates.append(
                                    self.__amebloJoin(s_year, month))
                        else:
                            for myear in range(s_year, e_year):
                                for mmonth in range(1, 13):
                                    newDates.append(
                                        self.__amebloJoin(myear, mmonth))
                            for emonth in range(1, e_month + 1):
                                newDates.append(
                                    self.__amebloJoin(e_year, emonth))
                        return newDates
                    # 只有开始时间
                    elif end == "" and self.__isValidDate(sta):
                        # 结束时间为此刻的年月
                        thisMonth = time.strftime(
                            '%Y%m', time.localtime(time.time()))
                        s_year, s_month = self.__dateCut(sta)
                        e_year, e_month = self.__dateCut(thisMonth)
                        if s_year == e_year:
                            for month in range(s_month, e_month + 1):
                                newDates.append(
                                    self.__amebloJoin(s_year, month))
                        else:
                            for smonth in range(s_month, 13):
                                newDates.append(
                                    self.__amebloJoin(s_year, smonth))
                            for myear in range(s_year + 1, e_year):
                                for mmonth in range(1, 13):
                                    newDates.append(
                                        self.__amebloJoin(myear, mmonth))
                            for emonth in range(1, e_month + 1):
                                newDates.append(
                                    self.__amebloJoin(e_year, emonth))
                        return newDates
                    else:
                        self.__amebloInfos("format_len")
            else:
                # 只有一个月
                if self.__isValidDate(dates):
                    newDates.append(self.__amebloJoin(dates))
                    return newDates
                else:
                    self.__amebloInfos("format_all")
        # 为空则从2005年开始到此刻的年月
        else:
            build = 2005
            thisMonth = time.strftime('%Y%m', time.localtime(time.time()))
            this_year, this_month = self.__dateCut(thisMonth)
            for year in range(build, this_year):
                for month in range(1, 13):
                    newDates.append(self.__amebloJoin(year, month))
            for emonth in range(1, this_month + 1):
                newDates.append(self.__amebloJoin(this_year, emonth))
            return newDates

    # 第一页的entry amebloEntryCode
    def __entryget(self, url):
        url = url
        # 正则获取entry地址
        rule = r'<p class="imgTitle"><a href="(.*?)" class="titLink">'
        response = self.__requests(url)
        imgindex = response.content
        entryurl = re.findall(rule, imgindex, re.S | re.M)
        return entryurl

    # 第二页以后的entry amebloEntryCode
    def __entrynextget(self, entries):
        entrynext = []
        # api接口
        entryapihost = "https://blogimgapi.ameba.jp/image_list/get.jsonp?"
        blogger = self.owner
        rule = r'"success":true'
        entries = entries.split("-")[-1].split(".")[0]
        for page in range(2, 4):
            try:
                # 参数生成
                para = {"ameba_id": blogger, "target_ym": entries,
                        "limit": 18, "page": page, "sp": "false"}
                response = self.__requests(entryapihost, params=para)
                content = response.text
                # 提取entry
                stat = re.findall(rule, content, re.S | re.M)
                if len(stat) == 1:
                    content = content.replace(
                        "Amb.Ameblo.image.Callback(", "").replace(");", "")
                    entrydict = json.loads(content)
                    imglist = entrydict["imgList"]
                    for entry in imglist:
                        entry = entry["entryUrl"].split(
                            "/")[-1].split(".")[0].split("-")[-1]
                        entrynext.append(entry)
            except Exception as e:
                raise e
        return entrynext

    # 获取所有的entry
    def amebloEntryCode(self, entries, thread):
        u = self.__urlCheck()
        entrycode = []
        entries = map(None, entries)
        urlentrynext_new = []
        urlentry_new = []
        urls = [u + t for t in entries]
        # 多线程获取entry
        pool = ThreadPool(thread)
        urlentry = pool.map(self.__entryget, urls)
        urlentrynext = pool.map(self.__entrynextget, entries)
        pool.close()
        pool.join()
        # 解析entry
        for entrynextlist in urlentrynext:
            if entrynextlist:
                for notnull in entrynextlist:
                    urlentrynext_new.append(notnull)
        for entrylist in urlentry:
            for num in entrylist:
                num = num.split("/")[-1].split(".")[0].split("-")[-1]
                urlentry_new.append(num)
        # 所有的entry合并
        entrycode = urlentry_new + urlentrynext_new
        return entrycode

    # 获取所有图片的url amebloImgList
    def __imgurlget(self, entry):
        owner = self.owner
        # 图片接口
        imghost = "http://stat.ameba.jp"
        imgapihost = "https://blogimgapi.ameba.jp/read_ahead/get.jsonp?"
        entry = entry
        imgurllist = []
        # 请求参数
        para = {"ameba_id": owner, "entry_id": entry,
                "old": "true", "sp": "false"}
        rules = r'"success":true'
        try:
            response = self.__requests(imgapihost, params=para)
            content = response.text
            stat = re.findall(rules, content, re.S | re.M)
            if len(stat) != 0:
                content = content.replace(
                    "Amb.Ameblo.image.Callback(", "").replace(");", "")
                imgdict = json.loads(content)
                imglist = imgdict["imgList"]
                for imgurl in imglist:
                    imgurl = imghost + imgurl["imgUrl"]
                    imgurllist.append(imgurl)
        except Exception as e:
            raise e
        return imgurllist

    # 图片url列表
    def amebloImgList(self, entry, thread):
        entry = entry
        imgurllist = []
        pool = ThreadPool(thread)
        imgpool = pool.map(self.__imgurlget, entry)
        pool.close()
        pool.join()
        # 图片真实url列表
        imgurllist = [i for img in imgpool for i in img]
        imgurllist = sorted(set(imgurllist))
        # 早期图片命名规则匹配
        rule = re.compile(r't[0-9]+\_')
        imgurllist = [rule.sub("o", i) for i in imgurllist]
        return imgurllist

    # 下载主函数 amebloImgGet
    def __getcore(self, imgurl):
        i = imgurl
        nglog = self.nglog
        if "user_images" in i:
            namepart = i.split("/")
            filename = namepart[4] + "-" + namepart[5] + "_" + namepart[10]
            dirs = self.dirs
            savepath = os.path.join(dirs, filename)
            logs = self.logs
            if self.owner in i:
                try:
                    f = self.__requests(i, timeout=60)
                    with open(savepath, "wb") as code:
                        for chunk in f.iter_content(chunk_size=1024):
                            code.write(chunk)
                except BaseException:
                    # 下载失败的图片
                    f = open(logs, "ab+")
                    errorurl = i + "\r\n"
                    f.write(errorurl)
                    f.close()
        else:
            # 图片被屏蔽
            NG = open(nglog, "ab+")
            ngcont = i + "\r\n"
            NG.write(ngcont)
            NG.close()

    def amebloImgGet(self, imglist, thread):
        # 创建日志文件
        logs = self.logs
        dirs = self.dirs
        nglog = self.nglog
        log404 = self.log404
        imglist = imglist
        pool = ThreadPool(thread)
        pool.map(self.__getcore, imglist)
        pool.close()
        pool.join()
        # 以下容错措施未做严格测试
        # 如果有下载失败的图片调用__amebloretry函数
        if os.path.exists(logs):
            print ".....Retry the failed file"
            while os.path.getsize(logs):
                self.__amebloretry(dirs, logs)
            os.remove(logs)
            print "Complete."
        else:
            print "Complete."
        # 记录被屏蔽的图片地址
        if os.path.exists(nglog):
            print "Please check " + nglog
        # 记录无效的图片地址
        if os.path.exists(log404):
            print "Last checking..."
            self.__amebloretry(dirs, log404)
            if os.path.getsize(log404):
                print "Please check " + log404

    # url有效性判断 amebloImgGet
    def __url200(self, urls):
        log404 = self.log404
        url = urls
        u_200 = []
        try:
            response = self.__requests(url)
            code = response.status_code
            if code == 200:
                u_200.append(url)
            else:
                f = open(log404, "ab+")
                notfound = url + "\r\n"
                f.write(notfound)
                f.close()
        except Exception as e:
            raise e
        return u_200

    # 重试函数 amebloImgGet
    def __amebloretry(self, dirs, logs):
        dirs = dirs
        logs = logs
        codelist = []
        retrylist = []
        if os.path.exists(dirs):
            # 读取日志内容
            if os.path.getsize(logs):
                logfile = open(logs, "r+")
                loglines = logfile.readlines()
                # 保存此刻的失败链接
                newlines = [line for line in loglines if line != '\r\n']
                # 清空日志用于记录下次的链接
                deltxt = open(logs, "w")
                codelist = [i.strip() for i in newlines]
                # 对图片地址做有效性判断
                pool = ThreadPool(20)
                codes = pool.map(self.__url200, codelist)
                pool.close()
                pool.join()
                # 移除无效的地址再下载
                retrylist = [c for code in codes for c in code]
                print "Retry [{}]".format(len(retrylist))
                pool = ThreadPool(20)
                pool.map(self.__getcore, retrylist)
                pool.close()
                pool.join()
                deltxt.close()


# 参数解析
def opts():
    paras = argparse.ArgumentParser(description="Download Ameblo Images")
    paras.add_argument('-o', dest='output',
                       action="store_true", default=False, help="save urls")
    args = paras.parse_args()
    return args


def main():
    para = opts()
    url = raw_input("Blog Index Url: ")
    ameba = ameblo(url)
    dirs = ameba.dirs
    t = raw_input("Date[YYYYMM-YYYYMM]: ")
    # 获取时间范围的entry地址
    entries = ameba.amebloEntryMain(t)
    thread = len(entries) * 2
    start = time.time()
    print "[1]Get Entries..."
    # 根据entry地址获取所有entry编号
    entrycode = ameba.amebloEntryCode(entries, thread)
    print "[2]Get Image urls..."
    # 根据编号发起请求获取所有图片地址
    imglist = ameba.amebloImgList(entrycode, thread)
    if not para.output:
        # 创建文件夹并以博主和当前时间命名
        os.mkdir(dirs)
        thread = len(imglist) / 2
        print "[3]Downloading...({})".format(len(imglist))
        # 下载图片
        ameba.amebloImgGet(imglist, thread)
        end = time.time()
        s = int(end - start)
        formats = str(datetime.timedelta(seconds=s))
        print "Lasted %s seconds" % formats
        raw_input("Press Enter to exit.")
    else:
        # 将所有下载地址输出到文本
        T = ameba.TIME
        outlog = "imgurls_" + T + ".log"
        print "[3]Save to {}".format(outlog)
        f = open(outlog, "ab+")
        for i in imglist:
            f.write(i + "\r\n")
        f.close()
        raw_input("Press Enter to exit.")


if __name__ == "__main__":
    main()
