#--coding: GBK --
import os
import sgmllib,urllib,urllib2,random,re
import getpass
import time,copy

class EFormat:
    def __init__(self,num):
        if num==0:
            self.error='帖子提取错误'

      
class Post:
    def __init__(self):
        self.id=''
        self.date=''
        self.subject=''
        self.url=''
    def __eq__(self,data):

        if self.id==data.id and self.date==data.date and self.subject==data.subject and self.url==data.url:
            return True
        else:
            return False

class PostList:
    def __init__(self):
        self.lst=[]
    def append(self,item):
        self.lst.append(item)
    def popfront(self):
        self.lst.reverse()
        rv=self.lst.pop()
        self.lst.reverse()
        return  rv
    def printlist(self):
        for i in range(0,len(self.lst)):
            print '%d:%s    %s    %s'%(i,self.lst[i].id,self.lst[i].date,self.lst[i].subject)
    def __delitem__(self,key):
        del self.lst[key]
    def __getitem__(self,key):
        return self.lst[key]
    def __add__(self,data):
        self.lst=self.lst+data
        return self

            

class LilyBoardParser(sgmllib.SGMLParser):
    def __init__(self):
        sgmllib.SGMLParser.__init__(self)
        self.post=[]
        self.ids=[]
        self.urls=[]
        self.strs=[]

    def start_a(self,attr):
        for an_attr in attr:
            tag,value=an_attr[:2]
            if tag.lower()=='href':
                if value.find('userid=')!=-1:
                    id=value[value.index('userid=')+len('userid='):]
                    self.ids.append(id)
                elif value.find('board=')!=-1:
                    self.urls.append('/'+value)
    def handle_data(self,data):
        data=data.strip()
        if data:
            self.strs.append(data)
##            print data
    def getPost(self):
        #输出的格式：
        #0:置顶/文章号
        #1:id
        #2:date
        #3:title
        #下面的根据是置顶还是非置顶、主题还是非主题有不一样

        #统计帖子总数
        pn=[]
        for i in range(len(self.strs)):
            if self.strs[i].find('○')!=-1 or self.strs[i].find('Re:')!=-1:
                pn.append(i)
        datanum=len(pn)
        urlnum=len(self.urls)
        if datanum!=urlnum:
            raise EFormat(0)
        for i in range(urlnum):
            post=Post()
            post.id=self.strs[pn[i]-2]
            post.url=self.urls[i]
            post.date=self.strs[pn[i]-1]
            post.subject=self.strs[pn[i]]
            self.post.append(post)
        return self.post

class Logger:
    lilyurl='xxx'               # ?????????????????????
    logapp='xxx'                # ?????????????????????
    psturl='xxx'                # ????????????????????
    def __init__(self):
        self.id=''              # id
        self.pw=''              # password
        self.userdir=''         # ????????????????????
        self.header=''          # ????????????????????
    def login(self):
        print '输入账号:'
        self.id=raw_input()     # get id
        self.pw=getpass.getpass("passwd:")
        self.userdir='/vd'+"%05d"%random.randint(0,100000)

        url=Logger.lilyurl+self.userdir+Logger.logapp
        formvalues={'id':self.id,'pw':self.pw,'lasturl':'xxx'}
        para=urllib.urlencode(formvalues)

        req=urllib2.Request(url,para)
        response=urllib2.urlopen(req)
        the_page=response.read()

        cookie="xxx=%d;xxx=%s;xxx=%d;"%(xxx,xxx[1],xxx)
       
        self.header={"cookie":cookie,'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.9) Gecko/20100824 Firefox/3.6.9'}        


class Boardplorer:
    def __init__(self):
        self.postlist=PostList()
        self.account=None
    def reply(self,post,text):
        if not self.account:
            print '现在没有登录，不能回帖'
            return -1
        f=re.compile('/[a-z]+/?')
        articleurl=f.sub('xxx',post.url,1)
        url=Logger.lilyurl+self.account.userdir+articleurl
        print url

        req=urllib2.Request(url,headers=self.account.header)
        response=urllib2.urlopen(req)
        the_page=response.read()
        print the_page

        if the_page.find('name=pid value=')!=-1:
            pid_start=the_page.index('name=pid value=')+len('name=pid value=')+1
            pid=the_page[ pid_start: pid_start+15]
            pid=pid[:pid.index("'")]
            print pid
        if the_page.find('name=reid value=')!=-1:
            reid_start=the_page.index('name=reid value=')+len('name=reid value=')+1
            reid=the_page[ reid_start: reid_start+15]
            reid=reid[:reid.index("'")]
            print reid

        sendurl=f.sub('xxx',post.url,1)
        sendurl=sendurl[:sendurl.index('&')]
        url=Logger.lilyurl+self.account.userdir+sendurl
        print url
        
        title=post.subject.replace('○','Re:')
        postcontest={'title':title,'pid':pid,'reid':reid,'text':text}
        para=urllib.urlencode(postcontest)

        req=urllib2.Request(url,para,self.account.header)
        response=urllib2.urlopen(req)
        the_page=response.read()
        print the_page
        return 0
    def publish(self,title,text):
        pass
    def setaccount(self,account):
        self.account=account
    def visitboard(self,boardname,read_same_theam=1):
        if read_same_theam:
            f='xxx'
        else:
            f='xxx'
        if self.account:
            url=Logger.lilyurl+self.account.userdir+f+'board='+boardname
            req=urllib2.Request(url,headers=self.account.header)
            response=urllib2.urlopen(req)
            del self.postlist[:]
            
            while True:
                contest=response.readline()
                if contest:
                    if contest.find('○')!=-1 or contest.find('Re:')!=-1:
                        parser=LilyBoardParser()
                        parser.feed(contest)
                        postlst=[]
                        try:
                            postlst=parser.getPost()
                        except EFormat,error:
                            print error.error
                            return 
                            
                        self.postlist=self.postlist+postlst
                        #print contest
                    else:
                        continue
                else:
                    break
            return self.postlist
            
        else:
            print '现在是匿名访问'
    def monitorboard(self,boardname):
        oldpstlst=copy.deepcopy(self.visitboard(boardname,1))
        print 'now old post %s'% oldpstlst[-1].subject

        while True:
            time.sleep(1)
            curpstlst=self.visitboard(boardname,1)
            if not(curpstlst[-1] == oldpstlst[-1]):
                self.reply(curpstlst[-1],'飘过~')
                oldpstlst=copy.deepcopy(self.visitboard(boardname,1))
        
        

  
if __name__=='__main__':

    login=Logger()
    login.login()
    plorer=Boardplorer()
    plorer.setaccount(login)
    plorer.monitorboard('xxx')

    
