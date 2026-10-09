from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'trendify_professional_secret_2026_change_in_production')

# ============================================================
# PRODUCT STORAGE (JSON file - permanent save)
# ============================================================
# Prefer /data when Railway Volume is mounted (survives restarts)
if os.path.isdir('/data'):
    DATA_DIR = '/data'
else:
    DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
PRODUCTS_FILE = os.path.join(DATA_DIR, 'products.json')
ORDERS_FILE = os.path.join(DATA_DIR, 'orders.json')

os.makedirs(DATA_DIR, exist_ok=True)

# Default products (used only on first run when no file exists)
DEFAULT_PRODUCTS = json.loads(r'''
[
  {
    "id": 1,
    "name": "CASUAL WHITE SNEAKERS",
    "brand": "TRENDIFY",
    "price": 1299.0,
    "old_price": 1799.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality casual white sneakers from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 27,
    "in_stock": true
  },
  {
    "id": 2,
    "name": "BLACK MESH RUNNERS",
    "brand": "TRENDIFY",
    "price": 1199.0,
    "old_price": 1599.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality black mesh runners from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6000000000000005,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 25,
    "in_stock": true
  },
  {
    "id": 3,
    "name": "NAVY SPORT SHOES",
    "brand": "TRENDIFY",
    "price": 1399.0,
    "old_price": 1899.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality navy sport shoes from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.7,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 26,
    "in_stock": true
  },
  {
    "id": 4,
    "name": "BROWN LEATHER CASUAL",
    "brand": "TRENDIFY",
    "price": 2499.0,
    "old_price": 3499.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality brown leather casual from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.800000000000001,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 28,
    "in_stock": true
  },
  {
    "id": 5,
    "name": "SLIP-ON COMFORT SHOES",
    "brand": "TRENDIFY",
    "price": 999.0,
    "old_price": 1499.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality slip-on comfort shoes from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.4,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 33,
    "in_stock": true
  },
  {
    "id": 6,
    "name": "HIGH TOP SNEAKERS",
    "brand": "TRENDIFY",
    "price": 1699.0,
    "old_price": 2299.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality high top sneakers from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 26,
    "in_stock": true
  },
  {
    "id": 7,
    "name": "WALKING SHOES MEN",
    "brand": "TRENDIFY",
    "price": 1149.0,
    "old_price": 1599.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality walking shoes men from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6000000000000005,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 28,
    "in_stock": true
  },
  {
    "id": 8,
    "name": "GYM TRAINING SHOES",
    "brand": "TRENDIFY",
    "price": 1599.0,
    "old_price": 2199.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality gym training shoes from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.7,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 27,
    "in_stock": true
  },
  {
    "id": 9,
    "name": "FORMAL OFFICE SHOES",
    "brand": "TRENDIFY",
    "price": 2899.0,
    "old_price": 3999.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality formal office shoes from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.800000000000001,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 27,
    "in_stock": true
  },
  {
    "id": 10,
    "name": "KIDS SPORT SNEAKERS",
    "brand": "TRENDIFY",
    "price": 899.0,
    "old_price": 1299.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality kids sport sneakers from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.4,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 11,
    "name": "CHUNKY SOLE SNEAKERS",
    "brand": "TRENDIFY",
    "price": 1799.0,
    "old_price": 2499.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality chunky sole sneakers from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 28,
    "in_stock": true
  },
  {
    "id": 12,
    "name": "CANVAS LOW TOP",
    "brand": "TRENDIFY",
    "price": 1099.0,
    "old_price": 1499.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality canvas low top from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6000000000000005,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 26,
    "in_stock": true
  },
  {
    "id": 13,
    "name": "RUNNING PRO SHOES",
    "brand": "TRENDIFY",
    "price": 1899.0,
    "old_price": 2599.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality running pro shoes from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.7,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 26,
    "in_stock": true
  },
  {
    "id": 14,
    "name": "SUEDE CASUAL MOCCASIN",
    "brand": "TRENDIFY",
    "price": 2199.0,
    "old_price": 2999.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality suede casual moccasin from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.800000000000001,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 26,
    "in_stock": true
  },
  {
    "id": 15,
    "name": "ORANGE ACCENT RUNNERS",
    "brand": "TRENDIFY",
    "price": 1349.0,
    "old_price": 1849.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality orange accent runners from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.4,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 27,
    "in_stock": true
  },
  {
    "id": 16,
    "name": "ALL BLACK STREET SHOES",
    "brand": "TRENDIFY",
    "price": 1249.0,
    "old_price": 1699.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality all black street shoes from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 26,
    "in_stock": true
  },
  {
    "id": 17,
    "name": "WHITE PLATFORM SNEAKERS",
    "brand": "TRENDIFY",
    "price": 1999.0,
    "old_price": 2799.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality white platform sneakers from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6000000000000005,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 28,
    "in_stock": true
  },
  {
    "id": 18,
    "name": "TRAIL HIKING SHOES",
    "brand": "TRENDIFY",
    "price": 2699.0,
    "old_price": 3599.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality trail hiking shoes from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.7,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 25,
    "in_stock": true
  },
  {
    "id": 19,
    "name": "SOFT FOAM SLIDES",
    "brand": "TRENDIFY",
    "price": 699.0,
    "old_price": 999.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality soft foam slides from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.800000000000001,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 20,
    "name": "ANIMAL PRINT SNEAKERS",
    "brand": "TRENDIFY",
    "price": 1499.0,
    "old_price": 2099.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality animal print sneakers from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.4,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 28,
    "in_stock": true
  },
  {
    "id": 21,
    "name": "CLASSIC LOAFERS",
    "brand": "TRENDIFY",
    "price": 2399.0,
    "old_price": 3299.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality classic loafers from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 27,
    "in_stock": true
  },
  {
    "id": 22,
    "name": "KNIT SOCK SNEAKERS",
    "brand": "TRENDIFY",
    "price": 1299.0,
    "old_price": 1799.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality knit sock sneakers from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6000000000000005,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 27,
    "in_stock": true
  },
  {
    "id": 23,
    "name": "VELCRO SPORT SHOES",
    "brand": "TRENDIFY",
    "price": 949.0,
    "old_price": 1349.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality velcro sport shoes from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.7,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 29,
    "in_stock": true
  },
  {
    "id": 24,
    "name": "DUAL TONE CASUAL",
    "brand": "TRENDIFY",
    "price": 1549.0,
    "old_price": 2149.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality dual tone casual from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.800000000000001,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 27,
    "in_stock": true
  },
  {
    "id": 25,
    "name": "LIGHTWEIGHT JOGGERS",
    "brand": "TRENDIFY",
    "price": 1179.0,
    "old_price": 1579.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality lightweight joggers from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.4,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 25,
    "in_stock": true
  },
  {
    "id": 26,
    "name": "CLASSIC LEATHER STRAP WATCH",
    "brand": "TRENDIFY",
    "price": 1499.0,
    "old_price": 2199.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality classic leather strap watch from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.7,
    "category": "Watches",
    "variants": [],
    "discount_percent": 31,
    "in_stock": true
  },
  {
    "id": 27,
    "name": "BLACK CHRONOGRAPH WATCH",
    "brand": "TRENDIFY",
    "price": 1899.0,
    "old_price": 2699.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality black chronograph watch from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.8,
    "category": "Watches",
    "variants": [],
    "discount_percent": 29,
    "in_stock": true
  },
  {
    "id": 28,
    "name": "GOLD TONE DRESS WATCH",
    "brand": "TRENDIFY",
    "price": 2299.0,
    "old_price": 3299.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality gold tone dress watch from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Watches",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 29,
    "name": "SILICONE SPORT WATCH",
    "brand": "TRENDIFY",
    "price": 899.0,
    "old_price": 1299.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality silicone sport watch from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6,
    "category": "Watches",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 30,
    "name": "SKELETON AUTOMATIC STYLE",
    "brand": "TRENDIFY",
    "price": 2799.0,
    "old_price": 3999.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality skeleton automatic style from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.7,
    "category": "Watches",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 31,
    "name": "MINIMAL SILVER WATCH",
    "brand": "TRENDIFY",
    "price": 1299.0,
    "old_price": 1899.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality minimal silver watch from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.8,
    "category": "Watches",
    "variants": [],
    "discount_percent": 31,
    "in_stock": true
  },
  {
    "id": 32,
    "name": "DUAL TIME ZONE WATCH",
    "brand": "TRENDIFY",
    "price": 1999.0,
    "old_price": 2899.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality dual time zone watch from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Watches",
    "variants": [],
    "discount_percent": 31,
    "in_stock": true
  },
  {
    "id": 33,
    "name": "ROSE GOLD LADIES WATCH",
    "brand": "TRENDIFY",
    "price": 1699.0,
    "old_price": 2499.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality rose gold ladies watch from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6,
    "category": "Watches",
    "variants": [],
    "discount_percent": 32,
    "in_stock": true
  },
  {
    "id": 34,
    "name": "DIGITAL SPORT WATCH",
    "brand": "TRENDIFY",
    "price": 799.0,
    "old_price": 1199.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality digital sport watch from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.7,
    "category": "Watches",
    "variants": [],
    "discount_percent": 33,
    "in_stock": true
  },
  {
    "id": 35,
    "name": "MESH BRACELET WATCH",
    "brand": "TRENDIFY",
    "price": 1599.0,
    "old_price": 2299.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality mesh bracelet watch from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.8,
    "category": "Watches",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 36,
    "name": "SQUARE TANK WATCH",
    "brand": "TRENDIFY",
    "price": 2199.0,
    "old_price": 3099.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality square tank watch from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Watches",
    "variants": [],
    "discount_percent": 29,
    "in_stock": true
  },
  {
    "id": 37,
    "name": "RUBBER STRAP DIVER STYLE",
    "brand": "TRENDIFY",
    "price": 1799.0,
    "old_price": 2599.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality rubber strap diver style from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6,
    "category": "Watches",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 38,
    "name": "COUPLE WATCH SET",
    "brand": "TRENDIFY",
    "price": 2999.0,
    "old_price": 4299.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality couple watch set from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.7,
    "category": "Watches",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 39,
    "name": "SMART LOOK HYBRID WATCH",
    "brand": "TRENDIFY",
    "price": 3499.0,
    "old_price": 4999.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality smart look hybrid watch from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.8,
    "category": "Watches",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 40,
    "name": "VINTAGE BROWN WATCH",
    "brand": "TRENDIFY",
    "price": 1399.0,
    "old_price": 1999.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality vintage brown watch from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Watches",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 41,
    "name": "STEEL BRACELET CHRONO",
    "brand": "TRENDIFY",
    "price": 2099.0,
    "old_price": 2999.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality steel bracelet chrono from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6,
    "category": "Watches",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 42,
    "name": "SLIM FORMAL WATCH",
    "brand": "TRENDIFY",
    "price": 1199.0,
    "old_price": 1699.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality slim formal watch from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.7,
    "category": "Watches",
    "variants": [],
    "discount_percent": 29,
    "in_stock": true
  },
  {
    "id": 43,
    "name": "KIDS CARTOON WATCH",
    "brand": "TRENDIFY",
    "price": 599.0,
    "old_price": 899.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality kids cartoon watch from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.8,
    "category": "Watches",
    "variants": [],
    "discount_percent": 33,
    "in_stock": true
  },
  {
    "id": 44,
    "name": "LUXURY BOXED WATCH SET",
    "brand": "TRENDIFY",
    "price": 2499.0,
    "old_price": 3599.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality luxury boxed watch set from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Watches",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 45,
    "name": "ARABIC DIAL WATCH",
    "brand": "TRENDIFY",
    "price": 1899.0,
    "old_price": 2699.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality arabic dial watch from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6,
    "category": "Watches",
    "variants": [],
    "discount_percent": 29,
    "in_stock": true
  },
  {
    "id": 46,
    "name": "PLAIN BLACK T-SHIRT",
    "brand": "TRENDIFY",
    "price": 699.0,
    "old_price": 999.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality plain black t-shirt from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.3999999999999995,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 47,
    "name": "WHITE CREW NECK TEE",
    "brand": "TRENDIFY",
    "price": 699.0,
    "old_price": 999.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality white crew neck tee from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 48,
    "name": "NAVY POLO SHIRT",
    "brand": "TRENDIFY",
    "price": 1299.0,
    "old_price": 1799.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality navy polo shirt from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 27,
    "in_stock": true
  },
  {
    "id": 49,
    "name": "GREY HOODIE",
    "brand": "TRENDIFY",
    "price": 1899.0,
    "old_price": 2699.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality grey hoodie from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.7,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 29,
    "in_stock": true
  },
  {
    "id": 50,
    "name": "BLACK TRACKSUIT SET",
    "brand": "TRENDIFY",
    "price": 2499.0,
    "old_price": 3499.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality black tracksuit set from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.3,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 28,
    "in_stock": true
  },
  {
    "id": 51,
    "name": "SLIM FIT JEANS",
    "brand": "TRENDIFY",
    "price": 2199.0,
    "old_price": 2999.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality slim fit jeans from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.3999999999999995,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 26,
    "in_stock": true
  },
  {
    "id": 52,
    "name": "CASUAL CHINO PANTS",
    "brand": "TRENDIFY",
    "price": 1799.0,
    "old_price": 2499.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality casual chino pants from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 28,
    "in_stock": true
  },
  {
    "id": 53,
    "name": "FORMAL WHITE SHIRT",
    "brand": "TRENDIFY",
    "price": 1499.0,
    "old_price": 2099.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality formal white shirt from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 28,
    "in_stock": true
  },
  {
    "id": 54,
    "name": "CHECK CASUAL SHIRT",
    "brand": "TRENDIFY",
    "price": 1399.0,
    "old_price": 1899.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality check casual shirt from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.7,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 26,
    "in_stock": true
  },
  {
    "id": 55,
    "name": "ZIPPER HOODIE",
    "brand": "TRENDIFY",
    "price": 1999.0,
    "old_price": 2799.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality zipper hoodie from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.3,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 28,
    "in_stock": true
  },
  {
    "id": 56,
    "name": "SPORT SHORTS",
    "brand": "TRENDIFY",
    "price": 899.0,
    "old_price": 1299.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality sport shorts from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.3999999999999995,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 57,
    "name": "3PCS T-SHIRT PACK",
    "brand": "TRENDIFY",
    "price": 1599.0,
    "old_price": 2299.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality 3pcs t-shirt pack from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 58,
    "name": "BOMBER JACKET",
    "brand": "TRENDIFY",
    "price": 2999.0,
    "old_price": 4299.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality bomber jacket from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 59,
    "name": "KNIT SWEATER",
    "brand": "TRENDIFY",
    "price": 1699.0,
    "old_price": 2399.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality knit sweater from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.7,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 29,
    "in_stock": true
  },
  {
    "id": 60,
    "name": "CARGO JOGGERS",
    "brand": "TRENDIFY",
    "price": 1899.0,
    "old_price": 2599.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality cargo joggers from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.3,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 26,
    "in_stock": true
  },
  {
    "id": 61,
    "name": "PRINTED GRAPHIC TEE",
    "brand": "TRENDIFY",
    "price": 849.0,
    "old_price": 1199.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality printed graphic tee from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.3999999999999995,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 29,
    "in_stock": true
  },
  {
    "id": 62,
    "name": "LONG SLEEVE HENLEY",
    "brand": "TRENDIFY",
    "price": 1199.0,
    "old_price": 1699.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality long sleeve henley from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 29,
    "in_stock": true
  },
  {
    "id": 63,
    "name": "DENIM JACKET",
    "brand": "TRENDIFY",
    "price": 2799.0,
    "old_price": 3999.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality denim jacket from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 64,
    "name": "SUMMER LINEN SHIRT",
    "brand": "TRENDIFY",
    "price": 1599.0,
    "old_price": 2199.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality summer linen shirt from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.7,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 27,
    "in_stock": true
  },
  {
    "id": 65,
    "name": "WOMEN BASIC TEE",
    "brand": "TRENDIFY",
    "price": 649.0,
    "old_price": 949.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality women basic tee from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.3,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 31,
    "in_stock": true
  },
  {
    "id": 66,
    "name": "WOMEN WIDE LEG PANTS",
    "brand": "TRENDIFY",
    "price": 1699.0,
    "old_price": 2399.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality women wide leg pants from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.3999999999999995,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 29,
    "in_stock": true
  },
  {
    "id": 67,
    "name": "KIDS HOODIE",
    "brand": "TRENDIFY",
    "price": 999.0,
    "old_price": 1499.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality kids hoodie from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 33,
    "in_stock": true
  },
  {
    "id": 68,
    "name": "UNISEX OVERSIZED TEE",
    "brand": "TRENDIFY",
    "price": 999.0,
    "old_price": 1399.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality unisex oversized tee from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 28,
    "in_stock": true
  },
  {
    "id": 69,
    "name": "FLEECE SWEATSHIRT",
    "brand": "TRENDIFY",
    "price": 1799.0,
    "old_price": 2499.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality fleece sweatshirt from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.7,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 28,
    "in_stock": true
  },
  {
    "id": 70,
    "name": "TAILORED BLAZER",
    "brand": "TRENDIFY",
    "price": 3999.0,
    "old_price": 5499.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality tailored blazer from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.3,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 27,
    "in_stock": true
  },
  {
    "id": 71,
    "name": "SANDAL BEAUTY CREAM",
    "brand": "SANDAL",
    "price": 360.0,
    "old_price": 450.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality sandal beauty cream from SANDAL. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.4,
    "category": "Beauty",
    "variants": [],
    "discount_percent": 20,
    "in_stock": true
  },
  {
    "id": 72,
    "name": "FACE WASH ALOE",
    "brand": "TRENDIFY",
    "price": 450.0,
    "old_price": 650.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality face wash aloe from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.4,
    "category": "Beauty",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 73,
    "name": "MOISTURIZING LOTION",
    "brand": "TRENDIFY",
    "price": 550.0,
    "old_price": 799.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality moisturizing lotion from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.4,
    "category": "Beauty",
    "variants": [],
    "discount_percent": 31,
    "in_stock": true
  },
  {
    "id": 74,
    "name": "VITAMIN C SERUM",
    "brand": "TRENDIFY",
    "price": 899.0,
    "old_price": 1299.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality vitamin c serum from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.4,
    "category": "Beauty",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 75,
    "name": "SUNSCREEN SPF 50",
    "brand": "TRENDIFY",
    "price": 699.0,
    "old_price": 999.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality sunscreen spf 50 from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.4,
    "category": "Beauty",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 76,
    "name": "LIP BALM SET 3PCS",
    "brand": "TRENDIFY",
    "price": 399.0,
    "old_price": 599.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality lip balm set 3pcs from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.4,
    "category": "Beauty",
    "variants": [],
    "discount_percent": 33,
    "in_stock": true
  },
  {
    "id": 77,
    "name": "HAND CREAM TUBE",
    "brand": "TRENDIFY",
    "price": 349.0,
    "old_price": 499.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality hand cream tube from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.4,
    "category": "Beauty",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 78,
    "name": "BODY SCRUB",
    "brand": "TRENDIFY",
    "price": 599.0,
    "old_price": 849.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality body scrub from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.4,
    "category": "Beauty",
    "variants": [],
    "discount_percent": 29,
    "in_stock": true
  },
  {
    "id": 79,
    "name": "FACE MASK SHEET 5PCS",
    "brand": "TRENDIFY",
    "price": 499.0,
    "old_price": 749.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality face mask sheet 5pcs from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.4,
    "category": "Beauty",
    "variants": [],
    "discount_percent": 33,
    "in_stock": true
  },
  {
    "id": 80,
    "name": "MEN DE-TAN CREAM",
    "brand": "NICONI",
    "price": 550.0,
    "old_price": 799.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality men de-tan cream from NICONI. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.4,
    "category": "Beauty",
    "variants": [],
    "discount_percent": 31,
    "in_stock": true
  },
  {
    "id": 81,
    "name": "SHAVING FOAM",
    "brand": "JOCKEY",
    "price": 399.0,
    "old_price": 549.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality shaving foam from JOCKEY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.4,
    "category": "Beauty",
    "variants": [],
    "discount_percent": 27,
    "in_stock": true
  },
  {
    "id": 82,
    "name": "PERFUME 50ML",
    "brand": "TRENDIFY",
    "price": 1299.0,
    "old_price": 1899.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality perfume 50ml from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.4,
    "category": "Beauty",
    "variants": [],
    "discount_percent": 31,
    "in_stock": true
  },
  {
    "id": 83,
    "name": "ROLL-ON DEODORANT",
    "brand": "TRENDIFY",
    "price": 299.0,
    "old_price": 449.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality roll-on deodorant from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.4,
    "category": "Beauty",
    "variants": [],
    "discount_percent": 33,
    "in_stock": true
  },
  {
    "id": 84,
    "name": "NIGHT CREAM",
    "brand": "TRENDIFY",
    "price": 749.0,
    "old_price": 1099.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality night cream from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.4,
    "category": "Beauty",
    "variants": [],
    "discount_percent": 31,
    "in_stock": true
  },
  {
    "id": 85,
    "name": "MAKEUP REMOVER",
    "brand": "TRENDIFY",
    "price": 449.0,
    "old_price": 649.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality makeup remover from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.4,
    "category": "Beauty",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 86,
    "name": "HAIR WAX STICK",
    "brand": "IKT",
    "price": 449.0,
    "old_price": 649.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality hair wax stick from IKT. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Hair Care",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 87,
    "name": "SILICONE SCALP BRUSH",
    "brand": "TRENDIFY",
    "price": 299.0,
    "old_price": 449.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality silicone scalp brush from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Hair Care",
    "variants": [],
    "discount_percent": 33,
    "in_stock": true
  },
  {
    "id": 88,
    "name": "HAIR OIL APPLICATOR",
    "brand": "TRENDIFY",
    "price": 349.0,
    "old_price": 499.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality hair oil applicator from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Hair Care",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 89,
    "name": "ROOT TOUCH-UP STICK",
    "brand": "TRENDIFY",
    "price": 499.0,
    "old_price": 799.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality root touch-up stick from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Hair Care",
    "variants": [],
    "discount_percent": 37,
    "in_stock": true
  },
  {
    "id": 90,
    "name": "BEARD GROWTH OIL",
    "brand": "DR ALIES",
    "price": 699.0,
    "old_price": 999.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality beard growth oil from DR ALIES. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Hair Care",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 91,
    "name": "ARGAN HAIR OIL 100ML",
    "brand": "TRENDIFY",
    "price": 599.0,
    "old_price": 899.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality argan hair oil 100ml from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Hair Care",
    "variants": [],
    "discount_percent": 33,
    "in_stock": true
  },
  {
    "id": 92,
    "name": "ANTI DANDRUFF SHAMPOO",
    "brand": "TRENDIFY",
    "price": 549.0,
    "old_price": 799.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality anti dandruff shampoo from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Hair Care",
    "variants": [],
    "discount_percent": 31,
    "in_stock": true
  },
  {
    "id": 93,
    "name": "HAIR SERUM SHINE",
    "brand": "TRENDIFY",
    "price": 649.0,
    "old_price": 949.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality hair serum shine from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Hair Care",
    "variants": [],
    "discount_percent": 31,
    "in_stock": true
  },
  {
    "id": 94,
    "name": "BEARD COMB SET",
    "brand": "TRENDIFY",
    "price": 399.0,
    "old_price": 599.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality beard comb set from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Hair Care",
    "variants": [],
    "discount_percent": 33,
    "in_stock": true
  },
  {
    "id": 95,
    "name": "HAIR CLIPPER",
    "brand": "TRENDIFY",
    "price": 1899.0,
    "old_price": 2699.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality hair clipper from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Hair Care",
    "variants": [],
    "discount_percent": 29,
    "in_stock": true
  },
  {
    "id": 96,
    "name": "CURL DEFINING CREAM",
    "brand": "TRENDIFY",
    "price": 549.0,
    "old_price": 799.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality curl defining cream from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Hair Care",
    "variants": [],
    "discount_percent": 31,
    "in_stock": true
  },
  {
    "id": 97,
    "name": "DRY SHAMPOO SPRAY",
    "brand": "TRENDIFY",
    "price": 499.0,
    "old_price": 749.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality dry shampoo spray from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.5,
    "category": "Hair Care",
    "variants": [],
    "discount_percent": 33,
    "in_stock": true
  },
  {
    "id": 98,
    "name": "WIRELESS EARBUDS",
    "brand": "TRENDIFY",
    "price": 2499.0,
    "old_price": 3499.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality wireless earbuds from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6,
    "category": "Electronics",
    "variants": [],
    "discount_percent": 28,
    "in_stock": true
  },
  {
    "id": 99,
    "name": "POWER BANK 10000MAH",
    "brand": "TRENDIFY",
    "price": 1899.0,
    "old_price": 2699.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality power bank 10000mah from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6,
    "category": "Electronics",
    "variants": [],
    "discount_percent": 29,
    "in_stock": true
  },
  {
    "id": 100,
    "name": "USB-C FAST CHARGER",
    "brand": "TRENDIFY",
    "price": 899.0,
    "old_price": 1299.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality usb-c fast charger from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6,
    "category": "Electronics",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 101,
    "name": "BLUETOOTH SPEAKER",
    "brand": "TRENDIFY",
    "price": 2999.0,
    "old_price": 4299.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality bluetooth speaker from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6,
    "category": "Electronics",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 102,
    "name": "PHONE HOLDER CAR",
    "brand": "TRENDIFY",
    "price": 599.0,
    "old_price": 899.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality phone holder car from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6,
    "category": "Electronics",
    "variants": [],
    "discount_percent": 33,
    "in_stock": true
  },
  {
    "id": 103,
    "name": "LED SELFIE RING LIGHT",
    "brand": "TRENDIFY",
    "price": 1499.0,
    "old_price": 2199.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality led selfie ring light from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6,
    "category": "Electronics",
    "variants": [],
    "discount_percent": 31,
    "in_stock": true
  },
  {
    "id": 104,
    "name": "SMART WATCH BAND",
    "brand": "TRENDIFY",
    "price": 499.0,
    "old_price": 799.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality smart watch band from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6,
    "category": "Electronics",
    "variants": [],
    "discount_percent": 37,
    "in_stock": true
  },
  {
    "id": 105,
    "name": "TYPE-C DATA CABLE 2PCS",
    "brand": "TRENDIFY",
    "price": 449.0,
    "old_price": 699.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality type-c data cable 2pcs from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6,
    "category": "Electronics",
    "variants": [],
    "discount_percent": 35,
    "in_stock": true
  },
  {
    "id": 106,
    "name": "LAPTOP COOLING PAD",
    "brand": "TRENDIFY",
    "price": 1799.0,
    "old_price": 2499.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality laptop cooling pad from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6,
    "category": "Electronics",
    "variants": [],
    "discount_percent": 28,
    "in_stock": true
  },
  {
    "id": 107,
    "name": "MINI TRIPOD STAND",
    "brand": "TRENDIFY",
    "price": 799.0,
    "old_price": 1199.0,
    "image": "/static/images/no-image.svg",
    "gallery_images": [
      "/static/images/no-image.svg"
    ],
    "description": "Premium quality mini tripod stand from TRENDIFY. Fast delivery across Pakistan. Cash on delivery available.",
    "ratings": 4.6,
    "category": "Electronics",
    "variants": [],
    "discount_percent": 33,
    "in_stock": true
  }
]
''')

def load_products():
    """Load products from JSON. Prefer /data volume file; seed defaults if empty."""
    if os.path.exists(PRODUCTS_FILE):
        try:
            with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    return data
        except (json.JSONDecodeError, IOError):
            pass
    # Seed full catalog on first run
    save_products(DEFAULT_PRODUCTS)
    return json.loads(json.dumps(DEFAULT_PRODUCTS))




def save_products(products_list):
    """Save products to JSON file so they survive server restart."""
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(products_list, f, ensure_ascii=False, indent=2)


def load_orders():
    if os.path.exists(ORDERS_FILE):
        try:
            with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return []


def save_orders(orders_list):
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders_list, f, ensure_ascii=False, indent=2)


# Load into memory at startup
PRODUCTS = load_products()
ORDERS = load_orders()


ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'trendify2026'


def get_product_by_id(product_id):
    for product in PRODUCTS:
        if product['id'] == product_id:
            return product
    return None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Please login as admin first.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


# ============================================================
# STORE ROUTES
# ============================================================

@app.route('/')
def home():
    category = request.args.get('category', '').strip()
    q = request.args.get('q', '').strip().lower()

    filtered = PRODUCTS[:]

    if category and category.lower() != 'all':
        filtered = [p for p in filtered if p.get('category', '').lower() == category.lower()]

    if q:
        filtered = [
            p for p in filtered
            if q in p.get('name', '').lower()
            or q in p.get('description', '').lower()
            or q in p.get('brand', '').lower()
            or q in p.get('category', '').lower()
        ]

    # Unique categories for nav
    categories = sorted(set(p.get('category', 'General') for p in PRODUCTS if p.get('category')))

    return render_template(
        'index.html',
        products=filtered,
        categories=categories,
        active_category=category or 'All',
        search_query=request.args.get('q', '')
    )


@app.route('/search')
def search():
    """Redirect search form to home with query param."""
    q = request.args.get('q', '').strip()
    return redirect(url_for('home', q=q) if q else url_for('home'))


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = get_product_by_id(product_id)
    if not product:
        flash('Product not found!', 'danger')
        return redirect(url_for('home'))
    return render_template('product.html', product=product)


# ============================================================
# CART ROUTES
# ============================================================

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = get_product_by_id(product_id)
    if not product:
        flash('Product not found!', 'danger')
        return redirect(url_for('home'))

    qty = request.args.get('qty', 1, type=int)
    if qty < 1:
        qty = 1

    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']
    str_id = str(product_id)

    if str_id in cart:
        cart[str_id] += qty
    else:
        cart[str_id] = qty

    session.modified = True
    flash(f'{product["name"]} added to cart!', 'success')
    return redirect(url_for('cart'))


@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' in session:
        cart = session['cart']
        str_id = str(product_id)
        if str_id in cart:
            cart[str_id] -= 1
            if cart[str_id] <= 0:
                del cart[str_id]
            session.modified = True
            flash('Item updated in cart.', 'info')
    return redirect(url_for('cart'))


@app.route('/delete_from_cart/<int:product_id>')
def delete_from_cart(product_id):
    if 'cart' in session:
        cart = session['cart']
        str_id = str(product_id)
        if str_id in cart:
            del cart[str_id]
            session.modified = True
            flash('Item removed from cart.', 'info')
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    cart_session = session.get('cart', {})
    cart_items = []
    total = 0.0

    for str_id, quantity in cart_session.items():
        product = get_product_by_id(int(str_id))
        if product:
            subtotal = product['price'] * quantity
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })

    return render_template('cart.html', cart_items=cart_items, total=total)


# ============================================================
# CHECKOUT & ORDER
# ============================================================

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_session = session.get('cart', {})
    if not cart_session:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('cart'))

    cart_items = []
    total = 0.0
    for str_id, quantity in cart_session.items():
        product = get_product_by_id(int(str_id))
        if product:
            subtotal = product['price'] * quantity
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })

    if request.method == 'POST':
        order = {
            'id': len(ORDERS) + 1,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'email': request.form.get('email'),
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'name': f"{request.form.get('first_name', '')} {request.form.get('last_name', '')}".strip(),
            'address': request.form.get('address'),
            'city': request.form.get('city'),
            'postal_code': request.form.get('postal_code'),
            'phone': request.form.get('phone'),
            'country': request.form.get('country', 'Pakistan'),
            'payment_method': request.form.get('payment_method', 'Cash on Delivery (COD)'),
            'items': cart_items,
            'subtotal': total,
            'shipping': 199.00,
            'total': total + 199.00,
            'status': 'Processing'
        }
        ORDERS.append(order)
        save_orders(ORDERS)
        session.pop('cart', None)
        session.modified = True

        return render_template(
            'order_success.html',
            name=order['name'],
            payment_method=order['payment_method'],
            total=order['total']
        )

    return render_template('checkout.html', cart_items=cart_items, total=total)


@app.route('/order-success')
def order_success():
    return redirect(url_for('home'))


# ============================================================
# NEWSLETTER
# ============================================================

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email', '').strip()
    if email and '@' in email:
        flash('Thank you! You have successfully subscribed to our newsletter.', 'newsletter')
    else:
        flash('Please enter a valid email address.', 'danger')
    return redirect(request.referrer or url_for('home'))


# ============================================================
# STATIC PAGES
# ============================================================

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Thank you! Your message has been sent. We will contact you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')


@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy.html')


@app.route('/terms')
def terms():
    return render_template('terms.html')


@app.route('/return-policy')
def return_policy():
    return render_template('return_policy.html')


# ============================================================
# ADMIN ROUTES
# ============================================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('is_admin'):
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['is_admin'] = True
            flash('Welcome Admin! You are now logged in.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


@app.route('/admin/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        price = request.form.get('price', type=float)
        old_price = request.form.get('old_price', type=float) or None
        image = request.form.get('image', '').strip()
        description = request.form.get('description', '').strip()

        if not name or price is None:
            flash('Name and price are required.', 'danger')
            return redirect(url_for('add_product'))

        new_id = max([p['id'] for p in PRODUCTS], default=0) + 1
        discount = 0
        if old_price and old_price > price:
            discount = int(((old_price - price) / old_price) * 100)

        # Smart image path: accept filename or full path
        if image.startswith('http') or image.startswith('/static/'):
            img_path = image
        elif image.startswith('static/'):
            img_path = '/' + image
        else:
            img_path = f'/static/images/{image}'

        PRODUCTS.append({
            'id': new_id,
            'name': name,
            'brand': 'TRENDIFY',
            'price': price,
            'old_price': old_price,
            'image': img_path,
            'gallery_images': [img_path],
            'description': description or 'Premium quality product from Trendify.',
            'ratings': 4.5,
            'category': request.form.get('category', 'General'),
            'variants': [],
            'discount_percent': discount,
            'in_stock': True,
        })
        save_products(PRODUCTS)
        flash(f'Product "{name}" added successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('add_product.html')


@app.route('/admin/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = get_product_by_id(product_id)
    if not product:
        flash('Product not found!', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        product['name'] = request.form.get('name', product['name']).strip()
        product['price'] = request.form.get('price', type=float) or product['price']
        old_price = request.form.get('old_price', type=float)
        product['old_price'] = old_price if old_price else None
        product['image'] = request.form.get('image', product['image']).strip()
        product['description'] = request.form.get('description', product['description']).strip()

        if product['old_price'] and product['old_price'] > product['price']:
            product['discount_percent'] = int(
                ((product['old_price'] - product['price']) / product['old_price']) * 100
            )
        else:
            product['discount_percent'] = 0

        save_products(PRODUCTS)
        flash(f'Product "{product["name"]}" updated successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('edit_product.html', product=product)


@app.route('/admin/delete_product/<int:product_id>')
@login_required
def delete_product(product_id):
    global PRODUCTS
    product = get_product_by_id(product_id)
    if product:
        PRODUCTS = [p for p in PRODUCTS if p['id'] != product_id]
        save_products(PRODUCTS)
        flash(f'Product "{product["name"]}" deleted.', 'info')
    else:
        flash('Product not found!', 'danger')
    return redirect(url_for('home'))



@app.route('/admin/export_products')
@login_required
def export_products():
    """Download products.json backup — save this file on your computer."""
    from flask import Response
    payload = json.dumps(PRODUCTS, ensure_ascii=False, indent=2)
    return Response(
        payload,
        mimetype='application/json',
        headers={'Content-Disposition': 'attachment; filename=products_backup.json'}
    )


@app.route('/admin/import_products', methods=['GET', 'POST'])
@login_required
def import_products():
    """Upload a products_backup.json to restore all products."""
    global PRODUCTS
    if request.method == 'POST':
        f = request.files.get('file')
        if not f or not f.filename:
            flash('Please choose a JSON file.', 'danger')
            return redirect(url_for('import_products'))
        try:
            data = json.load(f.stream)
            if not isinstance(data, list) or len(data) == 0:
                flash('Invalid file: expected a non-empty product list.', 'danger')
                return redirect(url_for('import_products'))
            PRODUCTS = data
            save_products(PRODUCTS)
            flash(f'Restored {len(PRODUCTS)} products successfully!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash(f'Import failed: {e}', 'danger')
            return redirect(url_for('import_products'))
    return render_template('import_products.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1', host='0.0.0.0', port=port)
