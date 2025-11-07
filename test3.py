import os
import sys
import re
import cv2
from time import sleep
import requests
import pandas as pd
from datetime import *
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as BS
from tqdm import tqdm, trange
from PIL import Image
from urllib.request import urlopen
from transliterate import translit

# my modules
from donor_checkers.utils.image_tools import format_image, get_ascii_url, perturb_image
from donor_checkers.utils.yandex_api import get_new_link, create_folder, upload_file

df = pd.read_excel(f"Promtorg.xlsx", sheet_name='Объявления')
df = df.drop_duplicates(subset=["Id"], keep='last')
df.to_excel(f'Promtorg.xlsx', sheet_name='Объявления', index=False)

