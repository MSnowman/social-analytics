CREATE TABLE `stock_prices` (
  `time` datetime NOT NULL,
  `ticker` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `price` int(11) DEFAULT NULL,
  `ccy` varchar(3) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `exchagne` varchar(45) DEFAULT NULL,
  `high` varchar(45) NOT NULL,
  `low` varchar(45) NOT NULL,
  `open` varchar(45) NOT NULL,
  `close` varchar(45) NOT NULL,
  `volume` varchar(45) NOT NULL,
  PRIMARY KEY (`time`,`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;