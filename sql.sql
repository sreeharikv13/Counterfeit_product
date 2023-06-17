/*
SQLyog Community Edition- MySQL GUI v8.03 
MySQL - 5.6.12-log : Database - counterfeit
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`counterfeit` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `counterfeit`;

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `complaint_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `complaint` varchar(100) DEFAULT NULL,
  `complaint_date` int(11) DEFAULT NULL,
  `reply` varchar(100) DEFAULT NULL,
  `replydate` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`complaint_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

insert  into `complaint`(`complaint_id`,`user_id`,`complaint`,`complaint_date`,`reply`,`replydate`) values (1,1,'duplicate',NULL,'bvvh','20230126'),(2,8,'aaa',20230317,'pending','0'),(3,8,'hhu',20230317,'pending','0'),(4,8,'uu',20230317,'pending','pending');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `loginid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL,
  `usertype` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`loginid`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`loginid`,`username`,`password`,`usertype`) values (1,'admin','admin','admin'),(2,'m','m','manufacture'),(3,'ssreeharikv@gmail.com','admin13','manufacture'),(4,'ssreeharikv@gmail.com','admin13','manufacture'),(5,'stb@gmail.com','admin14','manufacture'),(6,'hr@gmail.com','admin15','manufacture'),(7,'aa@gmail.com','123','user'),(8,'vishnu07@gmail.com','cr7','user');

/*Table structure for table `manufacture` */

DROP TABLE IF EXISTS `manufacture`;

CREATE TABLE `manufacture` (
  `manufacture_loginid` int(11) NOT NULL AUTO_INCREMENT,
  `manufacture_date` int(11) DEFAULT NULL,
  `manufacture_image` varchar(100) DEFAULT NULL,
  `place` varchar(30) DEFAULT NULL,
  `post` int(11) DEFAULT NULL,
  `pin` int(11) DEFAULT NULL,
  `district` varchar(30) DEFAULT NULL,
  `license_no` int(11) DEFAULT NULL,
  `email` varchar(20) DEFAULT NULL,
  `phoneno` int(11) DEFAULT NULL,
  `name` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`manufacture_loginid`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

/*Data for the table `manufacture` */

insert  into `manufacture`(`manufacture_loginid`,`manufacture_date`,`manufacture_image`,`place`,`post`,`pin`,`district`,`license_no`,`email`,`phoneno`,`name`) values (2,2022,'b','m',0,9,'f',56,'m@gmail.com',7777,'nn'),(4,2022,'/static/manufacture_img/20221215_153209.jpg','kannur',0,670001,'kannur',0,'ssreeharikv@gmail.co',2147483647,'profx'),(5,2000,'/static/manufacture_img/20221215_153957.jpg','calicut',0,630001,'calicut',0,'stb@gmail.com',2147483647,'starbucks'),(6,2002,'/static/manufacture_img/20221215_154531.jpg','kochi',0,270301,'eranakulam',0,'hr@gmail.com',2147483647,'horlicks');

/*Table structure for table `product` */

DROP TABLE IF EXISTS `product`;

CREATE TABLE `product` (
  `product_id` int(30) NOT NULL AUTO_INCREMENT,
  `product_name` varchar(50) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `quantity` double DEFAULT NULL,
  `manufacture_rate` int(20) DEFAULT NULL,
  `manufacture_date` int(10) DEFAULT NULL,
  `expire_date` int(10) DEFAULT NULL,
  `manufacture_id` int(50) DEFAULT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `product` */

insert  into `product`(`product_id`,`product_name`,`image`,`quantity`,`manufacture_rate`,`manufacture_date`,`expire_date`,`manufacture_id`) values (1,'lays','/static/manufacture_img/20221230_212922.jpg',10,5,31,31,NULL),(2,'dairymilk','/static/manufacture_img/20221230_213602.jpg',10,50,1,31,3);

/*Table structure for table `spam` */

DROP TABLE IF EXISTS `spam`;

CREATE TABLE `spam` (
  `spam_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `spam_details` varchar(100) DEFAULT NULL,
  `spam_images` varchar(100) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  PRIMARY KEY (`spam_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `spam` */

insert  into `spam`(`spam_id`,`user_id`,`spam_details`,`spam_images`,`date`) values (1,1,'dhgdggcg',NULL,8766);

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  `email` varchar(20) DEFAULT NULL,
  `phone_no` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`user_id`,`name`,`email`,`phone_no`) values (1,'hh','h@gmail.com',9876),(7,'aa','aa@gmail.com',2147483647),(8,'vishnu ','vishnu07@gmail.com',2147483647);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
