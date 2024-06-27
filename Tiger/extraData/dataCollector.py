import json
import requests
categories = [
    "baby-products/baby-bath-products",
    "baby-products/baby-skin-care",
    "baby-products/baby-wipes",
    "baby-products/diapers-offers",
    "beauty/bath-and-body-products",
    "beauty/beard-shaving",
    "beauty/eye-care",
    "beauty/fragrances",
    "beauty/fragrances/deodorants",
    "beauty/fragrances/men-perfumes",
    "beauty/fragrances/women-perfumes",
    "beauty/hair-care-products",
    "beauty/hair-care-products/hair-conditioners",
    "beauty/hair-care-products/hair-styling",
    "beauty/hair-care-products/hair-treatment",
    "beauty/hair-care-products/shampoos",
    "beauty/men-hair-removal",
    "beauty/skin-care-products",
    "beauty/skin-care-products/creams-moisturizers",
    "beauty/skin-care-products/facemasks-peels",
    "beauty/skin-care-products/facewash-cleansers",
    "beauty/skin-care-products/lotions-massage-oils",
    "beauty/skin-care-products/scrubs-exfoliators",
    "beauty/skin-care-products/serums-facial-oils",
    "beauty/skin-care-products/sunscreens",
    "earphones-headphones-offers/earbuds-airpods",
    "earphones-headphones-offers/earphones",
    "earphones-headphones-offers/neckbands",
    "electronics-products/automotive-accessories",
    "electronics-products/cameras-offers",
    "electronics-products/computers",
    "electronics-products/data-storage",
    "electronics-products/mechanical-tools",
    "electronics-products/monitors-offers",
    "electronics-products/power-banks-offers",
    "electronics-products/smart-gadgets",
    "electronics-products/smart-watch-bands-offers",
    "electronics-products/speakers-offers",
    "electronics-products/tablet-offers",
    "electronics-products/televisions-offers",
    "electronics-products/video-games",
    "fashion-accessories/men-bags-wallets",
    "fashion-accessories/men-watches-offers",
    "fashion-accessories/women-handbags-wallets",
    "fashion-accessories/women-watches-offers",
    "grocery/dairy-products",
    "grocery/household-care-products",
    "grocery/packaged-food",
    "grocery/personal-care",
    "grocery/personal-care/personal-hygiene-products",
    "grocery/snacks-and-beverages",
    "grocery/staples",
    "health-care-supplements/sports-supplements",
    "health-care-supplements/wellness-supplements",
    "home-appliances/air-conditioners-offers",
    "home-appliances/air-coolers",
    "home-appliances/air-purifiers",
    "home-appliances/cooling-fan",
    "home-appliances/geysers-offers",
    "home-appliances/irons-offers",
    "home-appliances/refrigerators-offers",
    "home-appliances/room-heaters-offers",
    "home-appliances/vaccum-cleaners-offers",
    "home-appliances/washing-machines-offers",
    "kitchen-appliances/air-fryer-offers",
    "kitchen-appliances/breakfast-appliances",
    "kitchen-appliances/food-processor-offers",
    "kitchen-appliances/hand-blenders-offers",
    "kitchen-appliances/induction-stove-offers",
    "kitchen-appliances/juicer-mixer-grinder-offers",
    "kitchen-appliances/kitchen-chimney",
    "kitchen-appliances/kitchenware-offers",
    "kitchen-appliances/microwave-ovens-offers",
    "kitchen-appliances/water-purifiers-offers",
    "laptops-offers",
    "lingerie",
    "men-clothing/men-jeans-trousers",
    "men-clothing/men-shirts",
    "men-clothing/men-tshirts",
    "men-clothing/men-winterwear",
    "men-shoes/men-casual-shoes",
    "men-shoes/men-formal-shoes",
    "men-shoes/men-slippers-flip-flops",
    "men-shoes/men-sports-shoes",
    "mobile-phones-offers",
    "personal-care-appliances/hair-dryers",
    "personal-care-appliances/hair-straighteners-offers",
    "personal-care-appliances/health-care-appliances",
    "personal-care-appliances/health-care-appliances/thermometer",
    "personal-care-appliances/shavers-trimmers-offers",
    "pet-care",
    "women-clothing/handbag-and-wallets",
    "women-clothing/saree-offers",
    "women-clothing/women-dresses",
    "women-clothing/women-ethnic-wear",
    "women-clothing/women-jeans-trousers",
    "women-clothing/women-kurtas-kurtis",
    "women-clothing/women-tops-tshirts",
    "women-clothing/women-winterwear",
    "women-shoes/women-casual-shoes",
    "women-shoes/women-formal-shoes",
    "women-shoes/women-heels",
    "women-shoes/women-sandals",
    "women-shoes/women-sports-shoes"
]
for category in categories:
    page = 1
    categoryData = []
    while page > 0:
        url = "https://cashkaro.com/pps/products?baseURL=category/"+category+"&include=products,filters,seo_content,cms_block&device=Desktop&page[number]="+str(page)+"&page[size]=100"

        payload = {}
        headers = {
            'authority': 'cashkaro.com',
            'referer': 'https://cashkaro.com/'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()
        print(len(data), category)
        if len(data) > 0:
            categoryData.extend(data)
            page += 1
        else:
            page = 0
    with open(category.replace("/", "_")+".json", "w") as file:
        json.dump(categoryData, file)
