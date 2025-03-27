-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 27, 2025 at 04:16 PM
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
-- Database: `user_registration`
--

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `verification_code` varchar(32) DEFAULT NULL,
  `is_verified` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `reset_token` varchar(32) DEFAULT NULL,
  `reset_token_expiry` datetime DEFAULT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `bio` text DEFAULT NULL,
  `skills` varchar(255) DEFAULT NULL,
  `profile_pic` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `verification_code`, `is_verified`, `created_at`, `reset_token`, `reset_token_expiry`, `full_name`, `bio`, `skills`, `profile_pic`) VALUES
(3, 'Lisa', 'lisa@gmail.com', 'scrypt:32768:8:1$01VP7JEJVXS9VNxi$da85f50a068dbd2a908162da3c32aa64ce21716eb7b1788540c3215a69289bfb09e971d7e7dac7f37d4f538c03705f06f8cdbb380cf2aaa7437dcf68730a6c39', NULL, 0, '2025-03-25 20:49:52', NULL, NULL, 'Lisa Smith', 'Dreamer, doer, and lover of all things creative. ✨\r\n\r\nBuilding my empire, one step at a time. 💼👑\r\n\r\nFueled by coffee, passion, and a little bit of chaos. ☕🔥', 'Empathy, multitasking, leadership, communication, emotional intelligence, problem-solving, creativity, adaptability, negotiation, conflict resolution, strategic planning, project management, time management, teamwork, decision-making, personal branding', 'Lisa_2754576_woman_female_avatar_icon.png'),
(4, 'John', 'john@gmail.com', 'scrypt:32768:8:1$PYnjd6dxAuurBLCx$0c0760a4cb16f0d30098c24c331314bde5647270fb91ac65b73c564bd7eae64ce9aafb1983b7bf4c3c5c73e5ca0e32609850566cf901ab15ba4cd3d92cddb043', NULL, 0, '2025-03-25 20:56:09', NULL, NULL, 'John Smith', 'Explorer | Dreamer | Coffee Addict | Storyteller | Wanderlust | Creator | Innovator | Music Junkie | Bookworm | Free Spirit | Thinker | Adventurer | Night Owl | Optimist | Rebel | Visionary | Lifelong Learner | Minimalist | Hustler | Dream Chaser | Problem Solver | Art Lover | Foodie | Gamer | Curious Mind | Nature Enthusiast | Introvert | Extrovert | Ambivert | Coffee & Code | Fitness Fanatic', 'Creative writing, public speaking, problem-solving, leadership, graphic design, coding, time management, data analysis, social media marketing, negotiation, critical thinking, project management, photography, video editing, SEO, copywriting, UX/UI design', 'John_portrait-man-cartoon-style.jpg'),
(5, 'Ragnar', 'vikings@gmail.com', 'scrypt:32768:8:1$aT30Ygr1OLLfGYWI$6f42b5926899e6f6014d17fa77273f3fcc9456b0be95d1e55fc67e5daf746a1dac036e6f53a2dbdd3794d215b6f89927acefaaed331967b78212fbc9686bc6c5', NULL, 0, '2025-03-25 23:24:56', NULL, NULL, 'Ragnar Lothbrok', 'Viking king, warrior, and conqueror of kingdoms. ⚔️🛡️\r\nSon of the gods, born to lead and fight. 🌿🔥\r\nFearless in battle, driven by destiny. 💥\r\nTales of my deeds echo across the seas. 🌊⚔️\r\nChasing glory, forging legends. 🏰🔱\r\nBrother, father, king – the saga continues. ⚔️👑', 'War strategy, leadership, swordsmanship, axe fighting, tactical warfare, inspiring loyalty, negotiation, resilience, survival skills, fearlessness, adaptability, visionary thinking, decision-making, navigation, diplomacy, ambition, conquering', 'Ragnar_Ragnar_Full_HD_wallpaper.jpg'),
(6, 'Floki', 'floki@gmail.com', 'scrypt:32768:8:1$iFsOj2Hax0vAOYo4$dab83a93f49e5697ae081e09f99d410fde8d7e95b0007e0986e34f32005735a82c2d86b627844defd7ffce779e5c2d1ffdd6384f3478450582e99f276f872f0a', NULL, 0, '2025-03-25 23:32:57', NULL, NULL, 'Floki Vilgerðarson', 'Master shipbuilder, trickster, and loyal to the gods. ⛵⚒️\r\nBuilder of dreams, servant of destiny. 🔨🌊\r\nA madman to some, a genius to others. 🌀🔥\r\nSailing into the unknown, guided by the gods. 🌊⚡\r\nLoki’s spirit, Odin’s wisdom, my own path. 🏹🛶\r\nI do not follow kings—I follow the gods. ⚡🌿', 'Shipbuilding, navigation, engineering, carpentry, innovation, tactical warfare, survival skills, creativity, blacksmithing, problem-solving, strategic thinking, fearlessness, loyalty, intuition, architecture, craftsmanship, resourcefulness, devotion, agil', 'Floki_loki.jpg'),
(7, 'The_Imp', 'dwarf@gmail.com', 'scrypt:32768:8:1$jWgnA1zsaJt097WO$91c587d7dc35fdde985eb268b1450f6e8192e49f841b50dd51f16f2fad1440d60b5f00728582378a024f13921b63c34c3a110f24d7bf5a413031387b73f9dbb0', NULL, 0, '2025-03-25 23:43:30', NULL, NULL, 'Tyrion Lannister', 'I drink and I know things. 🍷📖\r\nSharp mind, sharper tongue. 🐉🔥\r\nThe Imp, the Halfman, the Master of Survival. 🏰♟️\r\nOutspoken, underestimated, and always one step ahead. 🧠⚔️\r\nBorn a lion, but I choose my own path. 🦁👑\r\nWords are my weapons, wit is my shield. 🍷🗡️\r\nA Lannister always pays his debts. 💰', 'Strategic thinking, diplomacy, manipulation, negotiation, public speaking, quick wit, survival instincts, reading people, politics, leadership, persuasion, deception, financial management, humor, adaptability, resilience, knowledge of history, drinking', 'The_Imp_tyrion_lannister_icon.jpg'),
(8, 'JonSnow', 'js@gmail.com', 'scrypt:32768:8:1$Ezbpn3o9jXcll4m6$511625d91bf0bc482b957036646d9b5c8fa8733fa4677209db525dbfbf7dd16c9585d51df8cc4d6329415b0a0de4293cbd5e07d7eccdb841c87f218c394c50f5', NULL, 0, '2025-03-26 00:18:58', 'AM0qen0PQI2QriMa1OFasjzPE3_j4DJI', '2025-03-27 02:08:36', 'Aegon Targaryen VI  a.k.a John Snow ', 'A bastard by birth, a leader by fate. ❄️⚔️\r\nThe wolf in the night, the fire in the cold. 🐺🔥\r\nI never wanted a crown, but duty called. 👑⚔️\r\nYou know nothing, but I know honor. ❄️🗡️\r\nBound by duty, led by honor, shaped by sacrifice. 🏰⚔️\r\nBrother, warrior, king—yet still a man of the North. ❄️🐺\r\nThe real war was never for the throne. 🏹🔥', 'Swordsmanship, leadership, resilience, loyalty, tactical warfare, survival skills, horseback riding, negotiation, diplomacy, adaptability, endurance, hand-to-hand combat, honor-driven decision-making, inspiring others, strategic thinking, perseverance', 'Jon_Snow_jon_snow_icon.jpg'),
(9, 'Bean', 'bean@gmail.com', 'scrypt:32768:8:1$53KCYh5mCCsEGT8p$44f8c9218fdf58b1db9c1612477f97d0549c6ff07fcc1e45a699a4971a9d4d1b9804da79270be0c10b81bcf90fb0d68b56e5b021274fb19a596623dc1f164ed5', NULL, 0, '2025-03-26 21:25:13', NULL, NULL, 'Mr.Bean', 'Silent but hilarious! 😆 | \r\nMaster of mischief 🤪 | \r\nLover of Teddy 🧸 | \r\nCreating chaos everywhere I go! 🚗💥', 'Problem-solving in the weirdest ways, physical comedy, extreme facial expressions, driving (recklessly), mischief-making, improvisation, childlike curiosity, getting into trouble, creative thinking, miming, teddy bear companionship, ruining other people\'s', 'Mr_Bean_Mr__Bean.jpg'),
(10, 'test_user', 'test@example.com', 'test_password', NULL, 0, '2025-03-27 03:09:07', NULL, NULL, NULL, NULL, NULL, NULL),
(11, 'jon_doe', 'jd@gmail.com', 'scrypt:32768:8:1$U2FphxWuaeu9l0AT$8bf3b25f5a08bea3154136a0c069cbbdd2f6bc72867b807fca03cf841ec4db143eecceef274a7ce05cf75bb3dff04139ddd0fa4b51a2fe9864a6810f43e8f894', NULL, 0, '2025-03-27 03:11:12', NULL, NULL, 'Jon Doe', 'Electrical Engineer', 'Playing, Running, Cooking', 'jon_doe_jond.jpg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
