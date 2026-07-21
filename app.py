#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CyberScan Pro - Advanced Network & Port Scanner (Real Pentesting Tool)
Developed for Security Auditing and Network Analysis.
"""

import os
import sys
import socket
import time
from datetime import datetime

# محاولة استيراد مكتبة Scapy لفحص الشبكة عبر حزم ARP
try:
    from scapy.all import ARP, Ether, srp
except ImportError:
    print("[-] مكتبة Scapy غير مثبتة. يرجى تثبيتها عبر الأمر: pip install scapy")
    sys.exit(1)

def print_banner():
    """طباعة واجهة الأداة الاحترافية"""
    banner = """
    ======================================================
    #                 CYBERSCAN PRO v1.0                 #
    #       Real Network & Port Scanning Tool            #
    ======================================================
    """
    print(banner)

def scan_network(ip_range):
    """
    فحص الشبكة الحقيقية واكتشاف الأجهزة المتصلة عبر حزم ARP حقيقية
    """
    print(f"\n[*] بدء فحص الشبكة الحقيقية للنطاق: {ip_range}")
    print("[*] جاري إرسال حزم ARP لطلب عناوين الأجهزة المتاحة...\n")
    
    try:
        # إنشاء حزمة ARP لطلب العناوين وحزمة إيثرنت للبث
        arp_request = ARP(pdst=ip_range)
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        
        # إرسال الحزمة واستقبال الإجابات الحقيقية من الأجهزة
        answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]
        
        devices = []
        for element in answered_list:
            device_info = {"ip": element[1].psrc, "mac": element[1].hwsrc}
            devices.append(device_info)
            
        return devices
    except Exception as e:
        print(f"[-] حدث خطأ أثناء فحص الشبكة: {e}")
        print("[-] ملاحظة: فحص الشبكة الحقيقي يتطلب صلاحيات مسؤول النظام (Administrator/Root).")
        return []

def scan_ports(target_ip, ports_to_scan):
    """
    فحص المنافذ الحقيقية للجهاز المستهدف باستخدام اتصالات TCP Socket حقيقية
    """
    print(f"\n[*] بدء فحص المنافذ للجهاز: {target_ip}")
    print(f"[*] جاري فحص {len(ports_to_scan)} منفذ مستهدف...")
    print("-" * 50)
    print(f"{'المنفذ (Port)':<15}{'الحالة (Status)':<20}{'الخدمة المتوقعة':<15}")
    print("-" * 50)
    
    start_time = time.time()
    open_ports_count = 0
    
    for port in ports_to_scan:
        try:
            # إنشاء اتصال Socket حقيقي لاختبار المنفذ
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5) # وقت انتظار قصير لسرعة الفحص
            
            # محاولة الاتصال بالمنفذ
            result = s.connect_ex((target_ip, port))
            
            if result == 0:
                # إذا كانت النتيجة 0 فالمنفذ مفتوح حقيقياً
                try:
                    service = socket.getservbyname(port)
                except:
                    service = "Unknown"
                
                print(f"TCP / {port:<9}\033[92mمفتوح [OPEN]\033[0m       {service:<15}")
                open_ports_count += 1
            s.close()
            
        except KeyboardInterrupt:
            print("\n[-] تم إيقاف الفحص بواسطة المستخدم.")
            sys.exit()
        except socket.error:
            pass
            
    end_time = time.time()
    print("-" * 50)
    print(f"[✓] تم الفحص في: {end_time - start_time:.2f} ثانية.")
    print(f"[✓] عدد المنافذ المفتوحة المكتشفة: {open_ports_count}")

def main():
    print_banner()
    
    # التحقق من صلاحيات المسؤول (مهم للفحص الحقيقي)
    if os.name != 'nt' and os.geteuid() != 0:
        print("[⚠️] تنبيه: بعض وظائف فحص الشبكة المتقدمة تحتاج صلاحيات Root/Root Access لتشغيلها بنجاح.")
        print("[*] يمكنك تشغيل الأداة باستخدام الأمر: sudo python3 cyber_scan.py\n")
        
    print("اختر نوع الفحص الحقيقي المطلوب:")
    print("1. فحص الشبكة المحلية واكتشاف الأجهزة (ARP Network Scan)")
    print("2. فحص المنافذ لجهاز محدد (Detailed TCP Port Scan)")
    
    choice = input("\nأدخل رقم الاختيار (1 أو 2): ")
    
    if choice == "1":
        ip_range = input("أدخل نطاق الشبكة لفحصه (مثال 192.168.1.1/24): ")
        if not ip_range:
            ip_range = "192.168.1.1/24" # افتراضي لمعظم الموجهات المنزلية
            
        scan_results = scan_network(ip_range)
        
        if scan_results:
            print("\n[+] الأجهزة النشطة المكتشفة على الشبكة الحقيقية:")
            print("-" * 50)
            print(f"{'IP Address':<20}{'MAC Address':<20}")
            print("-" * 50)
            for device in scan_results:
                print(f"{device['ip']:<20}{device['mac']:<20}")
        else:
            print("[-] لم يتم العثور على أجهزة نشطة أو الصلاحيات غير كافية.")
            
    elif choice == "2":
        target = input("أدخل عنوان الـ IP أو الدومين المستهدف (مثال: 192.168.1.5 أو scanme.nmap.org): ")
        if not target:
            print("[-] خطأ: يجب تحديد هدف للفحص.")
            return
            
        try:
            target_ip = socket.gethostbyname(target)
        except socket.gaierror:
            print("[-] خطأ: تعذر الوصول إلى الهدف، تأكد من الاسم أو الاتصال.")
            return
            
        # قائمة بأشهر المنافذ الأمنية والإدارية في اختبار الاختراق
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 1433, 3306, 3389, 8080]
        
        scan_ports(target_ip, common_ports)
    else:
        print("[-] اختيار غير صحيح.")

if __name__ == "__main__":
    main()
