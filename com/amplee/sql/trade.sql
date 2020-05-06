/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50557
Source Host           : localhost:3306
Source Database       : trade

Target Server Type    : MYSQL
Target Server Version : 50557
File Encoding         : 65001

Date: 2020-05-06 17:15:33
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for tb_buy_record
-- ----------------------------
DROP TABLE IF EXISTS `tb_buy_record`;
CREATE TABLE `tb_buy_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(20) DEFAULT NULL,
  `price` float(11,5) DEFAULT NULL COMMENT '当前的价格',
  `ori_price` float(11,5) DEFAULT NULL COMMENT '原始买入时的价格',
  `buy_index` bigint(20) DEFAULT NULL COMMENT '买入时候的时间戳',
  `amount` float(11,5) DEFAULT NULL COMMENT '数量',
  `order_id` varchar(50) DEFAULT NULL,
  `min_income` float(11,5) DEFAULT NULL COMMENT '最低收入',
  `last_price` float(11,5) DEFAULT NULL COMMENT '最近一次买的价格',
  `status` tinyint(2) DEFAULT '0' COMMENT '0 正常状态 1 被止损了  2 进入买交易队列了  3进入卖交易队列  4进入挂单',
  `create_time` datetime DEFAULT NULL,
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `order_id_idx` (`order_id`),
  KEY `symbol_idx` (`symbol`)
) ENGINE=InnoDB AUTO_INCREMENT=170 DEFAULT CHARSET=utf8 COMMENT='记录每次买';

-- ----------------------------
-- Table structure for tb_buy_sell_history_record
-- ----------------------------
DROP TABLE IF EXISTS `tb_buy_sell_history_record`;
CREATE TABLE `tb_buy_sell_history_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(20) DEFAULT NULL,
  `type` tinyint(2) DEFAULT NULL COMMENT '0卖出  1买入',
  `buy_price` float(11,5) DEFAULT NULL COMMENT '买入时的价格',
  `sell_price` float(11,5) DEFAULT NULL COMMENT '卖出的价格',
  `buy_order_id` varchar(50) DEFAULT NULL COMMENT '买入的订单id',
  `sell_order_id` varchar(50) DEFAULT NULL COMMENT '卖出的订单',
  `amount` float(11,5) DEFAULT NULL COMMENT '数量',
  `oper_index` bigint(20) DEFAULT NULL COMMENT '交易时的时间戳',
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `s_ct_idx` (`symbol`,`create_time`)
) ENGINE=InnoDB AUTO_INCREMENT=294 DEFAULT CHARSET=utf8 COMMENT='每次正常买卖的记录';

-- ----------------------------
-- Table structure for tb_jump_queue_history_record
-- ----------------------------
DROP TABLE IF EXISTS `tb_jump_queue_history_record`;
CREATE TABLE `tb_jump_queue_history_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(20) DEFAULT NULL,
  `type` tinyint(2) DEFAULT NULL COMMENT '为单数即为买  1 正常买  2 正常卖  3 止损后买',
  `order_id` varchar(50) DEFAULT NULL,
  `low_price` float(11,5) DEFAULT NULL COMMENT '价格区间低',
  `high_price` float(11,5) DEFAULT NULL COMMENT '价格区间高',
  `jump_price` float(11,5) DEFAULT NULL COMMENT '触发跳跃的最低价格',
  `jump_count` int(11) DEFAULT NULL COMMENT '跳跃次数',
  `create_time` datetime DEFAULT NULL,
  `ori_price` float(11,5) DEFAULT NULL COMMENT '第一次加入跳跃队列时的价格',
  `oper_price` float(11,5) DEFAULT NULL COMMENT '最后执行操作的价格',
  `amount` float(11,5) DEFAULT NULL COMMENT '数量',
  PRIMARY KEY (`id`),
  KEY `symbol_idx` (`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='价格跳跃历史表';

-- ----------------------------
-- Table structure for tb_jump_queue_record
-- ----------------------------
DROP TABLE IF EXISTS `tb_jump_queue_record`;
CREATE TABLE `tb_jump_queue_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(20) DEFAULT NULL,
  `type` tinyint(2) DEFAULT NULL COMMENT '为单数即为买  1 正常买  2 正常卖  3 止损后买',
  `order_id` varchar(50) DEFAULT NULL,
  `low_price` float(11,5) DEFAULT NULL COMMENT '价格区间低',
  `high_price` float(11,5) DEFAULT NULL COMMENT '价格区间高',
  `jump_price` float(11,5) DEFAULT NULL COMMENT '触发跳跃的最低价格',
  `jump_count` int(11) DEFAULT NULL COMMENT '跳跃次数',
  `create_time` datetime DEFAULT NULL,
  `ori_price` float(11,5) DEFAULT NULL COMMENT '第一次加入跳跃队列时的价格',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `symbol_idx` (`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='价格跳跃表';

-- ----------------------------
-- Table structure for tb_sell_order_record
-- ----------------------------
DROP TABLE IF EXISTS `tb_sell_order_record`;
CREATE TABLE `tb_sell_order_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(20) DEFAULT NULL,
  `buy_price` float(11,5) DEFAULT NULL COMMENT '买入时的价格',
  `sell_price` float(11,5) DEFAULT NULL COMMENT '卖出的价格',
  `buy_index` bigint(20) DEFAULT NULL COMMENT '买入时的时间戳秒',
  `sell_index` bigint(20) DEFAULT NULL COMMENT '卖出时的时间戳秒',
  `buy_orderId` varchar(50) DEFAULT NULL COMMENT '买的订单id',
  `sell_orderId` varchar(50) DEFAULT NULL COMMENT '卖的订单id',
  `amount` float(11,5) DEFAULT NULL COMMENT '数量',
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `s_soi_idx` (`symbol`,`sell_orderId`),
  KEY `s_boi` (`symbol`,`buy_orderId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='提前卖的记录';

-- ----------------------------
-- Table structure for tb_stop_loss_history_record
-- ----------------------------
DROP TABLE IF EXISTS `tb_stop_loss_history_record`;
CREATE TABLE `tb_stop_loss_history_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` tinyint(2) DEFAULT NULL COMMENT '0卖出  1买入',
  `symbol` varchar(20) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `oper_price` float(11,5) DEFAULT NULL COMMENT '本次操作的价格',
  `last_price` float(11,5) DEFAULT NULL COMMENT '上一次操作的价格',
  `amount` float(11,5) DEFAULT NULL COMMENT '数量',
  `ori_order_id` varchar(50) DEFAULT NULL COMMENT '原始订单id',
  `order_id` varchar(50) DEFAULT NULL COMMENT '本次止损的订单id',
  PRIMARY KEY (`id`),
  KEY `symbol_idx` (`symbol`)
) ENGINE=InnoDB AUTO_INCREMENT=260 DEFAULT CHARSET=utf8 COMMENT='止损的历史记录';

-- ----------------------------
-- Table structure for tb_stop_loss_record
-- ----------------------------
DROP TABLE IF EXISTS `tb_stop_loss_record`;
CREATE TABLE `tb_stop_loss_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(20) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `sell_price` float(11,5) DEFAULT NULL COMMENT '止损卖出的价格',
  `ori_price` float(11,5) DEFAULT NULL COMMENT '原始买入的价格',
  `ori_amount` float(11,5) DEFAULT NULL COMMENT '原始数量',
  `ori_order_id` varchar(50) DEFAULT NULL COMMENT '原始订单id',
  `order_id` varchar(50) DEFAULT NULL COMMENT '本次止损的订单id',
  `status` tinyint(2) DEFAULT '0' COMMENT '0默认状态  1 进入交易队列',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `symbol_idx` (`symbol`)
) ENGINE=InnoDB AUTO_INCREMENT=134 DEFAULT CHARSET=utf8 COMMENT='止损卖出的记录';

-- ----------------------------
-- Table structure for tb_transaction_config
-- ----------------------------
DROP TABLE IF EXISTS `tb_transaction_config`;
CREATE TABLE `tb_transaction_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(20) DEFAULT NULL COMMENT '交易对 eosusdt',
  `every_expense` float(11,3) DEFAULT '10.000' COMMENT '每次交易的金额',
  `trade_gap` float(11,3) DEFAULT '0.030' COMMENT '与以往的交易间隔',
  `min_income` float(11,3) DEFAULT '0.035' COMMENT '最低收益率',
  `period` varchar(20) DEFAULT '1min' COMMENT 'K线周期',
  `precision` int(5) DEFAULT '2' COMMENT '小数点精度',
  `stopLoss` float(11,3) DEFAULT '0.150' COMMENT '止损点',
  `status` tinyint(2) DEFAULT '1' COMMENT '1 正常 0失效',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COMMENT='交易对配置';
