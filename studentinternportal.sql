-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 21, 2025 at 08:04 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `studentinternportal`
--

-- --------------------------------------------------------

--
-- Table structure for table `student_data`
--

CREATE TABLE `student_data` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `course` varchar(255) DEFAULT NULL,
  `branch` varchar(255) DEFAULT NULL,
  `institute_name` varchar(255) DEFAULT NULL,
  `project_domain` varchar(255) DEFAULT NULL,
  `project_title` varchar(255) DEFAULT NULL,
  `date_mentacc` date DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `guardian_name` varchar(255) DEFAULT NULL,
  `guardian_designation` varchar(255) DEFAULT NULL,
  `guardian_phn_no` varchar(25) DEFAULT NULL,
  `employee_code_no` varchar(50) DEFAULT NULL,
  `year_of_study` varchar(20) DEFAULT NULL,
  `institute_address` varchar(255) DEFAULT NULL,
  `permanent_address` varchar(255) DEFAULT NULL,
  `local_address` varchar(255) DEFAULT NULL,
  `phn_no` varchar(30) DEFAULT NULL,
  `alternate_phn_no` varchar(30) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `alternate_email` varchar(255) DEFAULT NULL,
  `project_group` varchar(255) DEFAULT NULL,
  `training_from_date` date DEFAULT NULL,
  `training_to_date` date DEFAULT NULL,
  `bank_name` varchar(255) DEFAULT NULL,
  `dd_no` varchar(255) DEFAULT NULL,
  `date_of_dd` date DEFAULT NULL,
  `date_of_dd2` date DEFAULT NULL,
  `amount` varchar(255) DEFAULT NULL,
  `designation_english` varchar(255) DEFAULT NULL,
  `designation_hindi` varchar(255) DEFAULT NULL,
  `incharge_english` varchar(255) DEFAULT NULL,
  `incharge_hindi` varchar(255) DEFAULT NULL,
  `conduct` varchar(150) DEFAULT NULL,
  `ref_no` varchar(100) DEFAULT NULL,
  `file_data` longblob DEFAULT NULL,
  `certificate` varchar(255) DEFAULT NULL,
  `guide_name` varchar(255) DEFAULT NULL,
  `submission_id` varchar(128) DEFAULT NULL,
  `joiningfile` longblob DEFAULT NULL,
  `dateofjoining` date DEFAULT NULL,
  `nodues_file` longblob DEFAULT NULL,
  `attendance` varchar(255) DEFAULT NULL,
  `projectdetails` varchar(1000) DEFAULT NULL,
  `idc` varchar(255) DEFAULT NULL,
  `gender` varchar(100) DEFAULT NULL,
  `mark` varchar(100) DEFAULT NULL,
  `photo` longblob DEFAULT NULL,
  `certificatecollectiondate` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(128) NOT NULL,
  `password` varchar(128) NOT NULL,
  `type` varchar(128) NOT NULL,
  `phone_no` varchar(15) NOT NULL,
  `email` varchar(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `type`, `phone_no`, `email`) VALUES
(23, 'admin', 'admin', 'admin', '9392702726', 'chaitan22bcd38@iiitkottayam.ac.in'),
(25, 'operator', 'operator', 'operator', '', 'okokkokoko@gmail.com');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `student_data`
--
ALTER TABLE `student_data`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `student_data`
--
ALTER TABLE `student_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
