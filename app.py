import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
from tensorflow import keras
import json
import time
from datetime import datetime
import random
import tensorflow as tf

app = Flask(__name__)

# Register the Sampling layer so VAE can be loaded
@keras.utils.register_keras_serializable()
class Sampling(keras.layers.Layer):
    """Uses (z_mean, z_log_var) to sample z, the vector encoding."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def call(self, inputs):
        z_mean, z_log_var = inputs
        batch = tf.shape(z_mean)[0]
        dim = tf.shape(z_mean)[1]
        epsilon = tf.random.normal(shape=(batch, dim))
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon

# Use relative paths for deployment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LSTM_MODEL_PATH = 'best_fl_model_LSTM_AE.keras'
VAE_MODEL_PATH  = 'best_model_VAE_Before_FL.keras'

lstm_model = None
vae_model  = None
_models_loaded = False

def load_models():
    """Lazy load models only when needed to prevent OOM on startup."""
    global lstm_model, vae_model, _models_loaded
    if _models_loaded:
        return
    try:
        lstm_model = keras.models.load_model(LSTM_MODEL_PATH, compile=False)
        print("✓ LSTM model loaded successfully")
    except Exception as e:
        print(f"✗ Error loading LSTM model: {e}")

    try:
        vae_model = keras.models.load_model(VAE_MODEL_PATH, custom_objects={'Sampling': Sampling}, compile=False)
        print("✓ VAE model loaded successfully")
    except Exception as e:
        print(f"✗ Error loading VAE model: {e}")
    
    _models_loaded = True

# Thresholds
LSTM_THRESHOLD = 0.000053
VAE_THRESHOLD  = 0.000241

# ─────────────────────────────────────────────────────────────────────────────
# EXPANDED IP + CITY POOL  (100+ land-only cities, unique IPs)
# ─────────────────────────────────────────────────────────────────────────────
CITY_NODES = [
    # ── North America ──────────────────────────────────────────────────────
    {"ip": "8.8.8.8",           "lat": 37.7749,  "lon": -122.4194, "city": "San Francisco"},
    {"ip": "142.250.185.46",    "lat": 40.7128,  "lon": -74.0060,  "city": "New York"},
    {"ip": "151.101.1.140",     "lat": 41.8781,  "lon": -87.6298,  "city": "Chicago"},
    {"ip": "172.217.14.206",    "lat": 29.7604,  "lon": -95.3698,  "city": "Houston"},
    {"ip": "1.1.1.1",           "lat": 34.0522,  "lon": -118.2437, "city": "Los Angeles"},
    {"ip": "13.107.42.14",      "lat": 47.6062,  "lon": -122.3321, "city": "Seattle"},
    {"ip": "104.16.132.229",    "lat": 33.4484,  "lon": -112.0740, "city": "Phoenix"},
    {"ip": "23.185.0.2",        "lat": 25.7617,  "lon": -80.1918,  "city": "Miami"},
    {"ip": "205.251.242.103",   "lat": 43.6532,  "lon": -79.3832,  "city": "Toronto"},
    {"ip": "206.81.0.1",        "lat": 45.5017,  "lon": -73.5673,  "city": "Montreal"},
    {"ip": "192.30.255.112",    "lat": 49.2827,  "lon": -123.1207, "city": "Vancouver"},
    {"ip": "54.239.28.85",      "lat": 39.9526,  "lon": -75.1652,  "city": "Philadelphia"},
    {"ip": "104.244.42.65",     "lat": 30.2672,  "lon": -97.7431,  "city": "Austin"},
    {"ip": "198.41.0.4",        "lat": 32.7767,  "lon": -96.7970,  "city": "Dallas"},
    {"ip": "8.26.56.26",        "lat": 33.7490,  "lon": -84.3880,  "city": "Atlanta"},
    {"ip": "68.87.76.178",      "lat": 42.3601,  "lon": -71.0589,  "city": "Boston"},
    {"ip": "72.21.91.8",        "lat": 39.7392,  "lon": -104.9903, "city": "Denver"},
    {"ip": "209.51.188.17",     "lat": 36.1699,  "lon": -115.1398, "city": "Las Vegas"},
    {"ip": "69.171.224.11",     "lat": 38.9072,  "lon": -77.0369,  "city": "Washington DC"},
    {"ip": "149.154.167.51",    "lat": 44.9778,  "lon": -93.2650,  "city": "Minneapolis"},
    {"ip": "198.35.26.96",      "lat": 47.5615,  "lon": -52.7126,  "city": "St. John's"},
    {"ip": "204.13.164.1",      "lat": 51.0447,  "lon": -114.0719, "city": "Calgary"},
    {"ip": "96.7.128.175",      "lat": 19.4326,  "lon": -99.1332,  "city": "Mexico City"},
    {"ip": "200.33.224.1",      "lat": 20.9674,  "lon": -89.5926,  "city": "Merida"},
    {"ip": "190.214.135.59",    "lat": 10.4806,  "lon": -66.9036,  "city": "Caracas"},

    # ── Europe ─────────────────────────────────────────────────────────────
    {"ip": "185.60.216.35",     "lat": 51.5074,  "lon": -0.1278,   "city": "London"},
    {"ip": "195.154.122.113",   "lat": 48.8566,  "lon":  2.3522,   "city": "Paris"},
    {"ip": "46.4.105.116",      "lat": 52.5200,  "lon": 13.4050,   "city": "Berlin"},
    {"ip": "217.160.0.187",     "lat": 41.9028,  "lon": 12.4964,   "city": "Rome"},
    {"ip": "91.198.174.192",    "lat": 40.4168,  "lon": -3.7038,   "city": "Madrid"},
    {"ip": "185.15.59.224",     "lat": 52.3676,  "lon":  4.9041,   "city": "Amsterdam"},
    {"ip": "194.150.245.142",   "lat": 59.3293,  "lon": 18.0686,   "city": "Stockholm"},
    {"ip": "213.180.193.3",     "lat": 55.7558,  "lon": 37.6173,   "city": "Moscow"},
    {"ip": "77.109.128.1",      "lat": 47.3769,  "lon":  8.5417,   "city": "Zurich"},
    {"ip": "178.254.3.1",       "lat": 48.2082,  "lon": 16.3738,   "city": "Vienna"},
    {"ip": "89.207.132.170",    "lat": 50.0755,  "lon": 14.4378,   "city": "Prague"},
    {"ip": "185.83.216.1",      "lat": 52.2297,  "lon": 21.0122,   "city": "Warsaw"},
    {"ip": "88.84.209.116",     "lat": 47.4979,  "lon": 19.0402,   "city": "Budapest"},
    {"ip": "213.251.173.1",     "lat": 45.4654,  "lon":  9.1859,   "city": "Milan"},
    {"ip": "194.97.97.97",      "lat": 59.4370,  "lon": 24.7536,   "city": "Tallinn"},
    {"ip": "84.22.100.108",     "lat": 60.1699,  "lon": 24.9384,   "city": "Helsinki"},
    {"ip": "195.43.85.53",      "lat": 55.6761,  "lon": 12.5683,   "city": "Copenhagen"},
    {"ip": "178.63.20.83",      "lat": 53.3498,  "lon": -6.2603,   "city": "Dublin"},
    {"ip": "83.97.20.34",       "lat": 41.3275,  "lon": 19.8187,   "city": "Tirana"},
    {"ip": "95.172.88.1",       "lat": 43.8563,  "lon": 18.4131,   "city": "Sarajevo"},
    {"ip": "188.93.16.1",       "lat": 44.8176,  "lon": 20.4633,   "city": "Belgrade"},
    {"ip": "213.108.105.1",     "lat": 42.6977,  "lon": 23.3219,   "city": "Sofia"},
    {"ip": "62.108.32.1",       "lat": 37.9755,  "lon": 23.7348,   "city": "Athens"},
    {"ip": "5.45.96.220",       "lat": 50.4501,  "lon": 30.5234,   "city": "Kyiv"},
    {"ip": "213.152.176.1",     "lat": 41.6938,  "lon": 44.8015,   "city": "Tbilisi"},

    # ── Asia ────────────────────────────────────────────────────────────────
    {"ip": "202.12.27.33",      "lat": 35.6762,  "lon":  139.6503, "city": "Tokyo"},
    {"ip": "103.28.248.1",      "lat": 37.5665,  "lon":  126.9780, "city": "Seoul"},
    {"ip": "61.135.169.125",    "lat": 39.9042,  "lon":  116.4074, "city": "Beijing"},
    {"ip": "180.149.132.47",    "lat": 31.2304,  "lon":  121.4737, "city": "Shanghai"},
    {"ip": "103.21.244.0",      "lat": 28.7041,  "lon":   77.1025, "city": "New Delhi"},
    {"ip": "182.50.132.242",    "lat": 19.0760,  "lon":   72.8777, "city": "Mumbai"},
    {"ip": "202.65.115.242",    "lat":  1.3521,  "lon":  103.8198, "city": "Singapore"},
    {"ip": "103.10.28.61",      "lat": 13.7563,  "lon":  100.5018, "city": "Bangkok"},
    {"ip": "114.111.167.14",    "lat": 22.3193,  "lon":  114.1694, "city": "Hong Kong"},
    {"ip": "203.104.144.75",    "lat": -6.2088,  "lon":  106.8456, "city": "Jakarta"},
    {"ip": "202.150.221.20",    "lat": 21.0285,  "lon":  105.8542, "city": "Hanoi"},
    {"ip": "203.162.2.1",       "lat": 10.8231,  "lon":  106.6297, "city": "Ho Chi Minh City"},
    {"ip": "121.54.32.1",       "lat": 14.5995,  "lon":  120.9842, "city": "Manila"},
    {"ip": "202.8.75.1",        "lat":  3.1390,  "lon":  101.6869, "city": "Kuala Lumpur"},
    {"ip": "112.213.89.1",      "lat": 16.8661,  "lon":   96.1951, "city": "Yangon"},
    {"ip": "202.56.250.1",      "lat": 23.7275,  "lon":   90.3945, "city": "Dhaka"},
    {"ip": "202.125.128.1",     "lat": 24.8607,  "lon":   67.0011, "city": "Karachi"},
    {"ip": "202.83.24.1",       "lat": 31.5497,  "lon":   74.3436, "city": "Lahore"},
    {"ip": "193.29.55.1",       "lat": 34.5553,  "lon":   69.2075, "city": "Kabul"},
    {"ip": "91.212.10.1",       "lat": 35.6892,  "lon":   51.3890, "city": "Tehran"},
    {"ip": "5.21.0.1",          "lat": 33.3128,  "lon":   44.3615, "city": "Baghdad"},
    {"ip": "46.30.160.1",       "lat": 24.7136,  "lon":   46.6753, "city": "Riyadh"},
    {"ip": "94.101.192.1",      "lat": 23.6850,  "lon":   58.1829, "city": "Muscat"},
    {"ip": "185.90.56.1",       "lat": 25.2854,  "lon":   51.5310, "city": "Doha"},
    {"ip": "212.117.128.1",     "lat": 24.4539,  "lon":   54.3773, "city": "Abu Dhabi"},
    {"ip": "43.250.192.1",      "lat": 17.3850,  "lon":   78.4867, "city": "Hyderabad"},
    {"ip": "14.139.223.1",      "lat": 12.9716,  "lon":   77.5946, "city": "Bengaluru"},
    {"ip": "43.231.244.1",      "lat": 13.0827,  "lon":   80.2707, "city": "Chennai"},
    {"ip": "202.53.94.1",       "lat": 22.5726,  "lon":   88.3639, "city": "Kolkata"},
    {"ip": "36.255.68.1",       "lat": 27.7172,  "lon":   85.3240, "city": "Kathmandu"},
    {"ip": "203.81.89.1",       "lat":  6.9271,  "lon":   79.8612, "city": "Colombo"},
    {"ip": "202.84.252.1",      "lat": 43.2220,  "lon":   76.8512, "city": "Almaty"},
    {"ip": "195.20.0.1",        "lat": 41.2995,  "lon":   69.2401, "city": "Tashkent"},
    {"ip": "217.174.248.1",     "lat": 37.9601,  "lon":   58.3261, "city": "Ashgabat"},
    {"ip": "217.77.192.1",      "lat": 38.5598,  "lon":   68.7738, "city": "Dushanbe"},
    {"ip": "80.80.224.1",       "lat": 42.8746,  "lon":   74.5698, "city": "Bishkek"},
    {"ip": "210.125.163.1",     "lat": 47.9077,  "lon":  106.8832, "city": "Ulaanbaatar"},
    {"ip": "58.253.9.1",        "lat": 22.2855,  "lon":  114.1577, "city": "Shenzhen"},
    {"ip": "163.180.103.1",     "lat": 35.1796,  "lon":  129.0756, "city": "Busan"},

    # ── Middle East ─────────────────────────────────────────────────────────
    {"ip": "185.125.190.36",    "lat": 25.2048,  "lon":   55.2708, "city": "Dubai"},
    {"ip": "213.42.20.19",      "lat": 31.7683,  "lon":   35.2137, "city": "Jerusalem"},
    {"ip": "37.48.64.150",      "lat": 33.8886,  "lon":   35.4955, "city": "Beirut"},
    {"ip": "5.63.13.202",       "lat": 41.0082,  "lon":   28.9784, "city": "Istanbul"},
    {"ip": "5.44.168.1",        "lat": 32.0853,  "lon":   34.7818, "city": "Tel Aviv"},
    {"ip": "62.235.200.1",      "lat": 33.5138,  "lon":   36.2765, "city": "Damascus"},
    {"ip": "37.153.0.1",        "lat": 30.0444,  "lon":   31.2357, "city": "Cairo"},
    {"ip": "5.100.0.1",         "lat": 15.5527,  "lon":   32.5324, "city": "Khartoum"},

    # ── South America ───────────────────────────────────────────────────────
    {"ip": "200.221.11.100",    "lat": -23.5505, "lon":  -46.6333, "city": "São Paulo"},
    {"ip": "186.148.177.20",    "lat": -34.6037, "lon":  -58.3816, "city": "Buenos Aires"},
    {"ip": "190.98.248.254",    "lat":   4.7110, "lon":  -74.0721, "city": "Bogotá"},
    {"ip": "181.225.253.186",   "lat": -12.0464, "lon":  -77.0428, "city": "Lima"},
    {"ip": "200.10.60.1",       "lat": -15.8267, "lon":  -47.9218, "city": "Brasília"},
    {"ip": "186.10.48.1",       "lat": -33.4489, "lon":  -70.6693, "city": "Santiago"},
    {"ip": "200.105.141.1",     "lat": -17.7833, "lon":  -63.1821, "city": "Santa Cruz"},
    {"ip": "186.155.8.1",       "lat":  -0.1807, "lon":  -78.4678, "city": "Quito"},
    {"ip": "186.64.112.1",      "lat":  10.4806, "lon":  -66.9036, "city": "Caracas"},
    {"ip": "200.195.139.1",     "lat":  -8.0476, "lon":  -34.8770, "city": "Recife"},
    {"ip": "200.24.128.1",      "lat":   3.8667, "lon":  -67.9000, "city": "Puerto Ayacucho"},
    {"ip": "190.6.64.1",        "lat": -25.2867, "lon":  -57.6470, "city": "Asunción"},
    {"ip": "200.40.30.245",     "lat": -34.9011, "lon":  -56.1645, "city": "Montevideo"},

    # ── Africa ──────────────────────────────────────────────────────────────
    {"ip": "197.242.150.244",   "lat": -26.2041, "lon":   28.0473, "city": "Johannesburg"},
    {"ip": "41.190.232.52",     "lat":  -1.2921, "lon":   36.8219, "city": "Nairobi"},
    {"ip": "105.235.130.54",    "lat": -33.9249, "lon":   18.4241, "city": "Cape Town"},
    {"ip": "154.73.220.137",    "lat":   6.5244, "lon":    3.3792, "city": "Lagos"},
    {"ip": "196.200.131.1",     "lat":   5.5600, "lon":   -0.1969, "city": "Accra"},
    {"ip": "196.168.0.1",       "lat":  12.3647, "lon":   -1.5353, "city": "Ouagadougou"},
    {"ip": "197.225.98.1",      "lat":  14.7167, "lon":  -17.4677, "city": "Dakar"},
    {"ip": "196.202.83.1",      "lat":   9.0579, "lon":    7.4951, "city": "Abuja"},
    {"ip": "41.203.64.1",       "lat":   4.0611, "lon":    9.7679, "city": "Douala"},
    {"ip": "196.207.6.1",       "lat": -4.3217,  "lon":   15.3222, "city": "Kinshasa"},
    {"ip": "197.157.192.1",     "lat": -11.7022, "lon":   27.4748, "city": "Lubumbashi"},
    {"ip": "196.41.128.1",      "lat": -25.9692, "lon":   32.5732, "city": "Maputo"},
    {"ip": "41.79.4.1",         "lat": -18.9249, "lon":   47.5185, "city": "Antananarivo"},
    {"ip": "196.27.100.1",      "lat":   3.8480,  "lon":   11.5021, "city": "Yaoundé"},
    {"ip": "196.1.99.1",        "lat":  15.5507,  "lon":   32.5322, "city": "Omdurman"},
    {"ip": "197.0.72.1",        "lat":   9.0280,  "lon":   38.7469, "city": "Addis Ababa"},
    {"ip": "197.136.0.1",       "lat":   2.0469,  "lon":   45.3182, "city": "Mogadishu"},
    {"ip": "196.216.2.1",       "lat": -17.7333,  "lon":   31.0500, "city": "Harare"},
    {"ip": "196.46.4.1",        "lat": -15.4167,  "lon":   28.2833, "city": "Lusaka"},
    {"ip": "197.228.64.1",      "lat":  36.8065,  "lon":   10.1815, "city": "Tunis"},
    {"ip": "41.248.64.1",       "lat":  33.9716,  "lon":   -6.8498, "city": "Rabat"},
    {"ip": "41.215.192.1",      "lat":  36.7538,  "lon":    3.0588, "city": "Algiers"},
    {"ip": "213.158.182.1",     "lat":  32.9081,  "lon":   13.1899, "city": "Tripoli"},

    # ── Australia / Oceania ─────────────────────────────────────────────────
    {"ip": "203.206.224.20",    "lat": -33.8688, "lon":  151.2093, "city": "Sydney"},
    {"ip": "202.124.127.230",   "lat": -37.8136, "lon":  144.9631, "city": "Melbourne"},
    {"ip": "210.48.77.68",      "lat": -36.8485, "lon":  174.7633, "city": "Auckland"},
    {"ip": "202.89.8.15",       "lat": -41.2865, "lon":  174.7762, "city": "Wellington"},
    {"ip": "203.0.178.191",     "lat": -27.4698, "lon":  153.0251, "city": "Brisbane"},
    {"ip": "203.57.57.57",      "lat": -31.9505, "lon":  115.8605, "city": "Perth"},
    {"ip": "202.159.253.1",     "lat": -34.9285, "lon":  138.6007, "city": "Adelaide"},
    {"ip": "202.188.0.1",       "lat": -12.4634, "lon":  130.8456, "city": "Darwin"},
    {"ip": "203.22.104.1",      "lat": -43.5321, "lon":  172.6362, "city": "Christchurch"},
    {"ip": "202.7.167.1",       "lat": -17.7333, "lon":  168.3273, "city": "Port Vila"},
]

JITTER_SCALE = 0.08

def _jitter(lat, lon):
    return (
        lat + random.uniform(-JITTER_SCALE, JITTER_SCALE),
        lon + random.uniform(-JITTER_SCALE, JITTER_SCALE),
    )

def add_real_ips_to_data(df_in):
    n = len(df_in)
    src_nodes = random.choices(CITY_NODES, k=n)
    dst_nodes = random.choices(CITY_NODES, k=n)

    src_lats, src_lons, dst_lats, dst_lons = [], [], [], []
    for s, d in zip(src_nodes, dst_nodes):
        slat, slon = _jitter(s["lat"], s["lon"])
        dlat, dlon = _jitter(d["lat"], d["lon"])
        src_lats.append(slat);  src_lons.append(slon)
        dst_lats.append(dlat);  dst_lons.append(dlon)

    df2 = df_in.copy()
    df2["src_ip"]   = [n["ip"]   for n in src_nodes]
    df2["dst_ip"]   = [n["ip"]   for n in dst_nodes]
    df2["src_lat"]  = src_lats
    df2["src_lon"]  = src_lons
    df2["dst_lat"]  = dst_lats
    df2["dst_lon"]  = dst_lons
    df2["src_city"] = [n["city"] for n in src_nodes]
    df2["dst_city"] = [n["city"] for n in dst_nodes]
    return df2

# Global cached data
df = None
df_with_ips = None
feature_cols = []
data_loaded = False

def load_data():
    """Load data lazily to speed up startup."""
    global df, df_with_ips, feature_cols, data_loaded
    if data_loaded:
        return
    csv_path = 'test_data.csv'
    df = pd.read_csv(csv_path)
    df_with_ips = add_real_ips_to_data(df)
    
    exclude_cols = ['label','src_ip','dst_ip','src_lat','src_lon','dst_lat','dst_lon','src_city','dst_city']
    feature_cols = [c for c in df.columns if c not in exclude_cols]
    data_loaded = True

@app.before_request
def setup():
    # Only loads data on the very first HTTP request
    if request.endpoint in ['start_detection', 'get_next_prediction']:
        load_data()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/start_detection', methods=['POST'])
def start_detection():
    data       = request.json
    model_type = data.get('model_type', 'lstm')
    test_size  = data.get('test_size', 100)

    try:
        test_size = int(test_size)
    except Exception:
        test_size = 100

    if test_size not in {25, 50, 75, 100}:
        test_size = 100

    # Ensure models are loaded
    load_models()

    subset_len = max(1, int(len(df_with_ips) * (test_size / 100.0)))

    return jsonify({
        'status':        'started',
        'model_type':    model_type,
        'total_records': subset_len
    })


@app.route('/api/get_next_prediction', methods=['POST'])
def get_next_prediction():
    data       = request.json
    model_type = data.get('model_type', 'lstm')
    index      = data.get('index', 0)

    if not data_loaded:
        return jsonify({'error': 'Data not initialized'}), 500

    if index >= len(df_with_ips):
        return jsonify({'status': 'completed', 'total_processed': index})

    row = df_with_ips.iloc[index]
    features = row[feature_cols].values.astype(np.float32).reshape(1, -1)
    actual_label = int(row['label'])

    if model_type == 'lstm':
        if lstm_model is None:
            return jsonify({'error': 'LSTM model not loaded'}), 500
        reconstruction       = lstm_model.predict(features, verbose=0)
        reconstruction_error = float(np.mean(np.square(features - reconstruction)))
        predicted_label      = 1 if reconstruction_error > LSTM_THRESHOLD else 0
        threshold            = LSTM_THRESHOLD
    else:
        if vae_model is None:
            return jsonify({'error': 'VAE model not loaded'}), 500
        reconstruction       = vae_model.predict(features, verbose=0)
        reconstruction_error = float(np.mean(np.square(features - reconstruction)))
        predicted_label      = 1 if reconstruction_error > VAE_THRESHOLD else 0
        threshold            = VAE_THRESHOLD

    result = {
        'index':               index,
        'src_ip':              row['src_ip'],
        'dst_ip':              row['dst_ip'],
        'src_lat':             float(row['src_lat']),
        'src_lon':             float(row['src_lon']),
        'dst_lat':             float(row['dst_lat']),
        'dst_lon':             float(row['dst_lon']),
        'src_city':            row['src_city'],
        'dst_city':            row['dst_city'],
        'actual_label':        actual_label,
        'predicted_label':     predicted_label,
        'reconstruction_error': reconstruction_error,
        'threshold':           threshold,
        'timestamp':           datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    return jsonify({
        'status': 'success',
        'result': result
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
