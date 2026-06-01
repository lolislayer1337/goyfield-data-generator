from check_images import check_images
from check_unused_images import check_unused_images
from fetch_data import fetch_data
from fetch_locales import fetch_locales
from create_empty_merged_files import create_empty_merged_files_if_not_exists
from merge_data import merge_data, merge_locales


create_empty_merged_files_if_not_exists()

fetch_data()

fetch_locales()

merge_data()

merge_locales()

# check_images()

# check_unused_images()
