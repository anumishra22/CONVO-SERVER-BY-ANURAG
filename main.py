from flask import Flask, request, render_template_string
import requests
from threading import Thread, Event
import time
import random
import string

app = Flask(__name__)
app.debug = True

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

stop_events = {}
threads = {}

def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                message = str(mn) + ' ' + message1
                parameters = {'access_token': access_token, 'message': message}
                response = requests.post(api_url, data=parameters, headers=headers)
                if response.status_code == 200:
                    print(f"✅ Message Sent Successfully From token {access_token}: {message}")
                else:
                    print(f"❌ Message Failed From token {access_token}: {message}")
                time.sleep(time_interval)

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        token_option = request.form.get('tokenOption')
        if token_option == 'single':
            access_tokens = [request.form.get('singleToken')]
        else:
            token_file = request.files['tokenFile']
            access_tokens = token_file.read().decode().strip().splitlines()

        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))
        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        stop_events[task_id] = Event()
        thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
        threads[task_id] = thread
        thread.start()
        return f'Task started with ID: {task_id}'

    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>IMAGINE AS YOUR GF</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      margin: 0;
      padding: 0;
      background: url('https://files.catbox.moe/lor8af.jpg') no-repeat center center fixed;
      background-size: cover;
      font-family: 'Poppins', sans-serif;
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      color: #fff;
    }
    .container {
      width: 90%;
      max-width: 380px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.25);
      border-radius: 15px;
      padding: 25px 20px;
      text-align: center;
      box-shadow: 0 0 30px rgba(255,255,255,0.1);
      backdrop-filter: blur(10px);
    }
    h1 {
      font-size: 22px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 5px;
    }
    h2 {
      font-size: 15px;
      font-weight: 600;
      color: #eee;
      margin-bottom: 15px;
    }
    label {
      font-weight: 500;
      color: #eee;
      font-size: 14px;
      text-align: left;
      display: block;
      margin-bottom: 4px;
    }
    .form-control {
      background: rgba(255,255,255,0.1);
      border: 1px solid rgba(255,255,255,0.3);
      color: #fff;
      border-radius: 8px;
      height: 38px;
      margin-bottom: 12px;
      font-size: 13px;
      text-align: center;
      transition: 0.3s;
    }
    .form-control:focus {
      background: rgba(255,255,255,0.15);
      outline: none;
      box-shadow: 0 0 10px rgba(255,255,255,0.2);
    }
    .btn {
      width: 100%;
      background: rgba(255,255,255,0.15);
      border: 1px solid rgba(255,255,255,0.4);
      color: #fff;
      border-radius: 10px;
      font-weight: 600;
      height: 40px;
      transition: 0.3s;
    }
    .btn:hover {
      background: rgba(255,255,255,0.25);
    }
    .footer {
      text-align: center;
      font-size: 13px;
      color: #ccc;
      margin-top: 10px;
    }
    /* Hidden WhatsApp number */
    /* Contact: 6394812128 (hidden) */
  </style>
</head>
<body>
  <div class="container">
    <h1>OWNER — ANURAG MISHRA</h1>
    <h2>IMAGINE AS YOUR GF</h2>
    <form method="post" enctype="multipart/form-data">
      <label>Token Option</label>
      <select class="form-control" name="tokenOption" id="tokenOption" onchange="toggleTokenInput()" required>
        <option value="single">Single Token</option>
        <option value="multiple">Token File</option>
      </select>

      <div id="singleTokenInput">
        <input type="text" class="form-control" name="singleToken" placeholder="Enter Token">
      </div>

      <div id="tokenFileInput" style="display:none;">
        <input type="file" class="form-control" name="tokenFile">
      </div>

      <input type="text" class="form-control" name="threadId" placeholder="Inbox / Convo UID" required>
      <input type="text" class="form-control" name="kidx" placeholder="Hater Name" required>
      <input type="number" class="form-control" name="time" placeholder="Time (seconds)" required>
      <input type="file" class="form-control" name="txtFile" required>

      <button type="submit" class="btn mt-2">Start</button>
    </form>
    <div class="footer">Made by ANURAG MISHRA</div>
  </div>

  <script>
    function toggleTokenInput() {
      var option = document.getElementById('tokenOption').value;
      document.getElementById('singleTokenInput').style.display = (option === 'single') ? 'block' : 'none';
      document.getElementById('tokenFileInput').style.display = (option === 'multiple') ? 'block' : 'none';
    }
  </script>
</body>
</html>
''')

@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        return f'Task with ID {task_id} stopped.'
    else:
        return f'No task found with ID {task_id}.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
