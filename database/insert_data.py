import sqlite3

conn = sqlite3.connect("retailmind.db")
cursor = conn.cursor()

# Purana data delete
cursor.execute("DELETE FROM products")

products = [

# =====================================================
# GRAINS
# =====================================================

("890100000001","Aashirvaad Atta 5Kg","Aashirvaad","Grains","5 Kg",220,250,80,10,"ABC Traders","Nashik",5,"110100","2027-12-31","A1","Active"),

("890100000002","Aashirvaad Atta 10Kg","Aashirvaad","Grains","10 Kg",430,470,60,10,"ABC Traders","Nashik",5,"110100","2027-12-31","A1","Active"),

("890100000003","Fortune Chakki Fresh","Fortune","Grains","5 Kg",230,255,70,10,"ABC Traders","Malegaon",5,"110100","2027-12-31","A2","Active"),

("890100000004","India Gate Basmati Rice","India Gate","Grains","5 Kg",520,580,45,8,"Rice World","Nashik",5,"100630","2028-01-31","A3","Active"),

("890100000005","Daawat Basmati Rice","Daawat","Grains","5 Kg",500,560,40,8,"Rice World","Pune",5,"100630","2028-01-31","A3","Active"),

("890100000006","Kolam Rice","Local","Grains","25 Kg",1250,1380,25,5,"Rice World","Malegaon",5,"100630","2028-01-31","A4","Active"),

("890100000007","Sona Masoori Rice","Local","Grains","25 Kg",1180,1320,20,5,"Rice World","Nashik",5,"100630","2028-01-31","A4","Active"),

("890100000008","Poha Thick","Laxmi","Grains","1 Kg",48,60,100,15,"Shree Foods","Nashik",5,"190410","2027-11-30","A5","Active"),

("890100000009","Suji","Fortune","Grains","1 Kg",38,50,120,20,"ABC Traders","Pune",5,"110311","2027-10-31","A5","Active"),

("890100000010","Daliya","Patanjali","Grains","500 g",28,40,90,15,"Patanjali Distributor","Nashik",5,"190420","2027-09-30","A5","Active"),

# =====================================================
# PULSES
# =====================================================

("890100000011","Toor Dal","Tata Sampann","Pulses","1 Kg",150,175,90,15,"Dal Suppliers","Nashik",5,"071360","2028-12-31","B1","Active"),

("890100000012","Moong Dal","Tata Sampann","Pulses","1 Kg",118,140,100,15,"Dal Suppliers","Nashik",5,"071331","2028-12-31","B1","Active"),

("890100000013","Chana Dal","Fortune","Pulses","1 Kg",82,100,110,20,"Dal Suppliers","Malegaon",5,"071320","2028-12-31","B2","Active"),

("890100000014","Urad Dal","Fortune","Pulses","1 Kg",132,155,80,15,"Dal Suppliers","Pune",5,"071340","2028-12-31","B2","Active"),

("890100000015","Masoor Dal","Tata Sampann","Pulses","1 Kg",92,115,95,15,"Dal Suppliers","Nashik",5,"071340","2028-12-31","B3","Active"),

("890100000016","Rajma","Organic India","Pulses","1 Kg",120,145,70,10,"Dal Suppliers","Pune",5,"071333","2028-12-31","B3","Active"),

("890100000017","Kabuli Chana","Fortune","Pulses","1 Kg",118,145,75,10,"Dal Suppliers","Malegaon",5,"071320","2028-12-31","B4","Active"),

("890100000018","Kala Chana","Local","Pulses","1 Kg",78,95,110,20,"Dal Suppliers","Nashik",5,"071320","2028-12-31","B4","Active"),

("890100000019","Safed Vatana","Local","Pulses","1 Kg",68,85,90,15,"Dal Suppliers","Nashik",5,"071310","2028-12-31","B5","Active"),

("890100000020","Dry Green Peas","Local","Pulses","1 Kg",72,90,85,15,"Dal Suppliers","Malegaon",5,"071310","2028-12-31","B5","Active"),

# =====================================================
# OIL & GHEE
# =====================================================

("890100000021","Fortune Sunflower Oil","Fortune","Oil & Ghee","1 L",145,165,120,20,"Oil Traders","Nashik",5,"151219","2027-12-31","C1","Active"),

("890100000022","Fortune Soyabean Oil","Fortune","Oil & Ghee","1 L",135,155,130,20,"Oil Traders","Malegaon",5,"150790","2027-12-31","C1","Active"),

("890100000023","Dhara Mustard Oil","Dhara","Oil & Ghee","1 L",165,190,90,15,"Oil Traders","Pune",5,"151499","2027-12-31","C2","Active"),

("890100000024","Engine Groundnut Oil","Engine","Oil & Ghee","1 L",185,210,70,15,"Oil Traders","Nashik",5,"150810","2027-12-31","C2","Active"),

("890100000025","Saffola Gold","Saffola","Oil & Ghee","1 L",175,205,60,10,"Oil Traders","Pune",5,"151219","2027-12-31","C3","Active"),

("890100000026","Rice Bran Oil","Fortune","Oil & Ghee","1 L",150,170,100,15,"Oil Traders","Malegaon",5,"151190","2027-12-31","C3","Active"),

("890100000027","Parachute Coconut Oil","Parachute","Oil & Ghee","500 ml",135,155,80,15,"Oil Traders","Nashik",5,"151311","2027-12-31","C4","Active"),

("890100000028","Amul Pure Ghee","Amul","Oil & Ghee","1 L",610,670,50,10,"Amul Distributor","Nashik",12,"040590","2027-09-30","C5","Active"),

("890100000029","Govardhan Ghee","Govardhan","Oil & Ghee","1 L",590,650,45,10,"Govardhan","Pune",12,"040590","2027-09-30","C5","Active"),

("890100000030","Dalda Vanaspati","Dalda","Oil & Ghee","1 Kg",145,170,75,15,"Oil Traders","Malegaon",5,"151620","2027-12-31","C6","Active"),

# =====================================================
# SPICES
# =====================================================

("890100000031","Everest Turmeric Powder","Everest","Spices","200 g",48,60,120,20,"Spice World","Nashik",5,"091030","2027-12-31","D1","Active"),

("890100000032","Everest Red Chilli Powder","Everest","Spices","200 g",62,75,100,20,"Spice World","Nashik",5,"090422","2027-12-31","D1","Active"),

("890100000033","Everest Coriander Powder","Everest","Spices","200 g",42,55,110,20,"Spice World","Pune",5,"090921","2027-12-31","D2","Active"),

("890100000034","Catch Jeera","Catch","Spices","100 g",58,70,90,15,"Spice World","Malegaon",5,"090931","2027-12-31","D2","Active"),

("890100000035","Mustard Seeds","Local","Spices","500 g",48,60,80,15,"Spice World","Nashik",5,"120750","2027-12-31","D3","Active"),

("890100000036","Ajwain","Catch","Spices","100 g",52,65,70,10,"Spice World","Pune",5,"091099","2027-12-31","D3","Active"),

("890100000037","MDH Garam Masala","MDH","Spices","100 g",68,85,90,15,"Spice World","Nashik",5,"091091","2027-12-31","D4","Active"),

("890100000038","MDH Kitchen King","MDH","Spices","100 g",70,88,85,15,"Spice World","Malegaon",5,"091091","2027-12-31","D4","Active"),

("890100000039","Everest Pav Bhaji Masala","Everest","Spices","100 g",62,78,80,15,"Spice World","Pune",5,"091091","2027-12-31","D5","Active"),

("890100000040","Everest Biryani Masala","Everest","Spices","100 g",68,85,75,15,"Spice World","Nashik",5,"091091","2027-12-31","D5","Active"),

# =====================================================
# SUGAR & SWEETENERS
# =====================================================

("890100000041","Madhur Sugar","Madhur","Sugar & Sweeteners","1 Kg",42,50,150,20,"Sweet Suppliers","Nashik",5,"170199","2028-12-31","E1","Active"),

("890100000042","Trust Sugar","Trust","Sugar & Sweeteners","1 Kg",41,49,140,20,"Sweet Suppliers","Malegaon",5,"170199","2028-12-31","E1","Active"),

("890100000043","Organic Jaggery","24 Mantra","Sugar & Sweeteners","1 Kg",65,80,80,15,"Organic Foods","Pune",5,"170114","2028-06-30","E2","Active"),

("890100000044","Mishri","Patanjali","Sugar & Sweeteners","500 g",48,60,70,10,"Patanjali Distributor","Nashik",5,"170290","2028-06-30","E2","Active"),

("890100000045","Brown Sugar","Organic India","Sugar & Sweeteners","500 g",78,95,50,10,"Organic Foods","Pune",5,"170199","2028-06-30","E3","Active"),

# =====================================================
# TEA & COFFEE
# =====================================================

("890100000046","Tata Tea Gold","Tata Tea","Tea & Coffee","1 Kg",520,590,70,10,"Tea Traders","Nashik",5,"090230","2028-12-31","F1","Active"),

("890100000047","Red Label Tea","Brooke Bond","Tea & Coffee","1 Kg",495,565,75,10,"Tea Traders","Malegaon",5,"090230","2028-12-31","F1","Active"),

("890100000048","Taj Mahal Tea","Brooke Bond","Tea & Coffee","500 g",290,335,60,10,"Tea Traders","Pune",5,"090230","2028-12-31","F2","Active"),

("890100000049","Nescafe Classic","Nestlé","Tea & Coffee","100 g",285,330,80,15,"Nestle India","Nashik",18,"210111","2028-12-31","F2","Active"),

("890100000050","Bru Instant Coffee","Bru","Tea & Coffee","100 g",265,310,70,15,"Coffee Traders","Malegaon",18,"210111","2028-12-31","F3","Active"),

# =====================================================
# DAIRY
# =====================================================

("890100000051","Amul Milk","Amul","Dairy","1 L",58,62,120,20,"Amul Distributor","Nashik",5,"040120","2027-12-31","G1","Active"),

("890100000052","Amul Butter","Amul","Dairy","500 g",255,285,60,10,"Amul Distributor","Nashik",12,"040510","2028-12-31","G1","Active"),

("890100000053","Amul Cheese","Amul","Dairy","200 g",118,135,50,10,"Amul Distributor","Pune",12,"040630","2028-12-31","G2","Active"),

("890100000054","Amul Paneer","Amul","Dairy","200 g",82,95,45,10,"Amul Distributor","Malegaon",5,"040610","2027-12-31","G2","Active"),

("890100000055","Amul Fresh Cream","Amul","Dairy","250 ml",62,75,40,8,"Amul Distributor","Nashik",12,"040150","2027-12-31","G3","Active"),

# =====================================================
# BISCUITS & BAKERY
# =====================================================

("890100000056","Parle-G","Parle","Biscuits & Bakery","800 g",48,60,200,30,"Parle Distributor","Nashik",18,"190531","2028-12-31","H1","Active"),

("890100000057","Marie Gold","Britannia","Biscuits & Bakery","250 g",28,35,180,25,"Britannia Distributor","Pune",18,"190531","2028-12-31","H1","Active"),

("890100000058","Good Day","Britannia","Biscuits & Bakery","200 g",32,40,170,25,"Britannia Distributor","Malegaon",18,"190531","2028-12-31","H2","Active"),

("890100000059","Bourbon","Britannia","Biscuits & Bakery","150 g",28,35,150,20,"Britannia Distributor","Nashik",18,"190531","2028-12-31","H2","Active"),

("890100000060","Hide & Seek","Parle","Biscuits & Bakery","120 g",32,40,140,20,"Parle Distributor","Pune",18,"190531","2028-12-31","H3","Active"),

# =====================================================
# INSTANT FOOD
# =====================================================

("890100000061","Maggi 2-Minute Noodles","Maggi","Instant Food","280 g",52,60,150,20,"Nestle India","Nashik",18,"190230","2028-12-31","I1","Active"),

("890100000062","Maggi Masala Noodles","Maggi","Instant Food","560 g",98,115,120,20,"Nestle India","Nashik",18,"190230","2028-12-31","I1","Active"),

("890100000063","Yippee Noodles","Sunfeast","Instant Food","280 g",48,58,130,20,"ITC Distributor","Pune",18,"190230","2028-12-31","I2","Active"),

("890100000064","Sunfeast Pasta","Sunfeast","Instant Food","500 g",62,75,90,15,"ITC Distributor","Malegaon",18,"190219","2028-12-31","I2","Active"),

("890100000065","Bambino Vermicelli","Bambino","Instant Food","500 g",42,55,100,15,"Bambino Foods","Nashik",5,"190219","2028-12-31","I3","Active"),

("890100000066","Quaker Oats","Quaker","Instant Food","1 Kg",175,210,70,10,"PepsiCo","Pune",5,"110412","2028-12-31","I3","Active"),

("890100000067","MTR Idli Mix","MTR","Instant Food","500 g",82,98,60,10,"MTR Foods","Nashik",5,"210690","2028-12-31","I4","Active"),

("890100000068","MTR Dosa Mix","MTR","Instant Food","500 g",84,100,60,10,"MTR Foods","Malegaon",5,"210690","2028-12-31","I4","Active"),

("890100000069","Gits Gulab Jamun Mix","Gits","Instant Food","200 g",52,65,70,10,"Gits Foods","Pune",5,"210690","2028-12-31","I5","Active"),

("890100000070","Gits Upma Mix","Gits","Instant Food","200 g",46,58,70,10,"Gits Foods","Nashik",5,"210690","2028-12-31","I5","Active"),

# =====================================================
# SOFT DRINKS & BEVERAGES
# =====================================================

("890100000071","Coca Cola","Coca-Cola","Soft Drinks","750 ml",38,45,120,18,"Coca-Cola Distributor","Nashik",28,"220210","2028-12-31","J1","Active"),

("890100000072","Pepsi","Pepsi","Soft Drinks","750 ml",38,45,120,18,"PepsiCo","Malegaon",28,"220210","2028-12-31","J1","Active"),

("890100000073","Thums Up","Coca-Cola","Soft Drinks","750 ml",40,48,110,18,"Coca-Cola Distributor","Nashik",28,"220210","2028-12-31","J1","Active"),

("890100000074","Sprite","Coca-Cola","Soft Drinks","750 ml",38,45,110,18,"Coca-Cola Distributor","Pune",28,"220210","2028-12-31","J2","Active"),

("890100000075","Fanta","Coca-Cola","Soft Drinks","750 ml",38,45,100,18,"Coca-Cola Distributor","Malegaon",28,"220210","2028-12-31","J2","Active"),

("890100000076","Limca","Coca-Cola","Soft Drinks","750 ml",38,45,95,18,"Coca-Cola Distributor","Nashik",28,"220210","2028-12-31","J2","Active"),

("890100000077","Maaza","Coca-Cola","Beverages","600 ml",38,45,90,18,"Coca-Cola Distributor","Pune",28,"220299","2028-12-31","J3","Active"),

("890100000078","Slice","Pepsi","Beverages","600 ml",38,45,90,18,"PepsiCo","Malegaon",28,"220299","2028-12-31","J3","Active"),

("890100000079","Real Mixed Fruit Juice","Real","Beverages","1 L",118,135,70,15,"Dabur Distributor","Nashik",12,"200990","2028-12-31","J4","Active"),

("890100000080","Tropicana Orange Juice","Tropicana","Beverages","1 L",125,145,65,15,"PepsiCo","Pune",12,"200990","2028-12-31","J4","Active"),

("890100000081","Frooti","Parle Agro","Beverages","1 L",105,120,80,15,"Parle Agro","Nashik",12,"220299","2028-12-31","J5","Active"),

("890100000082","Appy Fizz","Parle Agro","Beverages","250 ml",22,25,150,20,"Parle Agro","Malegaon",28,"220299","2028-12-31","J5","Active"),

("890100000083","Red Bull Energy Drink","Red Bull","Energy Drink","250 ml",115,125,40,8,"Red Bull India","Pune",28,"220299","2028-12-31","J6","Active"),

("890100000084","Monster Energy","Monster","Energy Drink","350 ml",125,140,35,8,"Monster India","Nashik",28,"220299","2028-12-31","J6","Active"),

("890100000085","Bisleri Mineral Water","Bisleri","Water","1 L",18,20,250,30,"Bisleri Distributor","Nashik",18,"220110","2028-12-31","J7","Active"),

("890100000086","Kinley Water","Kinley","Water","1 L",18,20,220,30,"Coca-Cola Distributor","Malegaon",18,"220110","2028-12-31","J7","Active"),

("890100000087","Aquafina Water","Aquafina","Water","1 L",18,20,220,30,"PepsiCo","Pune",18,"220110","2028-12-31","J8","Active"),

("890100000088","Paper Boat Aamras","Paper Boat","Beverages","600 ml",78,90,60,10,"Paper Boat","Nashik",12,"220299","2028-12-31","J8","Active"),

("890100000089","Paper Boat Jaljeera","Paper Boat","Beverages","600 ml",78,90,55,10,"Paper Boat","Malegaon",12,"220299","2028-12-31","J9","Active"),

("890100000090","Yakult Probiotic Drink","Yakult","Health Drink","65 ml x 5",95,110,40,8,"Yakult India","Pune",12,"220299","2028-12-31","J9","Active"),

# =====================================================
# CHOCOLATES & CONFECTIONERY
# =====================================================

("890100000091","Cadbury Dairy Milk","Cadbury","Chocolates","55 g",38,45,180,20,"Cadbury Distributor","Nashik",18,"180690","2028-12-31","K1","Active"),

("890100000092","Cadbury Silk","Cadbury","Chocolates","60 g",78,90,120,15,"Cadbury Distributor","Pune",18,"180690","2028-12-31","K1","Active"),

("890100000093","Cadbury 5 Star","Cadbury","Chocolates","40 g",18,20,200,25,"Cadbury Distributor","Malegaon",18,"180690","2028-12-31","K1","Active"),

("890100000094","Cadbury Perk","Cadbury","Chocolates","35 g",10,12,220,30,"Cadbury Distributor","Nashik",18,"180690","2028-12-31","K2","Active"),

("890100000095","Cadbury Gems","Cadbury","Chocolates","30 g",18,20,180,25,"Cadbury Distributor","Pune",18,"180690","2028-12-31","K2","Active"),

("890100000096","Nestle KitKat","Nestlé","Chocolates","38 g",18,20,220,30,"Nestle India","Nashik",18,"180690","2028-12-31","K2","Active"),

("890100000097","Nestle Munch","Nestlé","Chocolates","35 g",10,12,250,30,"Nestle India","Malegaon",18,"180690","2028-12-31","K3","Active"),

("890100000098","Nestle Milkybar","Nestlé","Chocolates","46 g",20,25,180,25,"Nestle India","Pune",18,"180690","2028-12-31","K3","Active"),

("890100000099","Nestle Bar One","Nestlé","Chocolates","35 g",18,20,170,20,"Nestle India","Nashik",18,"180690","2028-12-31","K3","Active"),

("890100000100","Ferrero Rocher","Ferrero","Chocolates","16 pcs",420,480,35,8,"Ferrero India","Mumbai",18,"180690","2028-12-31","K4","Active"),

("890100000101","Alpenliebe","Perfetti","Candy","200 g",48,60,160,20,"Perfetti Distributor","Nashik",18,"170490","2028-12-31","K4","Active"),

("890100000102","Mentos","Perfetti","Candy","200 g",52,65,150,20,"Perfetti Distributor","Malegaon",18,"170490","2028-12-31","K4","Active"),

("890100000103","Center Fresh","Perfetti","Chewing Gum","100 pcs",95,110,120,15,"Perfetti Distributor","Pune",18,"170410","2028-12-31","K5","Active"),

("890100000104","Center Fruit","Perfetti","Chewing Gum","100 pcs",95,110,120,15,"Perfetti Distributor","Nashik",18,"170410","2028-12-31","K5","Active"),

("890100000105","Orbit Sugar Free Gum","Wrigley","Chewing Gum","30 g",48,60,100,15,"Wrigley India","Pune",18,"170410","2028-12-31","K5","Active"),

("890100000106","Boomer Bubble Gum","Wrigley","Bubble Gum","100 pcs",95,110,100,15,"Wrigley India","Malegaon",18,"170410","2028-12-31","K6","Active"),

("890100000107","Pulse Candy","DS Group","Candy","180 g",95,110,140,20,"DS Group","Nashik",18,"170490","2028-12-31","K6","Active"),

("890100000108","Kismi Toffee","Parle","Toffee","200 g",58,70,140,20,"Parle Distributor","Pune",18,"170490","2028-12-31","K6","Active"),

("890100000109","Melody Chocolate","Parle","Toffee","200 g",65,80,130,20,"Parle Distributor","Malegaon",18,"170490","2028-12-31","K7","Active"),

("890100000110","Coffy Bite","Lotte","Candy","200 g",55,68,120,20,"Lotte India","Nashik",18,"170490","2028-12-31","K7","Active"),

# =====================================================
# SMALL GROCERY PRODUCTS
# =====================================================

("890100000111","Center Fresh","Perfetti","Chewing Gum","3 g",1,2,1000,100,"Perfetti Distributor","Nashik",18,"170410","2028-12-31","L1","Active"),
("890100000112","Center Fruit","Perfetti","Chewing Gum","4 g",1,2,1000,100,"Perfetti Distributor","Nashik",18,"170410","2028-12-31","L1","Active"),
("890100000113","Happy Dent","Perfetti","Chewing Gum","4 g",2,3,800,80,"Perfetti Distributor","Malegaon",18,"170410","2028-12-31","L1","Active"),
("890100000114","Boomer","Wrigley","Bubble Gum","5 g",2,3,700,70,"Wrigley India","Pune",18,"170410","2028-12-31","L1","Active"),
("890100000115","Orbit","Wrigley","Chewing Gum","14 g",8,10,400,40,"Wrigley India","Nashik",18,"170410","2028-12-31","L1","Active"),
("890100000116","Pulse","DS Group","Candy","4 g",1,2,1200,120,"DS Group","Nashik",18,"170490","2028-12-31","L2","Active"),
("890100000117","Melody","Parle","Toffee","5 g",1,2,1200,120,"Parle Distributor","Pune",18,"170490","2028-12-31","L2","Active"),
("890100000118","Mango Bite","Parle","Candy","5 g",1,2,1200,120,"Parle Distributor","Malegaon",18,"170490","2028-12-31","L2","Active"),
("890100000119","Kismi","Parle","Toffee","5 g",1,2,1000,100,"Parle Distributor","Nashik",18,"170490","2028-12-31","L2","Active"),
("890100000120","Eclairs","Cadbury","Candy","6 g",1,2,1000,100,"Cadbury Distributor","Nashik",18,"170490","2028-12-31","L2","Active"),
("890100000121","Poppins","Parle","Candy","20 g",8,10,400,40,"Parle Distributor","Nashik",18,"170490","2028-12-31","L3","Active"),
("890100000122","Hajmola Candy","Dabur","Candy","100 g",45,55,250,25,"Dabur Distributor","Malegaon",18,"170490","2028-12-31","L3","Active"),
("890100000123","Kaccha Mango Bite","Parle","Candy","5 g",1,2,900,90,"Parle Distributor","Pune",18,"170490","2028-12-31","L3","Active"),
("890100000124","Coffee Bite","Lotte","Candy","5 g",1,2,900,90,"Lotte India","Nashik",18,"170490","2028-12-31","L3","Active"),
("890100000125","Lacto King","Parle","Candy","5 g",1,2,900,90,"Parle Distributor","Nashik",18,"170490","2028-12-31","L3","Active"),

("890100000126","Parle-G ₹5","Parle","Biscuits","65 g",4,5,700,70,"Parle Distributor","Nashik",18,"190531","2028-12-31","L4","Active"),
("890100000127","Parle-G ₹10","Parle","Biscuits","120 g",8,10,600,60,"Parle Distributor","Malegaon",18,"190531","2028-12-31","L4","Active"),
("890100000128","Marie Gold ₹10","Britannia","Biscuits","70 g",8,10,500,50,"Britannia Distributor","Pune",18,"190531","2028-12-31","L4","Active"),
("890100000129","Good Day ₹10","Britannia","Biscuits","72 g",8,10,450,45,"Britannia Distributor","Nashik",18,"190531","2028-12-31","L4","Active"),
("890100000130","Monaco","Parle","Biscuits","75 g",9,10,450,45,"Parle Distributor","Nashik",18,"190531","2028-12-31","L4","Active"),
("890100000131","Krackjack","Parle","Biscuits","75 g",9,10,450,45,"Parle Distributor","Malegaon",18,"190531","2028-12-31","L4","Active"),
("890100000132","20-20 Cookies","Parle","Biscuits","75 g",9,10,450,45,"Parle Distributor","Pune",18,"190531","2028-12-31","L4","Active"),
("890100000133","Hide & Seek ₹10","Parle","Biscuits","82 g",9,10,400,40,"Parle Distributor","Nashik",18,"190531","2028-12-31","L5","Active"),
("890100000134","Oreo Vanilla","Cadbury","Biscuits","66 g",9,10,400,40,"Cadbury Distributor","Nashik",18,"190531","2028-12-31","L5","Active"),
("890100000135","Jim Jam","Britannia","Biscuits","75 g",9,10,350,35,"Britannia Distributor","Pune",18,"190531","2028-12-31","L5","Active"),

("890100000136","Lays Classic ₹5","Lays","Snacks","24 g",4,5,600,60,"PepsiCo","Nashik",18,"190590","2028-12-31","L6","Active"),
("890100000137","Lays Magic Masala ₹10","Lays","Snacks","52 g",9,10,500,50,"PepsiCo","Malegaon",18,"190590","2028-12-31","L6","Active"),
("890100000138","Kurkure Masala Munch","Kurkure","Snacks","34 g",4,5,600,60,"PepsiCo","Pune",18,"190590","2028-12-31","L6","Active"),
("890100000139","Kurkure Chilli Chatka","Kurkure","Snacks","34 g",4,5,600,60,"PepsiCo","Nashik",18,"190590","2028-12-31","L6","Active"),
("890100000140","Bingo Mad Angles","Bingo","Snacks","36 g",9,10,450,45,"ITC Distributor","Nashik",18,"190590","2028-12-31","L6","Active"),
("890100000141","Balaji Wafers","Balaji","Snacks","30 g",9,10,500,50,"Balaji Distributor","Malegaon",18,"190590","2028-12-31","L7","Active"),
("890100000142","Uncle Chips","Uncle Chips","Snacks","30 g",9,10,400,40,"PepsiCo","Pune",18,"190590","2028-12-31","L7","Active"),
("890100000143","Haldiram Aloo Bhujia","Haldiram","Namkeen","40 g",9,10,450,45,"Haldiram","Nashik",18,"190590","2028-12-31","L7","Active"),
("890100000144","Haldiram Moong Dal","Haldiram","Namkeen","40 g",9,10,400,40,"Haldiram","Malegaon",18,"190590","2028-12-31","L7","Active"),
("890100000145","Balaji Sev","Balaji","Namkeen","40 g",9,10,400,40,"Balaji Distributor","Pune",18,"190590","2028-12-31","L7","Active"),

("890100000146","Maggi ₹14 Pack","Maggi","Instant Food","70 g",12,14,700,70,"Nestle India","Nashik",18,"190230","2028-12-31","L8","Active"),
("890100000147","Yippee ₹10 Pack","Sunfeast","Instant Food","65 g",8,10,650,65,"ITC Distributor","Malegaon",18,"190230","2028-12-31","L8","Active"),
("890100000148","Top Ramen","Top Ramen","Instant Food","70 g",12,14,500,50,"Top Ramen","Pune",18,"190230","2028-12-31","L8","Active"),
("890100000149","Cup Noodles","Nissin","Instant Food","70 g",45,50,200,20,"Nissin Foods","Nashik",18,"190230","2028-12-31","L8","Active"),
("890100000150","Knorr Soup","Knorr","Instant Food","55 g",18,20,250,25,"HUL Distributor","Malegaon",18,"210410","2028-12-31","L8","Active"),

("890100000151","Frooti ₹10","Parle Agro","Beverages","160 ml",9,10,600,60,"Parle Agro","Nashik",12,"220299","2028-12-31","L9","Active"),
("890100000152","Maaza ₹10","Coca-Cola","Beverages","160 ml",9,10,600,60,"Coca-Cola Distributor","Malegaon",12,"220299","2028-12-31","L9","Active"),
("890100000153","Slice ₹10","Pepsi","Beverages","160 ml",9,10,550,55,"PepsiCo","Pune",12,"220299","2028-12-31","L9","Active"),
("890100000154","Appy Fizz ₹10","Parle Agro","Beverages","250 ml",9,10,500,50,"Parle Agro","Nashik",28,"220299","2028-12-31","L9","Active"),
("890100000155","Coca Cola 250ml","Coca-Cola","Soft Drinks","250 ml",18,20,400,40,"Coca-Cola Distributor","Nashik",28,"220210","2028-12-31","L10","Active"),
("890100000156","Pepsi 250ml","Pepsi","Soft Drinks","250 ml",18,20,400,40,"PepsiCo","Malegaon",28,"220210","2028-12-31","L10","Active"),
("890100000157","Sprite 250ml","Coca-Cola","Soft Drinks","250 ml",18,20,350,35,"Coca-Cola Distributor","Pune",28,"220210","2028-12-31","L10","Active"),
("890100000158","Thums Up 250ml","Coca-Cola","Soft Drinks","250 ml",18,20,350,35,"Coca-Cola Distributor","Nashik",28,"220210","2028-12-31","L10","Active"),
("890100000159","Limca 250ml","Coca-Cola","Soft Drinks","250 ml",18,20,300,30,"Coca-Cola Distributor","Malegaon",28,"220210","2028-12-31","L10","Active"),
("890100000160","Bisleri 500ml","Bisleri","Water","500 ml",9,10,800,80,"Bisleri Distributor","Nashik",18,"220110","2028-12-31","L10","Active"),

# =====================================================
# PERSONAL CARE (161–210)
# =====================================================

("890100000161","Colgate Strong Teeth","Colgate","Personal Care","20 g",9,10,500,50,"Colgate Distributor","Nashik",18,"330610","2029-12-31","M1","Active"),
("890100000162","Colgate Strong Teeth","Colgate","Personal Care","50 g",22,25,450,45,"Colgate Distributor","Malegaon",18,"330610","2029-12-31","M1","Active"),
("890100000163","Colgate MaxFresh","Colgate","Personal Care","80 g",48,55,350,35,"Colgate Distributor","Pune",18,"330610","2029-12-31","M1","Active"),
("890100000164","Pepsodent Germicheck","Pepsodent","Personal Care","40 g",18,20,450,45,"HUL Distributor","Nashik",18,"330610","2029-12-31","M1","Active"),
("890100000165","Closeup Red Hot","Closeup","Personal Care","80 g",48,55,320,30,"HUL Distributor","Malegaon",18,"330610","2029-12-31","M1","Active"),
("890100000166","Sensodyne Fresh Mint","Sensodyne","Personal Care","70 g",115,130,180,20,"GSK Distributor","Pune",18,"330610","2029-12-31","M1","Active"),

("890100000167","Clinic Plus Sachet","Clinic Plus","Personal Care","6 ml",1,2,1000,100,"HUL Distributor","Nashik",18,"330510","2029-12-31","M2","Active"),
("890100000168","Sunsilk Black Shine Sachet","Sunsilk","Personal Care","6 ml",1,2,900,90,"HUL Distributor","Malegaon",18,"330510","2029-12-31","M2","Active"),
("890100000169","Dove Sachet","Dove","Personal Care","6 ml",2,3,800,80,"HUL Distributor","Pune",18,"330510","2029-12-31","M2","Active"),
("890100000170","Head & Shoulders Sachet","P&G","Personal Care","6 ml",2,3,850,85,"P&G Distributor","Nashik",18,"330510","2029-12-31","M2","Active"),
("890100000171","Pantene Sachet","Pantene","Personal Care","6 ml",2,3,850,85,"P&G Distributor","Malegaon",18,"330510","2029-12-31","M2","Active"),
("890100000172","Clinic Plus Shampoo","Clinic Plus","Personal Care","180 ml",155,180,120,15,"HUL Distributor","Pune",18,"330510","2029-12-31","M2","Active"),

("890100000173","Lux Soap","Lux","Personal Care","100 g",34,38,350,35,"HUL Distributor","Nashik",18,"340111","2029-12-31","M3","Active"),
("890100000174","Lifebuoy Soap","Lifebuoy","Personal Care","125 g",36,40,350,35,"HUL Distributor","Malegaon",18,"340111","2029-12-31","M3","Active"),
("890100000175","Santoor Soap","Santoor","Personal Care","100 g",34,38,300,30,"Wipro Distributor","Pune",18,"340111","2029-12-31","M3","Active"),
("890100000176","Dove Soap","Dove","Personal Care","100 g",58,65,250,25,"HUL Distributor","Nashik",18,"340111","2029-12-31","M3","Active"),
("890100000177","Dettol Soap","Dettol","Personal Care","125 g",48,55,250,25,"Reckitt Distributor","Malegaon",18,"340111","2029-12-31","M3","Active"),
("890100000178","Pears Soap","Pears","Personal Care","125 g",58,65,200,20,"HUL Distributor","Pune",18,"340111","2029-12-31","M3","Active"),

("890100000179","Medimix Soap","Medimix","Personal Care","125 g",42,48,180,20,"Medimix Distributor","Nashik",18,"340111","2029-12-31","M4","Active"),
("890100000180","Cinthol Soap","Godrej","Personal Care","100 g",36,40,220,20,"Godrej Distributor","Malegaon",18,"340111","2029-12-31","M4","Active"),
("890100000181","Mysore Sandal Soap","KSDL","Personal Care","125 g",72,80,120,15,"KSDL Distributor","Pune",18,"340111","2029-12-31","M4","Active"),
("890100000182","Hamam Soap","Hamam","Personal Care","125 g",38,42,180,20,"HUL Distributor","Nashik",18,"340111","2029-12-31","M4","Active"),
("890100000183","Vivel Soap","Vivel","Personal Care","100 g",36,40,180,20,"ITC Distributor","Malegaon",18,"340111","2029-12-31","M4","Active"),
("890100000184","Fiama Soap","Fiama","Personal Care","125 g",52,58,150,15,"ITC Distributor","Pune",18,"340111","2029-12-31","M4","Active"),

("890100000185","Nivea Cream","Nivea","Personal Care","30 ml",52,60,150,15,"Nivea Distributor","Nashik",18,"330499","2029-12-31","M5","Active"),
("890100000186","Pond's Cold Cream","Pond's","Personal Care","50 g",68,75,120,15,"HUL Distributor","Malegaon",18,"330499","2029-12-31","M5","Active"),
("890100000187","Vaseline Jelly","Vaseline","Personal Care","50 ml",52,60,140,15,"HUL Distributor","Pune",18,"330499","2029-12-31","M5","Active"),
("890100000188","Boroline","Boroline","Personal Care","20 g",38,42,150,15,"Boroline Distributor","Nashik",18,"330499","2029-12-31","M5","Active"),
("890100000189","Vicco Turmeric Cream","Vicco","Personal Care","30 g",78,90,100,10,"Vicco Distributor","Malegaon",18,"330499","2029-12-31","M5","Active"),
("890100000190","Fair & Lovely","Glow & Lovely","Personal Care","25 g",58,65,120,12,"HUL Distributor","Pune",18,"330499","2029-12-31","M5","Active"),

("890100000191","Navratna Oil","Navratna","Personal Care","100 ml",82,95,120,15,"Emami Distributor","Nashik",18,"330590","2029-12-31","M6","Active"),
("890100000192","Parachute Coconut Oil","Parachute","Personal Care","100 ml",42,48,180,20,"Marico Distributor","Malegaon",18,"330590","2029-12-31","M6","Active"),
("890100000193","Bajaj Almond Drops","Bajaj","Personal Care","95 ml",88,99,120,12,"Bajaj Distributor","Pune",18,"330590","2029-12-31","M6","Active"),
("890100000194","Amla Hair Oil","Dabur","Personal Care","180 ml",92,105,100,10,"Dabur Distributor","Nashik",18,"330590","2029-12-31","M6","Active"),
("890100000195","Indulekha Hair Oil","Indulekha","Personal Care","100 ml",268,299,60,8,"HUL Distributor","Malegaon",18,"330590","2029-12-31","M6","Active"),

("890100000196","Gillette Guard Razor","Gillette","Personal Care","1 Pc",22,25,200,20,"P&G Distributor","Nashik",18,"821210","2029-12-31","M7","Active"),
("890100000197","Gillette Foam","Gillette","Personal Care","50 g",88,99,120,12,"P&G Distributor","Pune",18,"330710","2029-12-31","M7","Active"),
("890100000198","Old Spice Shaving Cream","Old Spice","Personal Care","70 g",58,65,100,10,"P&G Distributor","Malegaon",18,"330710","2029-12-31","M7","Active"),
("890100000199","Denver Deo","Denver","Personal Care","150 ml",185,210,80,8,"Denver Distributor","Nashik",18,"330720","2029-12-31","M7","Active"),
("890100000200","Fogg Deo","Fogg","Personal Care","150 ml",198,225,90,10,"Vini Distributor","Pune",18,"330720","2029-12-31","M7","Active"),

("890100000201","Engage Deo","Engage","Personal Care","150 ml",185,210,80,8,"ITC Distributor","Malegaon",18,"330720","2029-12-31","M8","Active"),
("890100000202","Wild Stone Deo","Wild Stone","Personal Care","150 ml",198,220,80,8,"McNROE","Nashik",18,"330720","2029-12-31","M8","Active"),
("890100000203","Cinthol Talc","Godrej","Personal Care","100 g",88,99,90,10,"Godrej Distributor","Pune",18,"330491","2029-12-31","M8","Active"),
("890100000204","Pond's Dreamflower Talc","Pond's","Personal Care","100 g",105,120,90,10,"HUL Distributor","Malegaon",18,"330491","2029-12-31","M8","Active"),
("890100000205","Nycil Powder","Nycil","Personal Care","100 g",115,130,80,8,"Zydus","Nashik",18,"330491","2029-12-31","M8","Active"),
("890100000206","Johnson Baby Powder","Johnson","Personal Care","100 g",138,155,80,8,"J&J Distributor","Pune",18,"330491","2029-12-31","M8","Active"),
("890100000207","Dettol Hand Wash","Dettol","Personal Care","200 ml",88,99,120,12,"Reckitt Distributor","Malegaon",18,"340130","2029-12-31","M9","Active"),
("890100000208","Lifebuoy Hand Wash","Lifebuoy","Personal Care","200 ml",82,95,120,12,"HUL Distributor","Nashik",18,"340130","2029-12-31","M9","Active"),
("890100000209","Savlon Hand Wash","Savlon","Personal Care","200 ml",85,98,100,10,"ITC Distributor","Pune",18,"340130","2029-12-31","M9","Active"),
("890100000210","Hand Sanitizer","Dettol","Personal Care","50 ml",45,50,200,20,"Reckitt Distributor","Nashik",18,"380894","2029-12-31","M9","Active"),

# =====================================================
# CLEANING & HOUSEHOLD (211–260)
# =====================================================

("890100000211","Surf Excel Easy Wash","Surf Excel","Cleaning","500 g",72,85,150,20,"HUL Distributor","Nashik",18,"340220","2029-12-31","N1","Active"),
("890100000212","Surf Excel Matic","Surf Excel","Cleaning","1 Kg",235,260,80,10,"HUL Distributor","Pune",18,"340220","2029-12-31","N1","Active"),
("890100000213","Rin Detergent Powder","Rin","Cleaning","1 Kg",82,95,140,15,"HUL Distributor","Malegaon",18,"340220","2029-12-31","N1","Active"),
("890100000214","Wheel Green","Wheel","Cleaning","1 Kg",68,78,160,20,"HUL Distributor","Nashik",18,"340220","2029-12-31","N1","Active"),
("890100000215","Ariel Detergent","Ariel","Cleaning","1 Kg",235,260,90,10,"P&G Distributor","Pune",18,"340220","2029-12-31","N1","Active"),
("890100000216","Tide Plus","Tide","Cleaning","1 Kg",135,155,120,15,"P&G Distributor","Malegaon",18,"340220","2029-12-31","N1","Active"),
("890100000217","Ghadi Detergent","Ghadi","Cleaning","1 Kg",62,72,180,20,"Ghadi Distributor","Nashik",18,"340220","2029-12-31","N1","Active"),
("890100000218","Nirma Powder","Nirma","Cleaning","1 Kg",58,68,180,20,"Nirma Distributor","Pune",18,"340220","2029-12-31","N1","Active"),
("890100000219","Vanish Stain Remover","Vanish","Cleaning","400 g",185,210,70,8,"Reckitt","Malegaon",18,"340220","2029-12-31","N2","Active"),
("890100000220","Comfort Fabric Conditioner","Comfort","Cleaning","860 ml",210,235,60,8,"HUL Distributor","Nashik",18,"340220","2029-12-31","N2","Active"),

("890100000221","Ujala Liquid","Ujala","Cleaning","75 ml",18,20,250,30,"Jyothy Labs","Nashik",18,"340220","2029-12-31","N2","Active"),
("890100000222","Vim Dishwash Bar","Vim","Cleaning","300 g",28,32,250,30,"HUL Distributor","Pune",18,"340220","2029-12-31","N2","Active"),
("890100000223","Vim Dishwash Liquid","Vim","Cleaning","500 ml",92,105,120,15,"HUL Distributor","Malegaon",18,"340220","2029-12-31","N2","Active"),
("890100000224","Exo Dishwash Bar","Exo","Cleaning","500 g",32,38,220,25,"Jyothy Labs","Nashik",18,"340220","2029-12-31","N2","Active"),
("890100000225","Pril Dishwash Liquid","Pril","Cleaning","425 ml",98,110,90,10,"Henkel","Pune",18,"340220","2029-12-31","N2","Active"),

("890100000226","Harpic Toilet Cleaner","Harpic","Cleaning","500 ml",92,105,120,15,"Reckitt","Nashik",18,"380894","2029-12-31","N3","Active"),
("890100000227","Lizol Floor Cleaner","Lizol","Cleaning","500 ml",108,120,100,12,"Reckitt","Malegaon",18,"380894","2029-12-31","N3","Active"),
("890100000228","Domex Toilet Cleaner","Domex","Cleaning","500 ml",92,105,100,12,"HUL Distributor","Pune",18,"380894","2029-12-31","N3","Active"),
("890100000229","Colin Glass Cleaner","Colin","Cleaning","500 ml",92,105,100,12,"Reckitt","Nashik",18,"340220","2029-12-31","N3","Active"),
("890100000230","Odonil Air Freshener","Odonil","Cleaning","50 g",52,60,120,15,"Dabur","Malegaon",18,"330749","2029-12-31","N3","Active"),

("890100000231","Good Knight Refill","Good Knight","Cleaning","45 ml",78,90,100,12,"Godrej","Nashik",18,"380891","2029-12-31","N4","Active"),
("890100000232","Good Knight Machine","Good Knight","Cleaning","1 Pc",78,90,80,10,"Godrej","Pune",18,"380891","2029-12-31","N4","Active"),
("890100000233","All Out Refill","All Out","Cleaning","45 ml",82,95,100,12,"SC Johnson","Malegaon",18,"380891","2029-12-31","N4","Active"),
("890100000234","All Out Machine","All Out","Cleaning","1 Pc",82,95,80,10,"SC Johnson","Nashik",18,"380891","2029-12-31","N4","Active"),
("890100000235","Hit Red Spray","Hit","Cleaning","400 ml",165,185,80,10,"Godrej","Pune",18,"380891","2029-12-31","N4","Active"),

("890100000236","Hit Black Spray","Hit","Cleaning","400 ml",168,190,80,10,"Godrej","Malegaon",18,"380891","2029-12-31","N4","Active"),
("890100000237","Match Box","Ship","Household","10 Sticks",2,3,1000,100,"Local Supplier","Nashik",18,"360500","2029-12-31","N5","Active"),
("890100000238","Cycle Agarbatti","Cycle","Household","100 Sticks",42,48,180,20,"Cycle Distributor","Pune",18,"330741","2029-12-31","N5","Active"),
("890100000239","Mangaldeep Agarbatti","Mangaldeep","Household","100 Sticks",38,45,180,20,"ITC","Malegaon",18,"330741","2029-12-31","N5","Active"),
("890100000240","Wax Candle","Local","Household","6 Pc",28,35,150,20,"Local Supplier","Nashik",18,"340600","2029-12-31","N5","Active"),

("890100000241","Garbage Bags","Clean Plus","Household","30 Pc",58,68,120,15,"Clean Distributor","Pune",18,"392321","2029-12-31","N6","Active"),
("890100000242","Aluminium Foil","FreshWrap","Household","9 m",95,110,100,12,"FreshWrap","Malegaon",18,"760711","2029-12-31","N6","Active"),
("890100000243","Cling Film","FreshWrap","Household","20 m",78,90,90,10,"FreshWrap","Nashik",18,"392043","2029-12-31","N6","Active"),
("890100000244","Paper Napkins","Origami","Household","100 Pc",62,70,120,15,"Origami","Pune",18,"481830","2029-12-31","N6","Active"),
("890100000245","Kitchen Tissue","Origami","Household","2 Roll",98,110,100,12,"Origami","Malegaon",18,"481820","2029-12-31","N6","Active"),

("890100000246","Toilet Paper","Origami","Household","4 Roll",145,165,70,8,"Origami","Nashik",18,"481810","2029-12-31","N7","Active"),
("890100000247","Scrub Pad","Scotch Brite","Household","3 Pc",48,55,150,15,"3M","Pune",18,"680530","2029-12-31","N7","Active"),
("890100000248","Steel Scrubber","Scotch Brite","Household","2 Pc",42,48,140,15,"3M","Malegaon",18,"732310","2029-12-31","N7","Active"),
("890100000249","Cleaning Cloth","Local","Household","1 Pc",28,35,200,20,"Local Supplier","Nashik",18,"630710","2029-12-31","N7","Active"),
("890100000250","Floor Wiper","Supreme","Household","1 Pc",135,155,60,8,"Supreme","Pune",18,"960390","2029-12-31","N7","Active"),

("890100000251","Plastic Bucket","Supreme","Household","15 L",285,320,50,8,"Supreme","Malegaon",18,"392490","2029-12-31","N8","Active"),
("890100000252","Plastic Mug","Supreme","Household","1 Pc",68,80,120,15,"Supreme","Nashik",18,"392490","2029-12-31","N8","Active"),
("890100000253","Broom","Local","Household","1 Pc",95,110,100,12,"Local Supplier","Pune",18,"960390","2029-12-31","N8","Active"),
("890100000254","Floor Mop","Spotzero","Household","1 Pc",385,430,40,5,"Spotzero","Malegaon",18,"960390","2029-12-31","N8","Active"),
("890100000255","Dustbin","Supreme","Household","20 L",265,295,40,5,"Supreme","Nashik",18,"392490","2029-12-31","N8","Active"),

("890100000256","Plastic Storage Box","Cello","Household","10 L",295,340,50,5,"Cello","Pune",18,"392310","2029-12-31","N9","Active"),
("890100000257","Clothes Clips","Local","Household","24 Pc",28,35,150,15,"Local Supplier","Malegaon",18,"392690","2029-12-31","N9","Active"),
("890100000258","Rope Nylon","Local","Household","10 m",48,58,120,12,"Local Supplier","Nashik",18,"560750","2029-12-31","N9","Active"),
("890100000259","Mosquito Coil","Good Knight","Household","10 Pc",42,48,150,15,"Godrej","Pune",18,"380891","2029-12-31","N9","Active"),
("890100000260","Camphor Tablets","Mangalam","Household","100 g",58,68,120,12,"Mangalam","Malegaon",18,"291429","2029-12-31","N9","Active"),

# =====================================================
# DRY FRUITS + CHOCOLATES + SOFT DRINKS + SAUCES + BABY CARE (261–310)
# =====================================================

("890100000261","Almond Premium","Nutraj","Dry Fruits","500 g",485,550,60,8,"Dry Fruit World","Nashik",5,"080212","2029-12-31","O1","Active"),
("890100000262","Cashew W320","Nutraj","Dry Fruits","500 g",565,640,50,8,"Dry Fruit World","Pune",5,"080132","2029-12-31","O1","Active"),
("890100000263","Raisins Premium","Nutraj","Dry Fruits","500 g",245,280,80,10,"Dry Fruit World","Malegaon",5,"080620","2029-12-31","O1","Active"),
("890100000264","Pistachio","Nutraj","Dry Fruits","250 g",365,420,40,5,"Dry Fruit World","Nashik",5,"080251","2029-12-31","O1","Active"),
("890100000265","Walnuts","Nutraj","Dry Fruits","250 g",345,390,35,5,"Dry Fruit World","Pune",5,"080232","2029-12-31","O1","Active"),
("890100000266","Dates Premium","Lion","Dry Fruits","500 g",185,220,70,10,"Dry Fruit World","Malegaon",5,"080410","2029-12-31","O1","Active"),
("890100000267","Anjeer","Nutraj","Dry Fruits","250 g",325,370,40,5,"Dry Fruit World","Nashik",5,"080420","2029-12-31","O2","Active"),
("890100000268","Mixed Dry Fruits","Nutraj","Dry Fruits","500 g",645,720,30,5,"Dry Fruit World","Pune",5,"081350","2029-12-31","O2","Active"),
("890100000269","Pumpkin Seeds","True Elements","Dry Fruits","200 g",225,260,40,5,"Healthy Foods","Nashik",5,"120799","2029-12-31","O2","Active"),
("890100000270","Sunflower Seeds","True Elements","Dry Fruits","200 g",165,190,40,5,"Healthy Foods","Malegaon",5,"120600","2029-12-31","O2","Active"),

("890100000271","Cadbury Dairy Milk","Cadbury","Chocolate","52 g",42,50,250,30,"Cadbury Distributor","Nashik",18,"180690","2029-12-31","O3","Active"),
("890100000272","Cadbury Silk","Cadbury","Chocolate","150 g",165,185,120,15,"Cadbury Distributor","Pune",18,"180690","2029-12-31","O3","Active"),
("890100000273","5 Star","Cadbury","Chocolate","40 g",18,20,350,40,"Cadbury Distributor","Malegaon",18,"180690","2029-12-31","O3","Active"),
("890100000274","Perk","Cadbury","Chocolate","35 g",10,10,400,50,"Cadbury Distributor","Nashik",18,"180690","2029-12-31","O3","Active"),
("890100000275","Munch","Nestle","Chocolate","32 g",10,10,400,50,"Nestle India","Pune",18,"180690","2029-12-31","O3","Active"),
("890100000276","KitKat","Nestle","Chocolate","37 g",20,20,350,40,"Nestle India","Malegaon",18,"180690","2029-12-31","O3","Active"),
("890100000277","Gems","Cadbury","Chocolate","30 g",10,10,300,40,"Cadbury Distributor","Nashik",18,"180690","2029-12-31","O4","Active"),
("890100000278","Ferrero Rocher","Ferrero","Chocolate","16 Pc",425,480,30,5,"Premium Foods","Pune",18,"180690","2029-12-31","O4","Active"),
("890100000279","Snickers","Mars","Chocolate","45 g",48,55,150,20,"Mars India","Malegaon",18,"180690","2029-12-31","O4","Active"),
("890100000280","Bounty","Mars","Chocolate","57 g",58,65,120,15,"Mars India","Nashik",18,"180690","2029-12-31","O4","Active"),

("890100000281","Coca Cola","Coca Cola","Soft Drinks","750 ml",38,40,180,20,"Coca Cola","Nashik",28,"220210","2029-12-31","O5","Active"),
("890100000282","Pepsi","Pepsi","Soft Drinks","750 ml",38,40,180,20,"PepsiCo","Pune",28,"220210","2029-12-31","O5","Active"),
("890100000283","Sprite","Coca Cola","Soft Drinks","750 ml",38,40,180,20,"Coca Cola","Malegaon",28,"220210","2029-12-31","O5","Active"),
("890100000284","Fanta","Coca Cola","Soft Drinks","750 ml",38,40,180,20,"Coca Cola","Nashik",28,"220210","2029-12-31","O5","Active"),
("890100000285","Limca","Coca Cola","Soft Drinks","750 ml",38,40,180,20,"Coca Cola","Pune",28,"220210","2029-12-31","O5","Active"),
("890100000286","7UP","PepsiCo","Soft Drinks","750 ml",38,40,180,20,"PepsiCo","Malegaon",28,"220210","2029-12-31","O5","Active"),
("890100000287","Mountain Dew","PepsiCo","Soft Drinks","750 ml",38,40,180,20,"PepsiCo","Nashik",28,"220210","2029-12-31","O6","Active"),
("890100000288","Sting Energy Drink","PepsiCo","Soft Drinks","250 ml",18,20,250,30,"PepsiCo","Pune",28,"220299","2029-12-31","O6","Active"),
("890100000289","Red Bull","Red Bull","Soft Drinks","250 ml",115,125,80,10,"Red Bull","Malegaon",28,"220299","2029-12-31","O6","Active"),
("890100000290","Monster Energy","Monster","Soft Drinks","350 ml",125,140,60,8,"Monster","Nashik",28,"220299","2029-12-31","O6","Active"),

("890100000291","Kissan Tomato Ketchup","Kissan","Sauces","950 g",135,150,100,12,"HUL Distributor","Nashik",12,"210320","2029-12-31","O7","Active"),
("890100000292","Maggi Tomato Ketchup","Maggi","Sauces","1 Kg",145,160,90,10,"Nestle India","Pune",12,"210320","2029-12-31","O7","Active"),
("890100000293","Ching's Green Chilli Sauce","Ching's","Sauces","680 g",105,120,80,10,"Capital Foods","Malegaon",12,"210390","2029-12-31","O7","Active"),
("890100000294","Veeba Mayonnaise","Veeba","Sauces","875 g",165,185,70,8,"Veeba","Nashik",12,"210390","2029-12-31","O7","Active"),
("890100000295","Soy Sauce","Ching's","Sauces","200 ml",78,90,80,10,"Capital Foods","Pune",12,"210390","2029-12-31","O7","Active"),

("890100000296","Johnson Baby Soap","Johnson","Baby Care","75 g",58,65,150,20,"J&J","Nashik",12,"340111","2029-12-31","O8","Active"),
("890100000297","Johnson Baby Powder","Johnson","Baby Care","100 g",125,140,120,15,"J&J","Pune",12,"330491","2029-12-31","O8","Active"),
("890100000298","Johnson Baby Oil","Johnson","Baby Care","100 ml",145,165,100,12,"J&J","Malegaon",12,"330499","2029-12-31","O8","Active"),
("890100000299","Johnson Baby Shampoo","Johnson","Baby Care","100 ml",155,175,90,10,"J&J","Nashik",12,"330510","2029-12-31","O8","Active"),
("890100000300","Himalaya Baby Lotion","Himalaya","Baby Care","100 ml",165,185,80,10,"Himalaya","Pune",12,"330499","2029-12-31","O8","Active"),

("890100000301","Pampers Small","Pampers","Baby Care","10 Pc",115,130,120,15,"P&G","Malegaon",12,"961900","2029-12-31","O9","Active"),
("890100000302","Pampers Medium","Pampers","Baby Care","10 Pc",125,140,120,15,"P&G","Nashik",12,"961900","2029-12-31","O9","Active"),
("890100000303","MamyPoko Pants","MamyPoko","Baby Care","10 Pc",118,135,120,15,"Unicharm","Pune",12,"961900","2029-12-31","O9","Active"),
("890100000304","Cerelac Wheat","Nestle","Baby Care","300 g",245,270,70,10,"Nestle India","Malegaon",18,"190110","2029-12-31","O9","Active"),
("890100000305","Cerelac Rice","Nestle","Baby Care","300 g",245,270,70,10,"Nestle India","Nashik",18,"190110","2029-12-31","O9","Active"),
("890100000306","Lactogen Stage 1","Nestle","Baby Care","400 g",385,430,50,8,"Nestle India","Pune",18,"190110","2029-12-31","O10","Active"),
("890100000307","Nan Pro 1","Nestle","Baby Care","400 g",725,790,30,5,"Nestle India","Malegaon",18,"190110","2029-12-31","O10","Active"),
("890100000308","Farex","Farex","Baby Care","300 g",265,295,60,8,"Farex","Nashik",18,"190110","2029-12-31","O10","Active"),
("890100000309","Baby Wipes","Johnson","Baby Care","72 Wipes",165,185,80,10,"J&J","Pune",12,"340119","2029-12-31","O10","Active"),
("890100000310","Baby Feeding Bottle","Pigeon","Baby Care","250 ml",245,275,50,8,"Pigeon","Malegaon",18,"392330","2029-12-31","O10","Active"),

]
cursor.executemany("""
INSERT OR IGNORE INTO products(
barcode,
product_name,
brand,
category,
unit,
purchase_price,
selling_price,
stock,
min_stock,
supplier,
market,
gst,
hsn_code,
expiry_date,
rack_no,
status
)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
""", products)

conn.commit()
conn.close()

print("Products Inserted Successfully!")