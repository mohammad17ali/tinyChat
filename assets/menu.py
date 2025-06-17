import openai
import csv
from fuzzywuzzy import fuzz
import pandas as pd

openai.api_key = "your-api-key"

image_urls = [
    "https://example.com/menu1.jpg",
    "https://example.com/menu2.jpg",
]

def extract_texts(image_urls):
    extracted_texts = []
    flag_count = 0

    for url in image_urls:
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "The attached image is of a restaurant menu. Extract menu items, their prices and their category from this restaurant menu. If category is not present, use 'All' as the default category. If the image does not resemble a restaurant menu respond with 'NO MENU FOUND', or if it is not readable respond with 'MENU NOT READABLE'."},
                        {"type": "image_url", "image_url": {"url": url}}
                    ]
                }
            ],
            max_tokens=2000
        )
        if response['choices'][0]['message']['content'] == "NO MENU FOUND" or response['choices'][0]['message']['content'] == "MENU NOT READABLE":
            flag_count += 1
        else:
            extracted_texts.append(response['choices'][0]['message']['content'])

    if flag_count == len(image_urls):
        return "FLAG"
        print("No menu found or menu not readable in any of the images.")

    combined_text = "\n\n".join(extracted_texts)

    return combined_text

def get_menu_csv(combined_text)
    # Use GPT-4 to interpret and convert to structured CSV
    final_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": f"""Here is the combined menu data from multiple images:

    {combined_text}

    Please extract the menu items, their prices, and their categories, and format them as CSV with three columns: 'Item', 'Price' and 'Category'.
    If default category 'All' is found for all items, use intelligent mapping and categorisation for all menu items based on the cuisine type, starter/main course, beverage, veg/non veg, etc
    """
            }
        ],
        max_tokens=2000
    )

    csv_output = final_response['choices'][0]['message']['content']
    return csv_output

# with open("menu_data.csv", "w", encoding="utf-8") as f:
#     f.write(csv_output)

def get menu_df(csv):
    csv = io.StringIO(get_menu_csv(extract_texts(image_urls)))
    df = pd.read_csv(csv)
    return df


def find_best_image_match(menu_item, image_df):
    best_score = 0
    best_match_id = None

    for index, row in image_df.iterrows():
        score = fuzz.partial_ratio(menu_item.lower(), row['item_name'].lower())
        if score > best_score:
            best_score = score
            best_match_id = row['image_id']

    return best_match_id

def get_image_url(df, image_db):
    menu_items = df['items']

    images = []

    for item in menu_items:
        matched_image_id = find_best_image_match(item, image_db)
        images.append(matched_image_id)

    df['image_url'] = pd.Series(images)
    return df


#images -> cloudinary-api
# images_list = list(image_urls)
userId = get_user_id
extracted_texts = extract_texts(image_urls)

if 'FLAG' in extracted_texts:
    #route to return dialog message
else:
    df = get_menu_csv(extract_texts(image_urls))
df = get_image_url(df, image_db)
