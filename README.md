Haproxy monitor plugin for Open-Falcon
------------------------------------
------------------------------------
功能支持
------------------
已测试的Haproxy版本1.5.3, 1.5.9.

通过Haproxy的stats socket接口来采集Haproxy基础状态信息,qcur,scur,rate等;

环境需求
-----------------
操作系统: Linux

Python > 2.6

python-toml > 0.9.0

haproxymon部署
--------------------------
1 目录解压到/path/to/haproxymon,配置文件也放到同一路径,记得根据你的实际情况修改配置文件中的参数

2 配置要采集的指标，因haproxy stats文件指标太多，为了方便关注关键指标，脚本提供指标筛选功能；

3 配置crontab, 修改haproxymon_cron文件中haproxymon安装路径; cat haproxymon_cron >> /var/spool/cron/root 

4 在haproxy.py中将debug_level设置：    

      0 表示不输出任何调试内容;
      1 表示输出调用本地falcon代理的返回信息;
      2 表示输出metric信息;
      3 表示输出采集的原始stats内容；

5 endpoint默认是hostname,还可以指定EndpointType来设置为使用本机IP.

6 推荐haproxy的配置文件中使用listen块来配置后端集群：
  本插件通过pxname,svname来识别不同metric的，参考例子如下：
  
     listen  http-in 0.0.0.0:80
        server server1:8000 192.168.0.10:8000 maxconn 32
        server server2:8000 192.168.0.11:8000 maxconn 32
        # other

一般情况几分钟后，可从open-falcon的dashboard中查看haproxy metric

采集的Haproxy指标
----------------------------------------

--------------------------------
| Counters | Type | Notes|
|-----|------|------|
|haproxy_getstats/pxname=your_pxname,svname=FRONTEND    |GAUGE|如果非0则表示无法获取stats socket信息|
|haproxy_status/pxname=your_pxname,svname=FRONTEND      |GAUGE|后端机器状态:down or up|
|haproxy_scur/pxname=your_pxname,svname=FRONTEND        |GAUGE|当前的会话数|
|haproxy_qcur/pxname=your_pxname,svname=FRONTEND        |GAUGE|当前排队的请求数量|
|haproxy_rate/pxname=your_pxname,svname=FRONTEND        |GAUGE|最近一秒的每秒请求会话数|
|haproxy_ereq/pxname=your_pxname,svname=FRONTEND        |GAUGE|客户端请求的错误数|
|haproxy_econ/pxname=your_pxname,svname=FRONTEND        |GAUGE|连接后端时的错误数|
|haproxy_dreq/pxname=your_pxname,svname=FRONTEND        |GAUGE|因安全原因被拒绝的请求数|
|haproxy_qtime/pxname=your_pxname,svname=FRONTEND       |GAUGE|请求的平均排队时间(毫秒)|
|haproxy_ctime/pxname=your_pxname,svname=FRONTEND       |GAUGE|请求的平均连接时间(毫秒)|

建议设置监控告警项
-----------------------------
说明:系统级监控项由falcon agent提供；监控触发条件根据场景自行调整
--------------------------------
| 告警项 | 触发条件 | 备注|
|-----|------|------|
|haproxy_getstats/pxname=your_pxname,svname=FRONTEND    |all(#3)>0|可能是因为stats socket不存在或是无权访问|
|haproxy_status/pxname=your_pxname,svname=FRONTEND      |all(#1)>0|后端机器down会导致负载能力下降，如果所有机器down则无法在提供服务|
|haproxy_scur/pxname=your_pxname,svname=FRONTEND        |all(#3)>=1800|会话数超过阀值会拒绝客户端建立新连接|
|haproxy_qcur/pxname=your_pxname,svname=FRONTEND        |all(#3)>100|超过阀值，说明排队请求多，整体负载压力大|
|haproxy_rate/pxname=your_pxname,svname=FRONTEND        |all(#3)>8000|超过阀值表示haproxy压力过大|
|haproxy_ereq/pxname=your_pxname,svname=FRONTEND        |all(#3)>100|客户端请求错误超过阀值需要检查timeout等于客户端连接有关的配置|
|haproxy_econ/pxname=your_pxname,svname=FRONTEND        |all(#3)>100|若这个值大幅上升可能是后端机器无法响应请求|
|haproxy_dreq/pxname=your_pxname,svname=FRONTEND        |all(#3)>100|tcp模式可能是触发tcp请求内容规则|
|haproxy_qtime/pxname=your_pxname,svname=FRONTEND       |all(#3)>50|超过阀值可能是后端处理能力在下降|
|haproxy_ctime/pxname=your_pxname,svname=FRONTEND       |all(#3)>50|超过阀值可能是haproxy到后端间网络状况变差|


Contributors
------------------------------------------
- 窦锦帅: QQ:33903914; weibo: http://weibo.com/iiask
