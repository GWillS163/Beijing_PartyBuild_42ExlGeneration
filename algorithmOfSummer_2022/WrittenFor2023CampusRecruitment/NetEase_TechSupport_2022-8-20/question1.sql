/*
 * # Author : Github: @GWillS163
 * # Time: $(Date)
 */


CREATE TABLE `courselive` (
        `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
        `ts` Date,
        `client` varchar(255) NOT NULL COMMENT '客户端',
        `userId` varchar(255) NOT NULL COMMENT '用户ID',
        `requl` varchar(255) DEFAULT NULL COMMENT 'url',
        `liveid` varchar(255) DEFAULT NULL COMMENT '直播间id',



        PRIMARY KEY (`id`)
        );

INSERT INTO courselive
VALUES('1','2018-02-01','web','urs-awsxd','https://ke.youdao.com/','abcde');
INSERT INTO courselive
VALUES('2','2018-02-02','iphone','urs-awsxd','https://ke.youdao.com/','abcde');
INSERT INTO courselive
VALUES('3','2018-02-03','Android','urs-tdggh','https://live.youdao.com/','edfgr');
INSERT INTO courselive
VALUES('4','2018-02-04','web','urs-awsxd','https://ke.youdao.com/','rgtgv');
INSERT INTO courselive
VALUES('5','2018-02-05','iphone','urs-erygh','https://ke.youdao.com/','jgfgf');



-- query all user client == iphone, show date and userId, ascending order by date
SELECT ts,userid FROM courselive WHERE client = 'iphone' ORDER BY ts ASC;





