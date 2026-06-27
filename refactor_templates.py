import os
import re

replacements = {
    r"url_for\('index'\)": "url_for('public.index')",
    r"url_for\('gallery_page'\)": "url_for('public.gallery_page')",
    r"url_for\('artists_page'\)": "url_for('public.artists_page')",
    r"url_for\('services_page'\)": "url_for('public.services_page')",
    r"url_for\('booking_page'\)": "url_for('customer.booking_page')",
    r"url_for\('login_page'\)": "url_for('auth.login')",
    r"url_for\('register_page'\)": "url_for('auth.register')",
    r"url_for\('login_post'\)": "url_for('auth.login')",
    r"url_for\('logout'\)": "url_for('auth.logout')",
    r"url_for\('admin_dashboard'\)": "url_for('admin.dashboard')",
    r"url_for\('customer_dashboard'\)": "url_for('customer.dashboard')",
}

def process_dir(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for pattern, repl in replacements.items():
                    content = re.sub(pattern, repl, content)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

if os.path.exists("app/templates"):
    process_dir("app/templates")
    print("Refactored app/templates")
elif os.path.exists("frontend/templates"):
    process_dir("frontend/templates")
    print("Refactored frontend/templates")
