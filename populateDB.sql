-- Insert vendors
INSERT INTO vendors (vendor_id, name, hash, store_name, description, contact_info) VALUES
(1, 'Tech Haven', 'abc123', 'Tech Haven Electronics', 'Your one-stop shop for the latest gadgets.', 'techhaven@example.com'),
(2, 'Home Essentials', 'def456', 'Home Essentials Supply', 'Quality products for your home needs.', 'homeessentials@example.com'),
(3, 'Fashion Fiesta', 'ghi789', 'Fashion Fiesta Boutique', 'Trendy clothing for every occasion.', 'fashionfiesta@example.com'),
(4, 'Pet Paradise', 'jkl012', 'Pet Paradise Store', 'Everything your pet could need.', 'petparadise@example.com'),
(5, 'Gourmet Delights', 'mno345', 'Gourmet Delights Market', 'Fine foods and gourmet treats.', 'gourmetdelights@example.com'),
(6, 'Fitness Hub', 'pqr678', 'Fitness Hub Gym', 'Gear up for your fitness journey.', 'fitnesshub@example.com'),
(7, 'Book Nook', 'stu901', 'The Book Nook', 'Your favorite reads at great prices.', 'booknook@example.com'),
(8, 'Crafty Corner', 'vwx234', 'Crafty Corner Supplies', 'Supplies for all your crafting needs.', 'craftycornersupplies@example.com');

-- Insert items for Tech Haven
INSERT INTO items (item_id, item_name, vendor_id, stock, price) VALUES
(1, 'Laptop Pro', 1, 10, 1200.00),
(2, 'Wireless Mouse', 1, 25, 25.00),
(3, 'Bluetooth Headphones', 1, 15, 75.00),
(4, '4K Monitor', 1, 8, 300.00),
(5, 'USB-C Hub', 1, 20, 45.00),
(6, 'Gaming Keyboard', 1, 12, 100.00),
(7, 'Smartwatch', 1, 18, 150.00),
(8, 'External SSD', 1, 10, 120.00),
(9, 'Portable Charger', 1, 30, 40.00),
(10, 'VR Headset', 1, 5, 400.00);

-- Insert items for Home Essentials
INSERT INTO items (item_id, item_name, vendor_id, stock, price) VALUES
(11, 'Kitchen Knife Set', 2, 20, 60.00),
(12, 'Non-stick Cookware', 2, 15, 80.00),
(13, 'Bedding Set', 2, 10, 100.00),
(14, 'Bath Towels', 2, 25, 15.00),
(15, 'Vacuum Cleaner', 2, 8, 200.00),
(16, 'Air Purifier', 2, 12, 150.00),
(17, 'Storage Bins', 2, 30, 10.00),
(18, 'Dining Table', 2, 5, 400.00),
(19, 'Wall Art', 2, 18, 70.00),
(20, 'Coffee Maker', 2, 15, 90.00);

-- Insert items for Fashion Fiesta
INSERT INTO items (item_id, item_name, vendor_id, stock, price) VALUES
(21, 'Summer Dress', 3, 20, 50.00),
(22, 'Casual Sneakers', 3, 15, 65.00),
(23, 'Leather Jacket', 3, 10, 120.00),
(24, 'Beanie Hat', 3, 25, 20.00),
(25, 'Sunglasses', 3, 30, 30.00),
(26, 'Denim Jeans', 3, 12, 45.00),
(27, 'Evening Gown', 3, 8, 200.00),
(28, 'Crossbody Bag', 3, 18, 55.00),
(29, 'Sports Bra', 3, 25, 25.00),
(30, 'Knit Sweater', 3, 15, 40.00);

-- Insert items for Pet Paradise
INSERT INTO items (item_id, item_name, vendor_id, stock, price) VALUES
(31, 'Dog Food', 4, 20, 50.00),
(32, 'Cat Litter', 4, 15, 20.00),
(33, 'Pet Bed', 4, 10, 35.00),
(34, 'Chew Toys', 4, 25, 10.00),
(35, 'Leash Set', 4, 30, 15.00),
(36, 'Fish Tank', 4, 8, 120.00),
(37, 'Bird Cage', 4, 5, 80.00),
(38, 'Grooming Kit', 4, 12, 45.00),
(39, 'Pet Carrier', 4, 10, 60.00),
(40, 'Scratch Post', 4, 15, 30.00);

-- Insert items for Gourmet Delights
INSERT INTO items (item_id, item_name, vendor_id, stock, price) VALUES
(41, 'Artisan Cheese', 5, 20, 25.00),
(42, 'Organic Olive Oil', 5, 15, 15.00),
(43, 'Dark Chocolate', 5, 30, 5.00),
(44, 'Gourmet Coffee', 5, 10, 10.00),
(45, 'Specialty Pasta', 5, 25, 7.00),
(46, 'Spices Set', 5, 12, 30.00),
(47, 'Fruit Preserves', 5, 18, 8.00),
(48, 'Honey Jar', 5, 15, 6.00),
(49, 'Tea Assortment', 5, 20, 12.00),
(50, 'Wine Selection', 5, 5, 20.00);

-- Insert items for Fitness Hub
INSERT INTO items (item_id, item_name, vendor_id, stock, price) VALUES
(51, 'Yoga Mat', 6, 25, 30.00),
(52, 'Dumbbell Set', 6, 15, 80.00),
(53, 'Resistance Bands', 6, 30, 20.00),
(54, 'Protein Powder', 6, 10, 50.00),
(55, 'Water Bottle', 6, 50, 10.00),
(56, 'Gym Bag', 6, 20, 35.00),
(57, 'Fitness Tracker', 6, 12, 100.00),
(58, 'Exercise Bike', 6, 8, 300.00),
(59, 'Jump Rope', 6, 40, 15.00),
(60, 'Foam Roller', 6, 30, 25.00);

-- Insert items for Book Nook
INSERT INTO items (item_id, item_name, vendor_id, stock, price) VALUES
(61, 'Mystery Novel', 7, 20, 15.00),
(62, 'Science Fiction Anthology', 7, 15, 20.00),
(63, 'Historical Biography', 7, 10, 25.00),
(64, 'Self-Help Guide', 7, 18, 12.00),
(65, 'Cookbook', 7, 25, 30.00),
(66, 'Children’s Storybook', 7, 30, 10.00),
(67, 'Graphic Novel', 7, 15, 20.00),
(68, 'Poetry Collection', 7, 12, 18.00),
(69, 'Travel Guide', 7, 8, 22.00),
(70, 'Classic Literature', 7, 10, 25.00);

-- Insert items for Crafty Corner
INSERT INTO items (item_id, item_name, vendor_id, stock, price) VALUES
(71, 'Acrylic Paint Set', 8, 20, 25.00),
(72, 'Sewing Machine', 8, 10, 150.00),
(73, 'Scrapbook Paper', 8, 30, 15.00),
(74, 'Knitting Needles', 8, 25, 5.00),
(75, 'Canvas Boards', 8, 20, 10.00),
(76, 'Glue Gun', 8, 15, 20.00),
(77, 'Beading Kit', 8, 12, 30.00),
(78, 'Craft Scissors', 8, 25, 8.00),
(79, 'Calligraphy Pens', 8, 18, 12.00),
(80, 'DIY Candle Kit', 8, 10, 40.00);