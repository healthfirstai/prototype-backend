CREATE DATABASE IF NOT EXISTS `healthfirstai`;
USE healthfirstai;

DROP TABLE IF EXISTS `food`;
DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `city`;
DROP TABLE IF EXISTS `country`;
DROP TABLE IF EXISTS `meal_plan`;
DROP TABLE IF EXISTS `meal`;
DROP TABLE IF EXISTS `meal_ingredient`;
DROP TABLE IF EXISTS `measurement`;
DROP TABLE IF EXISTS `country`;


CREATE TABLE `food` (
  `ID` int NOT NULL,
  `Name` text,
  `Food Group` text,
  `Calories` int DEFAULT NULL,
  `Fat (g)` double DEFAULT NULL,
  `Protein (g)` double DEFAULT NULL,
  `Carbohydrate (g)` double DEFAULT NULL,
  `Sugars (g)` text,
  `Fiber (g)` text,
  `Cholesterol (mg)` text,
  `Saturated Fats (g)` text,
  `Calcium (mg)` text,
  `Iron, Fe (mg)` text,
  `Potassium, K (mg)` text,
  `Magnesium (mg)` text,
  `Vitamin A, IU (IU)` text,
  `Vitamin A, RAE (mcg)` text,
  `Vitamin C (mg)` text,
  `Vitamin B-12 (mcg)` text,
  `Vitamin D (mcg)` text,
  `Vitamin E (Alpha-Tocopherol) (mg)` text,
  `Added Sugar (g)` text,
  `Net-Carbs (g)` double DEFAULT NULL,
  `Water (g)` double DEFAULT NULL,
  `Omega 3s (mg)` text,
  `Omega 6s (mg)` text,
  `PRAL score` text,
  `Trans Fatty Acids (g)` text,
  `Soluble Fiber (g)` text,
  `Insoluble Fiber (g)` text,
  `Sucrose (g)` text,
  `Glucose (Dextrose) (g)` text,
  `Fructose (g)` text,
  `Lactose (g)` text,
  `Maltose (g)` text,
  `Galactose (g)` text,
  `Starch (g)` text,
  `Total sugar alcohols (g)` text,
  `Phosphorus, P (mg)` text,
  `Sodium (mg)` int DEFAULT NULL,
  `Zinc, Zn (mg)` text,
  `Copper, Cu (mg)` text,
  `Manganese (mg)` text,
  `Selenium, Se (mcg)` text,
  `Fluoride, F (mcg)` text,
  `Molybdenum (mcg)` text,
  `Chlorine (mg)` text,
  `Thiamin (B1) (mg)` text,
  `Riboflavin (B2) (mg)` text,
  `Niacin (B3) (mg)` text,
  `Pantothenic acid (B5) (mg)` text,
  `Vitamin B6 (mg)` text,
  `Biotin (B7) (mcg)` text,
  `Folate (B9) (mcg)` text,
  `Folic acid (mcg)` text,
  `Food Folate (mcg)` text,
  `Folate DFE (mcg)` text,
  `Choline (mg)` text,
  `Betaine (mg)` text,
  `Retinol (mcg)` text,
  `Carotene, beta (mcg)` text,
  `Carotene, alpha (mcg)` text,
  `Lycopene (mcg)` text,
  `Lutein + Zeaxanthin (mcg)` text,
  `Vitamin D2 (ergocalciferol) (mcg)` text,
  `Vitamin D3 (cholecalciferol) (mcg)` text,
  `Vitamin D (IU) (IU)` text,
  `Vitamin K (mcg)` text,
  `Dihydrophylloquinone (mcg)` text,
  `Menaquinone-4 (mcg)` text,
  `Fatty acids, total monounsaturated (mg)` text,
  `Fatty acids, total polyunsaturated (mg)` text,
  `18:3 n-3 c,c,c (ALA) (mg)` text,
  `20:5 n-3 (EPA) (mg)` text,
  `22:5 n-3 (DPA) (mg)` text,
  `22:6 n-3 (DHA) (mg)` text,
  `Tryptophan (mg)` text,
  `Threonine (mg)` text,
  `Isoleucine (mg)` text,
  `Leucine (mg)` text,
  `Lysine (mg)` text,
  `Methionine (mg)` text,
  `Cystine (mg)` text,
  `Phenylalanine (mg)` text,
  `Tyrosine (mg)` text,
  `Valine (mg)` text,
  `Arginine (mg)` text,
  `Histidine (mg)` text,
  `Alanine (mg)` text,
  `Aspartic acid (mg)` text,
  `Glutamic acid (mg)` text,
  `Glycine (mg)` text,
  `Proline (mg)` text,
  `Serine (mg)` text,
  `Hydroxyproline (mg)` text,
  `Alcohol (g)` text,
  `Caffeine (mg)` text,
  `Theobromine (mg)` text,
  `Serving Weight 1 (g)` double DEFAULT NULL,
  `Serving Description 1 (g)` text,
  `Serving Weight 2 (g)` text,
  `Serving Description 2 (g)` text,
  `Serving Weight 3 (g)` text,
  `Serving Description 3 (g)` text,
  `Serving Weight 4 (g)` text,
  `Serving Description 4 (g)` text,
  `Serving Weight 5 (g)` text,
  `Serving Description 5 (g)` text,
  `Serving Weight 6 (g)` text,
  `Serving Description 6 (g)` text,
  `Serving Weight 7 (g)` text,
  `Serving Description 7 (g)` text,
  `Serving Weight 8 (g)` text,
  `Serving Description 8 (g)` text,
  `Serving Weight 9 (g)` text,
  `Serving Description 9 (g)` text,
  `200 Calorie Weight (g)` double DEFAULT NULL,
  PRIMARY KEY(`ID`)
);

CREATE TABLE `country`
(
    `ID`        INT          NOT NULL AUTO_INCREMENT,
    `name`      VARCHAR(255) NOT NULL,
    `continent` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`ID`)
);

CREATE TABLE `city`
(
    `ID`         INT          NOT NULL AUTO_INCREMENT,
    `name`       VARCHAR(255) NOT NULL,
    `country_id` INT          NOT NULL,
    PRIMARY KEY (`ID`),
    FOREIGN KEY (`country_id`) REFERENCES `country` (`ID`) ON DELETE CASCADE
);

CREATE TABLE `user`
(
    `ID`         INT                              NOT NULL AUTO_INCREMENT,
    `height`     DECIMAL(5, 2)                    NOT NULL,
    `weight`     DECIMAL(5, 2)                    NOT NULL,
    `gender`     ENUM ('Male', 'Female', 'Other') NOT NULL,
    `age`        INT                              NOT NULL,
    `country_id` INT                              NOT NULL,
    `city_id`    INT                              NOT NULL,
    `start_date` DATE                             NOT NULL,
    `end_date`   DATE                             NOT NULL,
    PRIMARY KEY (`ID`),
    FOREIGN KEY (`country_id`) REFERENCES `country` (`ID`) ON DELETE CASCADE,
    FOREIGN KEY (`city_id`) REFERENCES `city` (`ID`) ON DELETE CASCADE
);

CREATE TABLE `meal_plan` (
    `ID` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`ID`)
);

CREATE TABLE `meal` (
    `ID` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `meal_plan_id` INT NOT NULL,
    PRIMARY KEY (`ID`),
    FOREIGN KEY (`meal_plan_id`) REFERENCES `meal_plan` (`ID`) ON DELETE CASCADE
);

CREATE TABLE `measurement` (
    `ID` INT NOT NULL AUTO_INCREMENT,
    `unit` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`ID`)
);

CREATE TABLE `meal_ingredient` (
    `meal_id` INT NOT NULL,
    `ingredient_id` INT NOT NULL,
    `measurement_id` INT NOT NULL,
    `quantity` DECIMAL(5,2) NOT NULL,
    PRIMARY KEY (`meal_id`, `ingredient_id`),
    FOREIGN KEY (`meal_id`) REFERENCES `meal` (`ID`) ON DELETE CASCADE,
    FOREIGN KEY (`ingredient_id`) REFERENCES `food` (`ID`) ON DELETE CASCADE,
    FOREIGN KEY (`measurement_id`) REFERENCES `measurement` (`ID`) ON DELETE CASCADE
);
