#!/usr/bin/env python3
"""
Configuration file for Marine NGL Tool
Optimized for maximum speed and performance
"""

# Network Configuration
NETWORK_CONFIG = {
    'timeout': 8,  # Reduced timeout for faster requests
    'max_retries': 2,  # Reduced retries for speed
    'connection_pool_size': 100,  # Increased pool size
    'max_redirects': 3,  # Reduced redirects
    'verify_ssl': False,  # Disable SSL verification for speed
    'allow_redirects': True,
    'stream': False,  # Disable streaming for faster response
}

# Threading Configuration
THREADING_CONFIG = {
    'max_workers': 50,  # Maximum concurrent threads
    'thread_timeout': 2,  # Reduced thread timeout
    'queue_size': 1000,  # Increased queue size
    'batch_size': 10,  # Process requests in batches
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    'enable_connection_pooling': True,
    'enable_keep_alive': True,
    'enable_compression': True,
    'enable_caching': False,  # Disable caching for real-time updates
    'request_delay': 0.05,  # Reduced delay between requests
    'status_update_interval': 1000,  # Faster status updates (ms)
}

# Web Interface Configuration
WEB_CONFIG = {
    'debug': False,  # Disable debug mode for production
    'host': '0.0.0.0',
    'port': 5000,
    'threaded': True,
    'processes': 1,
}

# User Agent Configuration
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

# Request Headers Template
BASE_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Connection": "keep-alive",
    "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "X-Requested-With": "XMLHttpRequest"
}

# Emoji Configuration
EMOJI_LIST = [
    " 😊", " 😎", " 😍", " 😉", " 😁", " 😄", " 😃", " 🙂", " 😆", " 😅", " 🤣",
    " 😂", " 😋", " 😛", " 😜", " 🤪", " 🤩", " 🥰", " 😇", " 🙃", " 🥹", " 😌",
    " 🤗", " 😏", " 🤭", " 🫢", " 🫠", " 🤫", " 😭", " 😢", " 😥", " 😓", " 😞",
    " 😔", " 🙁", " ☹️", " 😠", " 😡", " 🤬", " 😤", " 😖", " 😫", " 😩", " 🥺",
    " 😱", " 😨", " 😰", " 😵", " 🤯", " 😳", " 😬", " 🫣", " 🥴", " 🤢", " 🤮",
    " 😷", " 🤒", " 🤕", " 🤧", " 🥶", " 🥵", " 😈", " 👿", " 💀", " 👻", " 👽",
    " 😺", " 😸", " 😹", " 😻", " 😼", " 😽", " 🙀", " 😿", " 😾", " 🤡", " ❤️",
    " 🧡", " 💛", " 💚", " 💙", " 💜", " 🤎", " 🖤", " 🤍", " 💓", " 💗", " 💖",
    " 💘", " 💝", " 💞", " 💕"
]

# API Endpoints
API_ENDPOINTS = {
    'submit': "https://ngl.link/api/submit",
    'user_check': "https://ngl.link/",
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'file': 'mngl.log',
    'max_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5,
}
