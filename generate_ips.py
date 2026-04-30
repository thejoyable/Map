"""
Script to add real-world IP addresses to the test_data.csv
This creates a new file: test_data_with_ips.csv
"""

import pandas as pd
import random

# Real-world IP addresses mapped to actual locations (land areas only)
REAL_WORLD_IPS = [
# ── North America ──────────────────────────────────────────────────────
{"src_ip": "8.8.8.8",           "dst_ip": "1.1.1.1",           "src_lat": 37.7749, "src_lon": -122.4194, "dst_lat": 34.0522,  "dst_lon": -118.2437, "src_city": "San Francisco",  "dst_city": "Los Angeles"},
{"src_ip": "142.250.185.46",    "dst_ip": "13.107.42.14",      "src_lat": 40.7128, "src_lon": -74.0060,  "dst_lat": 47.6062,  "dst_lon": -122.3321, "src_city": "New York",        "dst_city": "Seattle"},
{"src_ip": "151.101.1.140",     "dst_ip": "104.16.132.229",    "src_lat": 41.8781, "src_lon": -87.6298,  "dst_lat": 33.4484,  "dst_lon": -112.0740, "src_city": "Chicago",         "dst_city": "Phoenix"},
{"src_ip": "172.217.14.206",    "dst_ip": "23.185.0.2",        "src_lat": 29.7604, "src_lon": -95.3698,  "dst_lat": 25.7617,  "dst_lon": -80.1918,  "src_city": "Houston",         "dst_city": "Miami"},
{"src_ip": "205.251.242.103",   "dst_ip": "192.30.255.112",    "src_lat": 43.6532, "src_lon": -79.3832,  "dst_lat": 49.2827,  "dst_lon": -123.1207, "src_city": "Toronto",         "dst_city": "Vancouver"},
{"src_ip": "54.239.28.85",      "dst_ip": "104.244.42.65",     "src_lat": 39.9526, "src_lon": -75.1652,  "dst_lat": 30.2672,  "dst_lon": -97.7431,  "src_city": "Philadelphia",    "dst_city": "Austin"},
{"src_ip": "198.41.0.4",        "dst_ip": "8.26.56.26",        "src_lat": 32.7767, "src_lon": -96.7970,  "dst_lat": 33.7490,  "dst_lon": -84.3880,  "src_city": "Dallas",          "dst_city": "Atlanta"},
{"src_ip": "68.87.76.178",      "dst_ip": "72.21.91.8",        "src_lat": 42.3601, "src_lon": -71.0589,  "dst_lat": 39.7392,  "dst_lon": -104.9903, "src_city": "Boston",          "dst_city": "Denver"},
{"src_ip": "209.51.188.17",     "dst_ip": "69.171.224.11",     "src_lat": 36.1699, "src_lon": -115.1398, "dst_lat": 38.9072,  "dst_lon": -77.0369,  "src_city": "Las Vegas",       "dst_city": "Washington DC"},
{"src_ip": "206.81.0.1",        "dst_ip": "204.13.164.1",      "src_lat": 45.5017, "src_lon": -73.5673,  "dst_lat": 51.0447,  "dst_lon": -114.0719, "src_city": "Montreal",        "dst_city": "Calgary"},
{"src_ip": "96.7.128.175",      "dst_ip": "200.33.224.1",      "src_lat": 19.4326, "src_lon": -99.1332,  "dst_lat": 20.9674,  "dst_lon": -89.5926,  "src_city": "Mexico City",     "dst_city": "Merida"},
{"src_ip": "73.109.57.1",       "dst_ip": "66.163.168.1",      "src_lat": 45.5051, "src_lon": -122.6750, "dst_lat": 39.0997,  "dst_lon": -94.5786,  "src_city": "Portland",        "dst_city": "Kansas City"},
{"src_ip": "198.60.22.1",       "dst_ip": "65.182.64.1",       "src_lat": 40.7608, "src_lon": -111.8910, "dst_lat": 29.9511,  "dst_lon": -90.0715,  "src_city": "Salt Lake City",  "dst_city": "New Orleans"},
{"src_ip": "68.39.160.1",       "dst_ip": "66.235.128.1",      "src_lat": 42.3314, "src_lon": -83.0458,  "dst_lat": 32.7157,  "dst_lon": -117.1611, "src_city": "Detroit",         "dst_city": "San Diego"},
{"src_ip": "68.144.208.1",      "dst_ip": "64.247.109.1",      "src_lat": 30.3322, "src_lon": -81.6557,  "dst_lat": 35.1495,  "dst_lon": -90.0490,  "src_city": "Jacksonville",    "dst_city": "Memphis"},
{"src_ip": "149.154.167.51",    "dst_ip": "198.35.26.96",      "src_lat": 44.9778, "src_lon": -93.2650,  "dst_lat": 47.5615,  "dst_lon": -52.7126,  "src_city": "Minneapolis",     "dst_city": "St. John's"},
{"src_ip": "198.161.1.1",       "dst_ip": "66.183.128.1",      "src_lat": 53.5461, "src_lon": -113.4938, "dst_lat": 49.8951,  "dst_lon": -97.1384,  "src_city": "Edmonton",        "dst_city": "Winnipeg"},
{"src_ip": "74.63.192.1",       "dst_ip": "186.21.64.1",       "src_lat": 46.8139, "src_lon": -71.2082,  "dst_lat":  9.9281,  "dst_lon": -84.0907,  "src_city": "Quebec City",     "dst_city": "San José"},
{"src_ip": "190.111.1.1",       "dst_ip": "190.23.0.1",        "src_lat": 14.6349, "src_lon": -90.5069,  "dst_lat": 12.1328,  "dst_lon": -86.2504,  "src_city": "Guatemala City",  "dst_city": "Managua"},
{"src_ip": "190.38.64.1",       "dst_ip": "200.69.224.1",      "src_lat": 13.6929, "src_lon": -89.2182,  "dst_lat":  8.9936,  "dst_lon": -79.5197,  "src_city": "San Salvador",    "dst_city": "Panama City"},
{"src_ip": "72.36.148.1",       "dst_ip": "190.214.135.59",    "src_lat": 17.9970, "src_lon": -76.7936,  "dst_lat": 10.4806,  "dst_lon": -66.9036,  "src_city": "Kingston",        "dst_city": "Caracas"},

# ── Europe ─────────────────────────────────────────────────────────────
{"src_ip": "185.60.216.35",     "dst_ip": "195.154.122.113",   "src_lat": 51.5074, "src_lon":  -0.1278,  "dst_lat": 48.8566,  "dst_lon":   2.3522,  "src_city": "London",          "dst_city": "Paris"},
{"src_ip": "46.4.105.116",      "dst_ip": "217.160.0.187",     "src_lat": 52.5200, "src_lon":  13.4050,  "dst_lat": 41.9028,  "dst_lon":  12.4964,  "src_city": "Berlin",          "dst_city": "Rome"},
{"src_ip": "91.198.174.192",    "dst_ip": "185.15.59.224",     "src_lat": 40.4168, "src_lon":  -3.7038,  "dst_lat": 52.3676,  "dst_lon":   4.9041,  "src_city": "Madrid",          "dst_city": "Amsterdam"},
{"src_ip": "194.150.245.142",   "dst_ip": "213.180.193.3",     "src_lat": 59.3293, "src_lon":  18.0686,  "dst_lat": 55.7558,  "dst_lon":  37.6173,  "src_city": "Stockholm",       "dst_city": "Moscow"},
{"src_ip": "77.109.128.1",      "dst_ip": "178.254.3.1",       "src_lat": 47.3769, "src_lon":   8.5417,  "dst_lat": 48.2082,  "dst_lon":  16.3738,  "src_city": "Zurich",          "dst_city": "Vienna"},
{"src_ip": "89.207.132.170",    "dst_ip": "185.83.216.1",      "src_lat": 50.0755, "src_lon":  14.4378,  "dst_lat": 52.2297,  "dst_lon":  21.0122,  "src_city": "Prague",          "dst_city": "Warsaw"},
{"src_ip": "88.84.209.116",     "dst_ip": "213.251.173.1",     "src_lat": 47.4979, "src_lon":  19.0402,  "dst_lat": 45.4654,  "dst_lon":   9.1859,  "src_city": "Budapest",        "dst_city": "Milan"},
{"src_ip": "194.97.97.97",      "dst_ip": "84.22.100.108",     "src_lat": 59.4370, "src_lon":  24.7536,  "dst_lat": 60.1699,  "dst_lon":  24.9384,  "src_city": "Tallinn",         "dst_city": "Helsinki"},
{"src_ip": "195.43.85.53",      "dst_ip": "178.63.20.83",      "src_lat": 55.6761, "src_lon":  12.5683,  "dst_lat": 53.3498,  "dst_lon":  -6.2603,  "src_city": "Copenhagen",      "dst_city": "Dublin"},
{"src_ip": "5.45.96.220",       "dst_ip": "213.152.176.1",     "src_lat": 50.4501, "src_lon":  30.5234,  "dst_lat": 41.6938,  "dst_lon":  44.8015,  "src_city": "Kyiv",            "dst_city": "Tbilisi"},
{"src_ip": "217.12.208.1",      "dst_ip": "195.10.210.1",      "src_lat": 38.7169, "src_lon":  -9.1399,  "dst_lat": 50.8503,  "dst_lon":   4.3517,  "src_city": "Lisbon",          "dst_city": "Brussels"},
{"src_ip": "213.215.0.1",       "dst_ip": "213.229.192.1",     "src_lat": 48.1486, "src_lon":  17.1077,  "dst_lat": 46.0569,  "dst_lon":  14.5058,  "src_city": "Bratislava",      "dst_city": "Ljubljana"},
{"src_ip": "193.198.224.1",     "dst_ip": "188.93.16.1",       "src_lat": 45.8150, "src_lon":  15.9819,  "dst_lat": 44.8176,  "dst_lon":  20.4633,  "src_city": "Zagreb",          "dst_city": "Belgrade"},
{"src_ip": "62.108.32.1",       "dst_ip": "213.108.105.1",     "src_lat": 37.9755, "src_lon":  23.7348,  "dst_lat": 42.6977,  "dst_lon":  23.3219,  "src_city": "Athens",          "dst_city": "Sofia"},
{"src_ip": "82.148.64.1",       "dst_ip": "213.226.178.1",     "src_lat": 64.1466, "src_lon": -21.9426,  "dst_lat": 35.8997,  "dst_lon":  14.5147,  "src_city": "Reykjavik",       "dst_city": "Valletta"},
{"src_ip": "178.172.0.1",       "dst_ip": "213.219.128.1",     "src_lat": 53.9045, "src_lon":  27.5615,  "dst_lat": 56.9460,  "dst_lon":  24.1059,  "src_city": "Minsk",           "dst_city": "Riga"},
{"src_ip": "78.56.0.1",         "dst_ip": "37.221.128.1",      "src_lat": 54.6872, "src_lon":  25.2797,  "dst_lat": 47.0105,  "dst_lon":  28.8638,  "src_city": "Vilnius",         "dst_city": "Chisinau"},
{"src_ip": "212.34.0.1",        "dst_ip": "5.62.0.1",          "src_lat": 40.1872, "src_lon":  44.5152,  "dst_lat": 40.4093,  "dst_lon":  49.8671,  "src_city": "Yerevan",         "dst_city": "Baku"},
{"src_ip": "83.97.20.34",       "dst_ip": "95.172.88.1",       "src_lat": 41.3275, "src_lon":  19.8187,  "dst_lat": 43.8563,  "dst_lon":  18.4131,  "src_city": "Tirana",          "dst_city": "Sarajevo"},
{"src_ip": "77.28.0.1",         "dst_ip": "91.148.0.1",        "src_lat": 42.6629, "src_lon":  21.1655,  "dst_lat": 42.4304,  "dst_lon":  19.2594,  "src_city": "Pristina",        "dst_city": "Podgorica"},

# ── Asia ────────────────────────────────────────────────────────────────
{"src_ip": "202.12.27.33",      "dst_ip": "103.28.248.1",      "src_lat": 35.6762, "src_lon": 139.6503,  "dst_lat": 37.5665,  "dst_lon": 126.9780,  "src_city": "Tokyo",           "dst_city": "Seoul"},
{"src_ip": "61.135.169.125",    "dst_ip": "180.149.132.47",    "src_lat": 39.9042, "src_lon": 116.4074,  "dst_lat": 31.2304,  "dst_lon": 121.4737,  "src_city": "Beijing",         "dst_city": "Shanghai"},
{"src_ip": "103.21.244.0",      "dst_ip": "182.50.132.242",    "src_lat": 28.7041, "src_lon":  77.1025,  "dst_lat": 19.0760,  "dst_lon":  72.8777,  "src_city": "New Delhi",       "dst_city": "Mumbai"},
{"src_ip": "202.65.115.242",    "dst_ip": "103.10.28.61",      "src_lat":  1.3521, "src_lon": 103.8198,  "dst_lat": 13.7563,  "dst_lon": 100.5018,  "src_city": "Singapore",       "dst_city": "Bangkok"},
{"src_ip": "114.111.167.14",    "dst_ip": "203.104.144.75",    "src_lat": 22.3193, "src_lon": 114.1694,  "dst_lat": -6.2088,  "dst_lon": 106.8456,  "src_city": "Hong Kong",       "dst_city": "Jakarta"},
{"src_ip": "202.150.221.20",    "dst_ip": "203.162.2.1",       "src_lat": 21.0285, "src_lon": 105.8542,  "dst_lat": 10.8231,  "dst_lon": 106.6297,  "src_city": "Hanoi",           "dst_city": "Ho Chi Minh City"},
{"src_ip": "121.54.32.1",       "dst_ip": "202.8.75.1",        "src_lat": 14.5995, "src_lon": 120.9842,  "dst_lat":  3.1390,  "dst_lon": 101.6869,  "src_city": "Manila",          "dst_city": "Kuala Lumpur"},
{"src_ip": "202.56.250.1",      "dst_ip": "202.125.128.1",     "src_lat": 23.7275, "src_lon":  90.3945,  "dst_lat": 24.8607,  "dst_lon":  67.0011,  "src_city": "Dhaka",           "dst_city": "Karachi"},
{"src_ip": "91.212.10.1",       "dst_ip": "5.21.0.1",          "src_lat": 35.6892, "src_lon":  51.3890,  "dst_lat": 33.3128,  "dst_lon":  44.3615,  "src_city": "Tehran",          "dst_city": "Baghdad"},
{"src_ip": "43.250.192.1",      "dst_ip": "14.139.223.1",      "src_lat": 17.3850, "src_lon":  78.4867,  "dst_lat": 12.9716,  "dst_lon":  77.5946,  "src_city": "Hyderabad",       "dst_city": "Bengaluru"},
{"src_ip": "43.231.244.1",      "dst_ip": "202.53.94.1",       "src_lat": 13.0827, "src_lon":  80.2707,  "dst_lat": 22.5726,  "dst_lon":  88.3639,  "src_city": "Chennai",         "dst_city": "Kolkata"},
{"src_ip": "36.255.68.1",       "dst_ip": "203.81.89.1",       "src_lat": 27.7172, "src_lon":  85.3240,  "dst_lat":  6.9271,  "dst_lon":  79.8612,  "src_city": "Kathmandu",       "dst_city": "Colombo"},
{"src_ip": "202.84.252.1",      "dst_ip": "195.20.0.1",        "src_lat": 43.2220, "src_lon":  76.8512,  "dst_lat": 41.2995,  "dst_lon":  69.2401,  "src_city": "Almaty",          "dst_city": "Tashkent"},
{"src_ip": "210.125.163.1",     "dst_ip": "58.253.9.1",        "src_lat": 47.9077, "src_lon": 106.8832,  "dst_lat": 22.2855,  "dst_lon": 114.1577,  "src_city": "Ulaanbaatar",     "dst_city": "Shenzhen"},
{"src_ip": "103.253.88.1",      "dst_ip": "210.145.99.1",      "src_lat": 25.0330, "src_lon": 121.5654,  "dst_lat": 34.6937,  "dst_lon": 135.5023,  "src_city": "Taipei",          "dst_city": "Osaka"},
{"src_ip": "183.252.0.1",       "dst_ip": "117.136.0.1",       "src_lat": 30.5728, "src_lon": 104.0668,  "dst_lat": 30.5928,  "dst_lon": 114.3055,  "src_city": "Chengdu",         "dst_city": "Wuhan"},
{"src_ip": "119.147.0.1",       "dst_ip": "113.200.0.1",       "src_lat": 23.1291, "src_lon": 113.2644,  "dst_lat": 29.4316,  "dst_lon": 106.9123,  "src_city": "Guangzhou",       "dst_city": "Chongqing"},
{"src_ip": "115.240.0.1",       "dst_ip": "117.99.0.1",        "src_lat": 18.5204, "src_lon":  73.8567,  "dst_lat": 26.9124,  "dst_lon":  75.7873,  "src_city": "Pune",            "dst_city": "Jaipur"},
{"src_ip": "202.83.24.1",       "dst_ip": "193.29.55.1",       "src_lat": 31.5497, "src_lon":  74.3436,  "dst_lat": 34.5553,  "dst_lon":  69.2075,  "src_city": "Lahore",          "dst_city": "Kabul"},
{"src_ip": "163.180.103.1",     "dst_ip": "112.213.89.1",      "src_lat": 35.1796, "src_lon": 129.0756,  "dst_lat": 16.8661,  "dst_lon":  96.1951,  "src_city": "Busan",           "dst_city": "Yangon"},
{"src_ip": "203.144.0.1",       "dst_ip": "123.26.0.1",        "src_lat": 11.5625, "src_lon": 104.9160,  "dst_lat": 17.9757,  "dst_lon": 102.6331,  "src_city": "Phnom Penh",      "dst_city": "Vientiane"},

# ── Middle East ──────────────────────────────────────────────────────────
{"src_ip": "185.125.190.36",    "dst_ip": "213.42.20.19",      "src_lat": 25.2048, "src_lon":  55.2708,  "dst_lat": 31.7683,  "dst_lon":  35.2137,  "src_city": "Dubai",           "dst_city": "Jerusalem"},
{"src_ip": "37.48.64.150",      "dst_ip": "5.63.13.202",       "src_lat": 33.8886, "src_lon":  35.4955,  "dst_lat": 41.0082,  "dst_lon":  28.9784,  "src_city": "Beirut",          "dst_city": "Istanbul"},
{"src_ip": "46.30.160.1",       "dst_ip": "94.101.192.1",      "src_lat": 24.7136, "src_lon":  46.6753,  "dst_lat": 23.6850,  "dst_lon":  58.1829,  "src_city": "Riyadh",          "dst_city": "Muscat"},
{"src_ip": "185.90.56.1",       "dst_ip": "212.117.128.1",     "src_lat": 25.2854, "src_lon":  51.5310,  "dst_lat": 24.4539,  "dst_lon":  54.3773,  "src_city": "Doha",            "dst_city": "Abu Dhabi"},
{"src_ip": "37.34.0.1",         "dst_ip": "82.176.0.1",        "src_lat": 31.9554, "src_lon":  35.9451,  "dst_lat": 29.3759,  "dst_lon":  47.9774,  "src_city": "Amman",           "dst_city": "Kuwait City"},
{"src_ip": "31.22.0.1",         "dst_ip": "62.235.200.1",      "src_lat": 35.1856, "src_lon":  33.3823,  "dst_lat": 33.5138,  "dst_lon":  36.2765,  "src_city": "Nicosia",         "dst_city": "Damascus"},
{"src_ip": "5.100.0.1",         "dst_ip": "134.35.0.1",        "src_lat": 15.5527, "src_lon":  32.5324,  "dst_lat": 15.3694,  "dst_lon":  44.1910,  "src_city": "Khartoum",        "dst_city": "Sana'a"},
{"src_ip": "212.153.0.1",       "dst_ip": "5.44.168.1",        "src_lat": 26.2235, "src_lon":  50.5876,  "dst_lat": 32.0853,  "dst_lon":  34.7818,  "src_city": "Manama",          "dst_city": "Tel Aviv"},

# ── South America ───────────────────────────────────────────────────────
{"src_ip": "200.221.11.100",    "dst_ip": "186.148.177.20",    "src_lat": -23.5505, "src_lon": -46.6333, "dst_lat": -34.6037, "dst_lon": -58.3816,  "src_city": "São Paulo",       "dst_city": "Buenos Aires"},
{"src_ip": "190.98.248.254",    "dst_ip": "181.225.253.186",   "src_lat":   4.7110, "src_lon": -74.0721, "dst_lat": -12.0464, "dst_lon": -77.0428,  "src_city": "Bogotá",          "dst_city": "Lima"},
{"src_ip": "200.10.60.1",       "dst_ip": "186.10.48.1",       "src_lat": -15.8267, "src_lon": -47.9218, "dst_lat": -33.4489, "dst_lon": -70.6693,  "src_city": "Brasília",        "dst_city": "Santiago"},
{"src_ip": "186.155.8.1",       "dst_ip": "200.195.139.1",     "src_lat":  -0.1807, "src_lon": -78.4678, "dst_lat":  -8.0476, "dst_lon": -34.8770,  "src_city": "Quito",           "dst_city": "Recife"},
{"src_ip": "190.6.64.1",        "dst_ip": "200.40.30.245",     "src_lat": -25.2867, "src_lon": -57.6470, "dst_lat": -34.9011, "dst_lon": -56.1645,  "src_city": "Asunción",        "dst_city": "Montevideo"},
{"src_ip": "200.105.141.1",     "dst_ip": "190.214.135.59",    "src_lat": -17.7833, "src_lon": -63.1821, "dst_lat":  10.4806, "dst_lon": -66.9036,  "src_city": "Santa Cruz",      "dst_city": "Caracas"},
{"src_ip": "200.24.128.1",      "dst_ip": "186.64.112.1",      "src_lat":   3.8667, "src_lon": -67.9000, "dst_lat":   3.4372, "dst_lon": -76.5225,  "src_city": "Puerto Ayacucho", "dst_city": "Cali"},
{"src_ip": "190.15.128.1",      "dst_ip": "190.122.64.1",      "src_lat":  -8.1116, "src_lon": -79.0291, "dst_lat": -16.3989, "dst_lon": -71.5350,  "src_city": "Trujillo",        "dst_city": "Arequipa"},

# ── Africa ──────────────────────────────────────────────────────────────
{"src_ip": "197.242.150.244",   "dst_ip": "41.190.232.52",     "src_lat": -26.2041, "src_lon":  28.0473, "dst_lat":  -1.2921, "dst_lon":  36.8219,  "src_city": "Johannesburg",    "dst_city": "Nairobi"},
{"src_ip": "105.235.130.54",    "dst_ip": "154.73.220.137",    "src_lat": -33.9249, "src_lon":  18.4241, "dst_lat":   6.5244, "dst_lon":   3.3792,  "src_city": "Cape Town",       "dst_city": "Lagos"},
{"src_ip": "37.153.0.1",        "dst_ip": "197.228.64.1",      "src_lat":  30.0444, "src_lon":  31.2357, "dst_lat":  36.8065, "dst_lon":  10.1815,  "src_city": "Cairo",           "dst_city": "Tunis"},
{"src_ip": "41.248.64.1",       "dst_ip": "41.215.192.1",      "src_lat":  33.9716, "src_lon":  -6.8498, "dst_lat":  36.7538, "dst_lon":   3.0588,  "src_city": "Rabat",           "dst_city": "Algiers"},
{"src_ip": "197.0.72.1",        "dst_ip": "197.136.0.1",       "src_lat":   9.0280, "src_lon":  38.7469, "dst_lat":   2.0469, "dst_lon":  45.3182,  "src_city": "Addis Ababa",     "dst_city": "Mogadishu"},
{"src_ip": "196.216.2.1",       "dst_ip": "196.46.4.1",        "src_lat": -17.7333, "src_lon":  31.0500, "dst_lat": -15.4167, "dst_lon":  28.2833,  "src_city": "Harare",          "dst_city": "Lusaka"},
{"src_ip": "196.202.83.1",      "dst_ip": "41.203.64.1",       "src_lat":   9.0579, "src_lon":   7.4951, "dst_lat":   4.0611, "dst_lon":   9.7679,  "src_city": "Abuja",           "dst_city": "Douala"},
{"src_ip": "196.207.6.1",       "dst_ip": "197.157.192.1",     "src_lat":  -4.3217, "src_lon":  15.3222, "dst_lat": -11.7022, "dst_lon":  27.4748,  "src_city": "Kinshasa",        "dst_city": "Lubumbashi"},
{"src_ip": "196.41.128.1",      "dst_ip": "41.79.4.1",         "src_lat": -25.9692, "src_lon":  32.5732, "dst_lat": -18.9249, "dst_lon":  47.5185,  "src_city": "Maputo",          "dst_city": "Antananarivo"},
{"src_ip": "196.200.131.1",     "dst_ip": "196.168.0.1",       "src_lat":   5.5600, "src_lon":  -0.1969, "dst_lat":  12.3647, "dst_lon":  -1.5353,  "src_city": "Accra",           "dst_city": "Ouagadougou"},
{"src_ip": "197.225.98.1",      "dst_ip": "212.83.160.1",      "src_lat":  14.7167, "src_lon": -17.4677, "dst_lat":  12.6392, "dst_lon":  -8.0029,  "src_city": "Dakar",           "dst_city": "Bamako"},
{"src_ip": "213.158.182.1",     "dst_ip": "196.27.100.1",      "src_lat":  32.9081, "src_lon":  13.1899, "dst_lat":   3.8480, "dst_lon":  11.5021,  "src_city": "Tripoli",         "dst_city": "Yaoundé"},
{"src_ip": "196.1.99.1",        "dst_ip": "197.148.64.1",      "src_lat":  15.5507, "src_lon":  32.5322, "dst_lat":   0.3476, "dst_lon":  32.5825,  "src_city": "Omdurman",        "dst_city": "Kampala"},
{"src_ip": "196.218.0.1",       "dst_ip": "196.23.128.1",      "src_lat":  -1.9441, "src_lon":  30.0619, "dst_lat": -13.9626, "dst_lon":  33.7741,  "src_city": "Kigali",          "dst_city": "Lilongwe"},
{"src_ip": "196.200.0.1",       "dst_ip": "196.201.64.1",      "src_lat":   5.3600, "src_lon":  -4.0083, "dst_lat":   6.1375, "dst_lon":   1.2123,  "src_city": "Abidjan",         "dst_city": "Lomé"},
{"src_ip": "196.10.192.1",      "dst_ip": "196.43.64.1",       "src_lat": -22.5597, "src_lon":  17.0832, "dst_lat": -24.6282, "dst_lon":  25.9231,  "src_city": "Windhoek",        "dst_city": "Gaborone"},
{"src_ip": "196.168.64.1",      "dst_ip": "154.72.0.1",        "src_lat":   6.3703, "src_lon":   2.3912, "dst_lat":  13.5137, "dst_lon":   2.1098,  "src_city": "Cotonou",         "dst_city": "Niamey"},
{"src_ip": "197.234.64.1",      "dst_ip": "196.190.32.1",      "src_lat":  12.1348, "src_lon":  15.0557, "dst_lat":   0.3901, "dst_lon":   9.4544,  "src_city": "N'Djamena",       "dst_city": "Libreville"},
{"src_ip": "41.71.128.1",       "dst_ip": "196.14.0.1",        "src_lat":  11.5720, "src_lon":  43.1456, "dst_lat":  -8.8399, "dst_lon":  13.2894,  "src_city": "Djibouti City",   "dst_city": "Luanda"},

# ── Australia / Oceania ─────────────────────────────────────────────────
{"src_ip": "203.206.224.20",    "dst_ip": "202.124.127.230",   "src_lat": -33.8688, "src_lon": 151.2093, "dst_lat": -37.8136, "dst_lon": 144.9631,  "src_city": "Sydney",          "dst_city": "Melbourne"},
{"src_ip": "210.48.77.68",      "dst_ip": "202.89.8.15",       "src_lat": -36.8485, "src_lon": 174.7633, "dst_lat": -41.2865, "dst_lon": 174.7762,  "src_city": "Auckland",        "dst_city": "Wellington"},
{"src_ip": "203.0.178.191",     "dst_ip": "203.57.57.57",      "src_lat": -27.4698, "src_lon": 153.0251, "dst_lat": -31.9505, "dst_lon": 115.8605,  "src_city": "Brisbane",        "dst_city": "Perth"},
{"src_ip": "202.159.253.1",     "dst_ip": "202.188.0.1",       "src_lat": -34.9285, "src_lon": 138.6007, "dst_lat": -12.4634, "dst_lon": 130.8456,  "src_city": "Adelaide",        "dst_city": "Darwin"},
{"src_ip": "203.2.218.1",       "dst_ip": "203.22.104.1",      "src_lat": -35.2835, "src_lon": 149.1281, "dst_lat": -43.5321, "dst_lon": 172.6362,  "src_city": "Canberra",        "dst_city": "Christchurch"},
{"src_ip": "202.72.0.1",        "dst_ip": "202.131.0.1",       "src_lat": -18.1248, "src_lon": 178.4501, "dst_lat":  -9.4438, "dst_lon": 147.1803,  "src_city": "Suva",            "dst_city": "Port Moresby"},
]


def add_real_ips_to_csv(input_file='test_data.csv', output_file='test_data_with_ips.csv'):
    """
    Add real-world IP addresses and locations to the CSV file
    """
    print(f"📂 Reading {input_file}...")
    df = pd.read_csv(input_file)

    print(f"📊 Found {len(df)} records")
    print(f"🌍 Adding real-world IP addresses from {len(REAL_WORLD_IPS)} location pairs...")

    # Randomly assign IP addresses from our pool
    ip_assignments = [random.choice(REAL_WORLD_IPS) for _ in range(len(df))]

    # Add new columns
    df['src_ip']   = [ip['src_ip']   for ip in ip_assignments]
    df['dst_ip']   = [ip['dst_ip']   for ip in ip_assignments]
    df['src_lat']  = [ip['src_lat']  for ip in ip_assignments]
    df['src_lon']  = [ip['src_lon']  for ip in ip_assignments]
    df['dst_lat']  = [ip['dst_lat']  for ip in ip_assignments]
    df['dst_lon']  = [ip['dst_lon']  for ip in ip_assignments]
    df['src_city'] = [ip['src_city'] for ip in ip_assignments]
    df['dst_city'] = [ip['dst_city'] for ip in ip_assignments]

    # Save to new file
    df.to_csv(output_file, index=False)

    print(f"✅ Enhanced CSV saved to: {output_file}")
    print(f"📈 Total columns: {len(df.columns)}")
    print(f"📋 New columns added: src_ip, dst_ip, src_lat, src_lon, dst_lat, dst_lon, src_city, dst_city")

    # Show sample
    print("\n📝 Sample data (first 3 rows):")
    print(df[['src_ip', 'dst_ip', 'src_city', 'dst_city']].head(3))

    return df


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🛡️  Network Intrusion Detection - IP Address Generator")
    print("="*60 + "\n")

    df_enhanced = add_real_ips_to_csv()

    print("\n" + "="*60)
    print(f"✨ Done!  {len(REAL_WORLD_IPS)} city-pairs available → test_data_with_ips.csv")
    print("="*60 + "\n")
