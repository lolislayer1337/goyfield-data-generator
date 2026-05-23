from check_images import check_images
from check_unused_images import check_unused_images
from fetch_data import fetch_data
from fetch_locales import fetch_locales


fetch_data()

fetch_locales()

check_images()

check_unused_images()
