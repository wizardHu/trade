/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50557
Source Host           : 127.0.0.1:3306
Source Database       : trade

Target Server Type    : MYSQL
Target Server Version : 50557
File Encoding         : 65001

Date: 2020-08-02 10:20:39
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for tb_buy_record
-- ----------------------------
DROP TABLE IF EXISTS `tb_buy_record`;
CREATE TABLE `tb_buy_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(20) DEFAULT NULL,
  `price` decimal(12,5) DEFAULT NULL COMMENT '当前的价格',
  `ori_price` decimal(12,5) DEFAULT NULL COMMENT '原始买入时的价格',
  `buy_index` bigint(20) DEFAULT NULL COMMENT '买入时候的时间戳',
  `amount` float(11,5) DEFAULT NULL COMMENT '数量',
  `order_id` varchar(50) DEFAULT NULL,
  `min_income` decimal(12,5) DEFAULT NULL COMMENT '最低收入',
  `last_price` decimal(12,5) DEFAULT NULL COMMENT '最近一次买的价格',
  `status` tinyint(2) DEFAULT '0' COMMENT '0 正常状态 1 被止损了  2 进入买交易队列了  3进入卖交易队列  4进入挂单',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id_idx` (`order_id`),
  KEY `symbol_idx` (`symbol`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='记录每次买';

-- ----------------------------
-- Table structure for tb_buy_sell_history_record
-- ----------------------------
DROP TABLE IF EXISTS `tb_buy_sell_history_record`;
CREATE TABLE `tb_buy_sell_history_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(20) DEFAULT NULL,
  `type` tinyint(2) DEFAULT NULL COMMENT '0卖出  1买入',
  `buy_price` decimal(12,5) DEFAULT NULL COMMENT '买入时的价格',
  `sell_price` decimal(12,5) DEFAULT NULL COMMENT '卖出的价格',
  `buy_order_id` varchar(50) DEFAULT NULL COMMENT '买入的订单id',
  `sell_order_id` varchar(50) DEFAULT NULL COMMENT '卖出的订单',
  `amount` decimal(12,5) DEFAULT NULL COMMENT '数量',
  `oper_index` bigint(20) DEFAULT NULL COMMENT '交易时的时间戳',
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `s_ct_idx` (`symbol`,`create_time`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COMMENT='每次正常买卖的记录';

-- ----------------------------
-- Table structure for tb_jump_queue_history_record
-- ----------------------------
DROP TABLE IF EXISTS `tb_jump_queue_history_record`;
CREATE TABLE `tb_jump_queue_history_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(20) DEFAULT NULL,
  `type` tinyint(2) DEFAULT NULL COMMENT '为单数即为买  1 正常买  2 正常卖  3 止损后买',
  `order_id` varchar(50) DEFAULT NULL,
  `low_price` decimal(12,5) DEFAULT NULL COMMENT '价格区间低',
  `high_price` decimal(12,5) DEFAULT NULL COMMENT '价格区间高',
  `jump_price` decimal(12,5) DEFAULT NULL COMMENT '触发跳跃的最低价格',
  `jump_count` int(11) DEFAULT NULL COMMENT '跳跃次数',
  `create_time` datetime DEFAULT NULL,
  `ori_price` decimal(12,5) DEFAULT NULL COMMENT '第一次加入跳跃队列时的价格',
  `oper_price` decimal(12,5) DEFAULT NULL COMMENT '最后执行操作的价格',
  `amount` decimal(12,5) DEFAULT NULL COMMENT '数量',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `symbol_idx` (`symbol`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COMMENT='价格跳跃历史表';

-- ----------------------------
-- Table structure for tb_jump_queue_record
-- ----------------------------
DROP TABLE IF EXISTS `tb_jump_queue_record`;
CREATE TABLE `tb_jump_queue_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(20) DEFAULT NULL,
  `type` tinyint(2) DEFAULT NULL COMMENT '为单数即为买  1 正常买  2 正常卖  3 止损后买',
  `order_id` varchar(50) DEFAULT NULL,
  `low_price` decimal(12,5) DEFAULT NULL COMMENT '价格区间低',
  `high_price` decimal(12,5) DEFAULT NULL COMMENT '价格区间高',
  `jump_price` decimal(12,5) DEFAULT NULL COMMENT '触发跳跃的最低价格',
  `jump_count` int(11) DEFAULT NULL COMMENT '跳跃次数',
  `create_time` datetime DEFAULT NULL,
  `ori_price` decimal(12,5) DEFAULT NULL COMMENT '第一次加入跳跃队列时的价格',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `symbol_idx` (`symbol`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COMMENT='价格跳跃表';

-- ----------------------------
-- Table structure for tb_kline_record
-- ----------------------------
DROP TABLE IF EXISTS `tb_kline_record`;
CREATE TABLE `tb_kline_record` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `open` decimal(12,5) DEFAULT NULL COMMENT '开盘价',
  `close` decimal(12,5) DEFAULT NULL,
  `high` decimal(12,5) DEFAULT NULL COMMENT '最高价',
  `low` decimal(12,5) DEFAULT NULL COMMENT '最低价',
  `amount` decimal(20,5) DEFAULT NULL COMMENT '以基础币种计量的交易量',
  `count` int(11) DEFAULT NULL COMMENT '交易次数',
  `vol` decimal(20,5) DEFAULT NULL COMMENT '以报价币种计量的交易量',
  `line_index` bigint(20) DEFAULT NULL COMMENT '调整为新加坡时间的时间戳，单位秒，并以此作为此K线柱的id',
  `create_time` datetime DEFAULT NULL,
  `symbol` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `create_time_symbol_idx` (`create_time`,`symbol`),
  KEY `line_index_symbol_idx` (`line_index`,`symbol`)
) ENGINE=InnoDB AUTO_INCREMENT=5333 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for tb_sell_order_record
-- ----------------------------
DROP TABLE IF EXISTS `tb_sell_order_record`;
CREATE TABLE `tb_sell_order_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(20) DEFAULT NULL,
  `buy_price` decimal(12,5) DEFAULT NULL COMMENT '买入时的价格',
  `sell_price` decimal(12,5) DEFAULT NULL COMMENT '卖出的价格',
  `buy_index` bigint(20) DEFAULT NULL COMMENT '买入时的时间戳秒',
  `sell_index` bigint(20) DEFAULT NULL COMMENT '卖出时的时间戳秒',
  `buy_orderId` varchar(50) DEFAULT NULL COMMENT '买的订单id',
  `sell_orderId` varchar(50) DEFAULT NULL COMMENT '卖的订单id',
  `amount` decimal(12,5) DEFAULT NULL COMMENT '数量',
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `s_soi_idx` (`symbol`,`sell_orderId`),
  KEY `s_boi` (`symbol`,`buy_orderId`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='提前卖的记录';

-- ----------------------------
-- Table structure for tb_stop_loss_history_record
-- ----------------------------
DROP TABLE IF EXISTS `tb_stop_loss_history_record`;
CREATE TABLE `tb_stop_loss_history_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` tinyint(2) DEFAULT NULL COMMENT '0卖出  1买入',
  `symbol` varchar(20) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `oper_price` decimal(12,5) DEFAULT NULL COMMENT '本次操作的价格',
  `last_price` decimal(12,5) DEFAULT NULL COMMENT '上一次操作的价格',
  `amount` decimal(12,5) DEFAULT NULL COMMENT '数量',
  `ori_order_id` varchar(50) DEFAULT NULL COMMENT '原始订单id',
  `order_id` varchar(50) DEFAULT NULL COMMENT '本次止损的订单id',
  PRIMARY KEY (`id`),
  KEY `symbol_idx` (`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='止损的历史记录';

-- ----------------------------
-- Table structure for tb_stop_loss_record
-- ----------------------------
DROP TABLE IF EXISTS `tb_stop_loss_record`;
CREATE TABLE `tb_stop_loss_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(20) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `sell_price` decimal(12,5) DEFAULT NULL COMMENT '止损卖出的价格',
  `ori_price` decimal(12,5) DEFAULT NULL COMMENT '原始买入的价格',
  `ori_amount` decimal(12,5) DEFAULT NULL COMMENT '原始数量',
  `ori_order_id` varchar(50) DEFAULT NULL COMMENT '原始订单id',
  `order_id` varchar(50) DEFAULT NULL COMMENT '本次止损的订单id',
  `status` tinyint(2) DEFAULT '0' COMMENT '0默认状态  1 进入交易队列',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `symbol_idx` (`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='止损卖出的记录';

-- ----------------------------
-- Table structure for tb_symbol_statistics_ofday
-- ----------------------------
DROP TABLE IF EXISTS `tb_symbol_statistics_ofday`;
CREATE TABLE `tb_symbol_statistics_ofday` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(20) DEFAULT NULL,
  `balance` decimal(20,8) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `up_down_range` float(11,5) DEFAULT NULL COMMENT '与前一日对比的涨跌幅度',
  PRIMARY KEY (`id`),
  KEY `create_time` (`create_time`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for tb_transaction_config
-- ----------------------------
DROP TABLE IF EXISTS `tb_transaction_config`;
CREATE TABLE `tb_transaction_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(20) DEFAULT NULL COMMENT '交易对 eosusdt',
  `every_expense` decimal(12,3) DEFAULT NULL COMMENT '每次交易的金额',
  `trade_gap` decimal(12,3) DEFAULT NULL COMMENT '与以往的交易间隔',
  `min_income` decimal(12,3) DEFAULT NULL COMMENT '最低收益率',
  `period` varchar(20) DEFAULT '1min' COMMENT 'K线周期',
  `precision` int(5) DEFAULT '2' COMMENT '小数点精度',
  `price_precision` int(5) DEFAULT NULL COMMENT '价格精度',
  `stopLoss` decimal(12,3) DEFAULT NULL COMMENT '止损点',
  `status` tinyint(2) DEFAULT '1' COMMENT '1 正常 0失效',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COMMENT='交易对配置';
