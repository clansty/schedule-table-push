import os

from playwright.sync_api import sync_playwright
import base64
import requests
import json

FORWARD_GROUP = os.getenv('FORWARD_GROUP')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
ONEBOT_URL = os.getenv('ONEBOT_URL')


def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    device = playwright.devices['Pixel 2 XL']
    context = browser.new_context(**device)
    page = context.new_page()
    page.goto("https://react-schedule-table.vercel.app/")
    screenshot_bytes = page.screenshot(full_page=True)
    page.close()
    context.close()
    browser.close()
    base64_data = base64.b64encode(screenshot_bytes)
    post_data = {
        'group_id': FORWARD_GROUP,
        'message': {
            'type': 'image',
            'data': {
                'file': 'base64://' + str(base64_data, 'utf-8')
            }
        }
    }
    rq = requests.post(ONEBOT_URL,
                       auth=(USERNAME, PASSWORD),
                       data=json.dumps(post_data))
    print(rq.json())


with sync_playwright() as playwright:
    run(playwright)
