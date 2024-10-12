-- Adminer 4.8.1 MySQL 10.4.32-MariaDB dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP DATABASE IF EXISTS `tiktok-downloader`;
CREATE DATABASE `tiktok-downloader` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `tiktok-downloader`;

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `first_name` (`first_name`),
  KEY `last_name` (`last_name`),
  KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `videos`;
CREATE TABLE `videos` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `author_id` varchar(255) DEFAULT NULL,
  `author_username` varchar(255) DEFAULT NULL,
  `video_id` bigint(20) NOT NULL,
  `file_id` varchar(255) NOT NULL,
  `file_unique_id` varchar(255) NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `video_id` (`video_id`),
  KEY `file_id` (`file_id`),
  KEY `file_unique_id` (`file_unique_id`),
  KEY `author_id` (`author_id`),
  KEY `author_username` (`author_username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- 2024-10-12 23:06:54