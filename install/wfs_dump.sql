/*! WFS Database settings */;
/*! Insert this to DB and all tables will be created with necessary settings */;

--
-- Table structure for table `gps`
--

DROP TABLE IF EXISTS `gps`;
CREATE TABLE `gps` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `lat` float DEFAULT NULL,
  `lon` float DEFAULT NULL,
  `alt` float DEFAULT NULL,
  `tmestmp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table `mean`
--

DROP TABLE IF EXISTS `mean`;
CREATE TABLE `mean` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `mean` float DEFAULT NULL,
  `tmestmp` datetime DEFAULT CURRENT_TIMESTAMP,
  `red` int(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table `sens`
--

DROP TABLE IF EXISTS `sens`;
CREATE TABLE `sens` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `temp` float DEFAULT NULL,
  `hum` int DEFAULT NULL,
  `atp` int(11) DEFAULT NULL,
  `issame` int(2) DEFAULT NULL,
  `tmestmp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table `wind`
--

DROP TABLE IF EXISTS `wind`;
CREATE TABLE `wind` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `wind` float DEFAULT NULL,
  `tmestmp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table `error`
--

DROP TABLE IF EXISTS `error`;
CREATE TABLE `error` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `file` varchar(100) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `obj` varchar(100) DEFAULT NULL,
  `line` int(9) DEFAULT NULL,
  `tmestmp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
  )ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
