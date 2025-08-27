#!/usr/bin/env python3
"""
Marine NGL Tool - Web Application
A Flask-based web interface for the mNGL spam tool
"""

from flask import Flask, render_template, request, jsonify
import threading
import time
import queue
import os
import sys
from main import mNGL

# Initialize Flask app
app = Flask(__name__)

# Global variables for managing instances
running_instances = {}
instance_counter = 0

class WebNGL(mNGL):
    """Extended mNGL class for web interface"""
    
    def __init__(self, username, threads, question, enable_emoji=False):
        # Initialize base mNGL properties
        self.messages = []
        self._username = username
        self._threads = threads
        self._question = question
        self._ngl = "https://ngl.link/api/submit"
        self._timeout = 8  # Giảm timeout để tăng tốc độ
        self.NAME_TOOL = "mNGL Web Tool"
        self.VERSION_TOOL = "v1.0.0"
        self.enable_emoji = enable_emoji
        
        # Initialize device ID and headers
        self.device_id = self._random_str(36)
        self.base_headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://ngl.link",
            "Referer": f"https://ngl.link/{self._username}",
            "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        
        # Initialize locks and queues
        self.success_lock = threading.Lock()
        self.print_lock = threading.Lock()
        self.successful_runs = 0
        self.should_stop = False
        self.print_queue = queue.Queue()

    def _input(self):
        """Override input method for web interface"""
        pass

    def landing(self):
        """Override landing method for web interface"""
        return "mNGL Web Tool"

    def banner(self):
        """Override banner method for web interface"""
        pass
        
    def _convert(self, input_str: str = None) -> str:
        """Convert input string to username format"""
        if input_str is None:
            return self._username
            
        input_str = input_str.strip()
        if input_str.startswith("https://ngl.link/"):
            try:
                from urllib.parse import urlparse
                _parsed = urlparse(input_str)
                if _parsed.scheme != "https" or _parsed.netloc != "ngl.link":
                    return None
                username = _parsed.path.lstrip("/")
                if not username:
                    return None
                return username
            except Exception:
                return None
        else:
            if not input_str:
                return None
            return input_str
            
    def _random_str(self, length: int = 10, chars: str = "abcdefghijklmnopqrstuvwxyz0123456789") -> str:
        """Generate random string"""
        import random
        return "".join(random.choice(chars) for _ in range(length))
        
    def _check_user(self, username: str) -> bool:
        """Check if user exists"""
        try:
            import requests
            response = requests.get(
                f"https://ngl.link/{username}",
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "text/html",
                },
                timeout=self._timeout,
                verify=True,
            )
            return "Could not find user" not in response.text
        except Exception:
            return False
            
    def run(self, target: str = None, threads: int = None, note: str = None) -> None:
        """Run the attack"""
        target = target or self._username
        threads = threads or self._threads
        note = note or self._question
        
        self.should_stop = False
        self.successful_runs = 0
        
        # Start sending messages with optimized speed
        while not self.should_stop and self.successful_runs < threads:
            try:
                self.mNGL(1)  # Send one message
                time.sleep(0.05)  # Giảm delay từ 0.1s xuống 0.05s để tăng tốc độ
            except Exception as e:
                print(f"Error in attack: {e}")
                break
                
    def mNGL(self, thread_id: int):
        """Send NGL message"""
        import random
        import requests
        from urllib.parse import urlencode
        
        icon = (random.choice([
            " 😊", " 😎", " 😍", " 😉", " 😁", " 😄", " 😃", " 🙂", " 😆", " 😅", " 🤣",
            " 😂", " 😋", " 😛", " 😜", " 🤪", " 🤩", " 🥰", " 😇", " 🙃", " 🥹", " 😌",
            " 🤗", " 😏", " 🤭", " 🫢", " 🫠", " 🤫", " 😭", " 😢", " 😥", " 😓", " 😞",
            " 😔", " 🙁", " ☹️", " 😠", " 😡", " 🤬", " 😤", " 😖", " 😫", " 😩", " 🥺",
            " 😱", " 😨", " 😰", " 😵", " 🤯", " 😳", " 😬", " 🫣", " 🥴", " 🤢", " 🤮",
            " 😷", " 🤒", " 🤕", " 🤧", " 🥶", " 🥵", " 😈", " 👿", " 💀", " 👻", " 👽",
            " 😺", " 😸", " 😹", " 😻", " 😼", " 😽", " 🙀", " 😿", " 😾", " 🤡", " ❤️",
            " 🧡", " 💛", " 💚", " 💙", " 💜", " 🤎", " 🖤", " 🤍", " 💓", " 💗", " 💖",
            " 💘", " 💝", " 💞", " 💕"
        ]) if self.enable_emoji else "")
        
        try:
            data = {
                "username": self._username,
                "question": self._question + icon,
                "deviceId": self.device_id,
                "gameSlug": "",
                "referrer": "",
            }
            
            response = requests.post(
                self._ngl,
                headers=self.base_headers,
                data=urlencode(data),
                timeout=self._timeout,
                verify=False,  # Tắt SSL verification để tăng tốc độ
            )
            response.raise_for_status()
            
            with self.success_lock:
                self.successful_runs += 1
                if self.successful_runs >= self._threads:
                    self.should_stop = True
            
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            return False

# Routes
@app.route('/')
def index():
    """Main page route"""
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_attack():
    """Start a new attack"""
    global instance_counter
    
    try:
        data = request.get_json()
        
        # Extract and validate input
        username = data.get('username', '').strip()
        threads = int(data.get('threads', 50))
        question = data.get('question', 'Marine').strip()
        enable_emoji = data.get('enable_emoji', False)
        
        # Validation
        if not username:
            return jsonify({'error': 'Vui lòng nhập tên người dùng'}), 400
        
        if threads < 1 or threads > 500:
            return jsonify({'error': 'Số threads phải từ 1 đến 500'}), 400
        
        if len(question) > 70:
            return jsonify({'error': 'Tin nhắn không được quá 70 ký tự'}), 400
        
        # Convert username if it's a URL
        temp_instance = WebNGL("temp", 1, "temp")
        converted_username = temp_instance._convert(username)
        if not converted_username:
            return jsonify({'error': 'Username không hợp lệ'}), 400
        
        # Create NGL instance
        ngl_instance = WebNGL(converted_username, threads, question, enable_emoji)
        
        # Check if user exists
        if not ngl_instance._check_user(converted_username):
            return jsonify({'error': f'Người dùng "{converted_username}" không tồn tại'}), 400
        
        # Generate instance ID
        instance_counter += 1
        instance_id = instance_counter
        
        # Store instance
        running_instances[instance_id] = {
            'instance': ngl_instance,
            'status': 'running',
            'start_time': time.time()
        }
        
        # Start attack in background thread
        def run_attack():
            try:
                ngl_instance.run(converted_username, threads, question)
                # Check if attack completed successfully or was stopped
                if ngl_instance.successful_runs >= threads:
                    running_instances[instance_id]['status'] = 'completed'
                    running_instances[instance_id]['completion_message'] = f'Hoàn thành! Đã gửi {ngl_instance.successful_runs} tin nhắn'
                else:
                    running_instances[instance_id]['status'] = 'stopped'
                    running_instances[instance_id]['completion_message'] = f'Đã dừng! Đã gửi {ngl_instance.successful_runs} tin nhắn'
            except Exception as e:
                running_instances[instance_id]['status'] = 'error'
                running_instances[instance_id]['error'] = str(e)
        
        # Start the attack thread
        attack_thread = threading.Thread(target=run_attack)
        attack_thread.daemon = True
        attack_thread.start()
        
        return jsonify({
            'success': True,
            'instance_id': instance_id,
            'message': f'Đã bắt đầu tấn công {username} với {threads} threads'
        })
        
    except Exception as e:
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500

@app.route('/status/<int:instance_id>')
def get_status(instance_id):
    """Get status of a specific attack instance"""
    if instance_id not in running_instances:
        return jsonify({'error': 'Không tìm thấy cuộc tấn công'}), 404
    
    instance = running_instances[instance_id]
    ngl_instance = instance['instance']
    
    return jsonify({
        'status': instance['status'],
        'successful_runs': ngl_instance.successful_runs,
        'target_threads': ngl_instance._threads,
        'username': ngl_instance._username,
        'question': ngl_instance._question,
        'start_time': instance['start_time'],
        'error': instance.get('error', None),
        'completion_message': instance.get('completion_message', None)
    })

@app.route('/stop/<int:instance_id>')
def stop_attack(instance_id):
    """Stop a running attack instance"""
    if instance_id not in running_instances:
        return jsonify({'error': 'Không tìm thấy cuộc tấn công'}), 404
    
    instance = running_instances[instance_id]
    ngl_instance = instance['instance']
    
    if instance['status'] == 'running':
        ngl_instance.should_stop = True
        instance['status'] = 'stopped'
        instance['completion_message'] = f'Đã dừng thủ công! Đã gửi {ngl_instance.successful_runs} tin nhắn'
    
    return jsonify({'success': True, 'message': 'Đang dừng tấn công...'})

@app.route('/instances')
def list_instances():
    """List all attack instances"""
    instances = []
    
    for instance_id, instance in running_instances.items():
        ngl_instance = instance['instance']
        instances.append({
            'id': instance_id,
            'status': instance['status'],
            'username': ngl_instance._username,
            'question': ngl_instance._question,
            'threads': ngl_instance._threads,
            'successful_runs': ngl_instance.successful_runs,
            'target_threads': ngl_instance._threads,
            'start_time': instance['start_time'],
            'completion_message': instance.get('completion_message', None)
        })
    
    return jsonify(instances)

# Main execution
if __name__ == "__main__":
    # Tạo thư mục static nếu chưa có
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    print("🚀 Đang khởi động Marine NGL Tool...")
    print("📱 Mở trình duyệt và truy cập: http://localhost:5000")
    print("✨ Tool đã sẵn sàng sử dụng!")
    
    # Chạy Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)

# Export app cho Vercel
app.debug = False
