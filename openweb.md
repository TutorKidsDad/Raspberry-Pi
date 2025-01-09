To set up your Raspberry Pi as a hotspot with a captive portal and browser-based access to a pen drive, follow these steps:

---

### **Step 1: Set Up Raspberry Pi as a Wi-Fi Hotspot**
1. **Install and configure `dnsmasq` and `hostapd`:**
   ```bash
   sudo apt update
   sudo apt install dnsmasq hostapd
   ```
2. **Configure the static IP address:**
   Edit the `/etc/dhcpcd.conf` file:
   ```bash
   sudo nano /etc/dhcpcd.conf
   ```
   Add at the end:
   ```
   interface wlan0
   static ip_address=192.168.4.1/24
   nohook wpa_supplicant
   ```
   Restart the service:
   ```bash
   sudo service dhcpcd restart
   ```

3. **Set up `dnsmasq` for DHCP and DNS:**
   Edit `/etc/dnsmasq.conf`:
   ```bash
   sudo nano /etc/dnsmasq.conf
   ```
   Add:
   ```
   interface=wlan0
   dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
   ```

4. **Configure `hostapd` for the hotspot:**
   Edit `/etc/hostapd/hostapd.conf`:
   ```bash
   sudo nano /etc/hostapd/hostapd.conf
   ```
   Add:
   ```
   interface=wlan0
   driver=nl80211
   ssid=RaspberryPi
   hw_mode=g
   channel=7
   wmm_enabled=0
   macaddr_acl=0
   auth_algs=1
   ignore_broadcast_ssid=0
   ```
   Point `hostapd` to this config file:
   Edit `/etc/default/hostapd`:
   ```bash
   sudo nano /etc/default/hostapd
   ```
   Set:
   ```
   DAEMON_CONF="/etc/hostapd/hostapd.conf"
   ```

5. **Start the hotspot:**
   ```bash
   sudo systemctl unmask hostapd
   sudo systemctl enable hostapd
   sudo systemctl start hostapd
   ```

---

### **Step 2: Create a Captive Portal**
1. **Install a web server:**
   ```bash
   sudo apt install lighttpd
   ```

2. **Set up the captive portal:**
   Create a simple HTML file:
   ```bash
   sudo nano /var/www/html/index.html
   ```
   Example:
   ```html
   <html>
   <body>
       <h1>Login to Access the Pen Drive</h1>
       <form action="/login" method="POST">
           <input type="text" name="username" placeholder="Username">
           <input type="password" name="password" placeholder="Password">
           <button type="submit">Login</button>
       </form>
   </body>
   </html>
   ```

3. **Redirect all traffic to the captive portal:**
   Edit `/etc/dnsmasq.conf` to force DNS redirection:
   ```bash
   address=/#/192.168.4.1
   ```

   Restart `dnsmasq`:
   ```bash
   sudo systemctl restart dnsmasq
   ```

4. **Implement login handling:**
   Use a lightweight backend like PHP or Python Flask to handle logins and grant access to the pen drive.

---

### **Step 3: Share Pen Drive via Browser**
1. **Mount the pen drive:**
   Plug in the pen drive and find its path:
   ```bash
   sudo fdisk -l
   ```
   Mount it:
   ```bash
   sudo mount /dev/sda1 /mnt/usb
   ```

2. **Set up file sharing:**
   Symlink the pen drive to the web server:
   ```bash
   sudo ln -s /mnt/usb /var/www/html/usb
   ```
   Now files on the pen drive are accessible at `http://192.168.4.1/usb`.

---

### **Step 4: Test and Finalize**
- Connect to the hotspot.
- Open any browser, and you should see the captive portal.
- Login to access the pen drive.

Let me know if you need assistance with any specific part!
