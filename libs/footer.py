from django.urls import reverse
import datetime

from libs.settings import site_name, logo_url, site_phone, site_email, site_address_1_row, site_address_2_row


current_year = datetime.date.today().year

useful_links_title = 'Корисні посилання'
useful_links = [
    {"title": "Головна", "url": reverse("home"), "childs": 0},
    {"title": "Клієнти", "url": reverse("client_list"), "childs": 0},
    {"title": "Контакти", "url": reverse("contact_list"), "childs": 0},
    {"title": "Доступи", "url": reverse("access_list"), "childs": 0},
]

our_services_title = 'Наші послуги'
our_services = [
    {"title": "Головна", "url": reverse("home"), "childs": 0},
    {"title": "Клієнти", "url": reverse("client_list"), "childs": 0},
    {"title": "Контакти", "url": reverse("contact_list"), "childs": 0},
    {"title": "Доступи", "url": reverse("access_list"), "childs": 0},
]

footer_about = f"""
<a href="{logo_url }" class="d-flex align-items-center">
    <span class="sitename">{site_name}</span>
</a>
<div class="footer-contact pt-3">
    <p>{site_address_1_row}</p>
    <p>{site_address_2_row}</p>
    <p class="mt-3"><strong>Phone:</strong> <span>{site_phone}</span></p>
    <p><strong>Email:</strong> <span>{site_email}</span></p>
</div>
"""

footer_folow_us_title = "Ми в соціальних мережах"
footer_folow_us_text = "Слідкуйте за нами також на сторінках соцыальних мереж:"
footer_folow_us = f"""
<h4>{footer_folow_us_title}</h4>
                <p>{footer_folow_us_text}</p>
                <div class="social-links d-flex">
                    <a href=""><i class="bi bi-twitter-x"></i></a>
                    <a href=""><i class="bi bi-facebook"></i></a>
                    <a href=""><i class="bi bi-instagram"></i></a>
                    <a href=""><i class="bi bi-linkedin"></i></a>
                </div>
"""

footer_copyright = f"""
<p>
    ©<strong class="px-1 sitename">{site_name} 2025-{current_year}</strong> <span>All Rights Reserved</span>
</p>
        <div class="credits">
            Created by <a href="https://soft-master.iho.com.ua/" target="_blank">IFess</a>
        </div>
"""